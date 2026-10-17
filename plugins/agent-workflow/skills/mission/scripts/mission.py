#!/usr/bin/env python3
"""Persist small, worktree-bound mission continuity records.

The CLI stores JSON outside the repository and only invokes git read-only through
argument vectors. It never executes a recorded action or any user-supplied text.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple

try:
    import fcntl
except ImportError:  # pragma: no cover - exercised only on non-POSIX hosts.
    fcntl = None  # type: ignore


STATE_VERSION = 1
MISSION_ID = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
STATUSES = {"pending", "in_progress", "blocked", "complete"}


class MissionError(Exception):
    """A concise, safe error suitable for the command line."""


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def fail(message: str) -> None:
    raise MissionError(message)


def git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=str(cwd), text=True, capture_output=True, check=False
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        fail("mission requires a Git worktree: " + detail)
    return result.stdout.strip()


def repository_identity(cwd: Path) -> Dict[str, str]:
    root = Path(git(cwd, "rev-parse", "--show-toplevel")).resolve()
    common_raw = Path(git(cwd, "rev-parse", "--git-common-dir"))
    common = (cwd / common_raw).resolve() if not common_raw.is_absolute() else common_raw.resolve()
    head = git(cwd, "rev-parse", "HEAD")
    material = (str(root) + "\0" + str(common)).encode("utf-8")
    return {
        "id": hashlib.sha256(material).hexdigest()[:24],
        "worktree": str(root),
        "common_dir": str(common),
        "head": head,
    }


def validate_mission_id(value: str) -> str:
    if not MISSION_ID.fullmatch(value):
        fail("mission id must use lowercase letters, digits, and hyphens; path separators are not allowed")
    return value


def within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def state_root(value: str, repo_root: Path) -> Path:
    raw = Path(value).expanduser()
    raw_absolute = raw.absolute()
    if raw.exists() and raw.is_symlink():
        fail("state directory may not be a symlink")
    root = raw.resolve()
    if within(raw_absolute, repo_root) or within(root, repo_root):
        fail("state directory must be outside the repository")
    return root


def secure_directory(path: Path) -> None:
    """Create a path only when each directory we own is a real directory."""
    if path.exists():
        if path.is_symlink() or not path.is_dir():
            fail("state directory contains an unsafe symlink or non-directory")
        return
    parent = path.parent
    if parent != path:
        secure_directory(parent)
    path.mkdir(mode=0o700)


def paths(root: Path, identity: Dict[str, str], mission_id: str, create: bool) -> Tuple[Path, Path]:
    if create:
        secure_directory(root)
        secure_directory(root / "worktrees")
        secure_directory(root / "worktrees" / identity["id"])
    else:
        for directory in (root, root / "worktrees", root / "worktrees" / identity["id"]):
            if directory.exists() or directory.is_symlink():
                if directory.is_symlink() or not directory.is_dir():
                    fail("state directory contains an unsafe symlink or non-directory")
    base = root / "worktrees" / identity["id"]
    return base / (mission_id + ".json"), base / (mission_id + ".lock")


def assert_safe_file(path: Path) -> None:
    if path.exists() or path.is_symlink():
        try:
            os.lstat(path)
        except OSError as error:
            fail("cannot inspect state file: " + str(error))
        if os.path.islink(path) or not os.path.isfile(path):
            fail("state file may not be a symlink or non-regular file")


def foreign_mission(root: Path, own_id: str, mission_id: str) -> bool:
    worktrees = root / "worktrees"
    if not worktrees.exists() or worktrees.is_symlink() or not worktrees.is_dir():
        return False
    for directory in worktrees.iterdir():
        if directory.name != own_id and directory.is_dir() and not directory.is_symlink():
            candidate = directory / (mission_id + ".json")
            if candidate.exists() or candidate.is_symlink():
                return True
    return False


@contextmanager
def locked(lock_path: Path) -> Iterator[None]:
    if fcntl is None:
        fail("mission requires POSIX fcntl locking; this platform is unsupported")
    assert_safe_file(lock_path)
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(str(lock_path), flags, 0o600)
    except OSError as error:
        fail("cannot open mission lock safely: " + str(error))
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            fail("mission lock contention; inspect the other writer and retry")
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def read_state(path: Path) -> Dict[str, Any]:
    assert_safe_file(path)
    if not path.exists():
        fail("mission state not found")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        fail("mission state is corrupted and was not changed: " + str(error))
    validate_state(value)
    return value


def is_positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def corrupted() -> None:
    fail("mission state is corrupted or has an unsupported version and was not changed")


def valid_evidence(entries: Any) -> bool:
    if not isinstance(entries, list):
        return False
    paths_seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            return False
        path, digest, device, inode = entry.get("path"), entry.get("sha256"), entry.get("device"), entry.get("inode")
        if set(entry) != {"path", "sha256", "device", "inode"} or not isinstance(path, str) or not Path(path).is_absolute() or not isinstance(digest, str) or not SHA256.fullmatch(digest) or not is_positive_int(device) or not is_positive_int(inode):
            return False
        if path in paths_seen:
            return False
        paths_seen.add(path)
    return True


def validate_state(value: Any) -> None:
    if not isinstance(value, dict) or value.get("state_version") != STATE_VERSION:
        corrupted()
    required = {"state_version", "id", "revision", "created_at", "updated_at", "outcome", "constraints", "next_action", "status", "blocked_reason", "milestones", "decisions", "repo", "history"}
    if set(value) != required or not isinstance(value["id"], str) or not MISSION_ID.fullmatch(value["id"]):
        corrupted()
    if not is_positive_int(value["revision"]) or not all(isinstance(value[field], str) and value[field].strip() for field in ("created_at", "updated_at", "outcome", "next_action")):
        corrupted()
    if not isinstance(value["constraints"], list) or not all(isinstance(item, str) for item in value["constraints"]):
        corrupted()
    if not isinstance(value["decisions"], list) or not all(isinstance(item, str) for item in value["decisions"]):
        corrupted()
    if not isinstance(value["status"], str) or value["status"] not in STATUSES or (value["status"] == "blocked") != isinstance(value["blocked_reason"], str):
        corrupted()
    if isinstance(value["blocked_reason"], str) and not value["blocked_reason"].strip():
        corrupted()
    milestones = value["milestones"]
    if not isinstance(milestones, list) or not milestones:
        corrupted()
    milestone_ids = set()
    for milestone in milestones:
        if not isinstance(milestone, dict) or set(milestone) != {"id", "description", "acceptance", "status", "blocked_reason", "evidence"}:
            corrupted()
        if not isinstance(milestone["id"], str) or not MISSION_ID.fullmatch(milestone["id"]) or milestone["id"] in milestone_ids:
            corrupted()
        milestone_ids.add(milestone["id"])
        if not all(isinstance(milestone[field], str) and milestone[field].strip() for field in ("description", "acceptance")):
            corrupted()
        if not isinstance(milestone["status"], str) or milestone["status"] not in STATUSES or (milestone["status"] == "blocked") != isinstance(milestone["blocked_reason"], str):
            corrupted()
        if isinstance(milestone["blocked_reason"], str) and not milestone["blocked_reason"].strip():
            corrupted()
        if not valid_evidence(milestone["evidence"]):
            corrupted()
        if milestone["status"] == "complete" and not milestone["evidence"]:
            corrupted()
    repo = value["repo"]
    if not isinstance(repo, dict) or set(repo) != {"worktree", "common_dir", "initial_head", "current_head"}:
        corrupted()
    if not all(isinstance(repo[field], str) and repo[field] for field in ("worktree", "common_dir", "initial_head", "current_head")):
        corrupted()
    if not Path(repo["worktree"]).is_absolute() or not Path(repo["common_dir"]).is_absolute():
        corrupted()
    if not all(re.fullmatch(r"[0-9a-f]{40,64}", repo[field]) for field in ("initial_head", "current_head")):
        corrupted()
    history = value["history"]
    if not isinstance(history, list) or not history:
        corrupted()
    for event in history:
        if not isinstance(event, dict) or not is_positive_int(event.get("revision")) or not isinstance(event.get("at"), str) or not event["at"].strip() or not isinstance(event.get("action"), str) or not event["action"].strip():
            corrupted()
        allowed = {"revision", "at", "action"}
        if event["action"] == "checkpoint":
            allowed.add("status")
        if set(event) != allowed or (event["action"] == "checkpoint" and
                                    (not isinstance(event["status"], str) or event["status"] not in STATUSES)):
            corrupted()


def atomic_write(path: Path, value: Dict[str, Any]) -> None:
    assert_safe_file(path)
    encoded = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    descriptor, temporary = tempfile.mkstemp(prefix=".mission-", suffix=".tmp", dir=str(path.parent))
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except OSError as error:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        fail("could not atomically write mission state: " + str(error))


def assert_bound(state: Dict[str, Any], identity: Dict[str, str]) -> None:
    repo = state.get("repo")
    if not isinstance(repo, dict) or repo.get("worktree") != identity["worktree"] or repo.get("common_dir") != identity["common_dir"]:
        fail("mission belongs to a different repository or worktree")


def load_for_current(root: Path, identity: Dict[str, str], mission_id: str) -> Tuple[Path, Path, Dict[str, Any]]:
    state_path, lock_path = paths(root, identity, mission_id, create=False)
    if not state_path.exists() and not state_path.is_symlink() and foreign_mission(root, identity["id"], mission_id):
        fail("mission belongs to a different repository or worktree")
    state = read_state(state_path)
    assert_bound(state, identity)
    return state_path, lock_path, state


def parse_milestone(value: str) -> Dict[str, Any]:
    pieces = value.split("|", 2)
    if len(pieces) != 3 or not all(piece.strip() for piece in pieces):
        fail("--milestone must be id|description|acceptance")
    milestone_id, description, acceptance = (piece.strip() for piece in pieces)
    if not MISSION_ID.fullmatch(milestone_id):
        fail("milestone id must use lowercase letters, digits, and hyphens")
    return {"id": milestone_id, "description": description, "acceptance": acceptance, "status": "pending", "blocked_reason": None, "evidence": []}


def parse_milestone_status(value: str) -> Tuple[str, str]:
    if "=" not in value:
        fail("--milestone-status must be id=status")
    milestone_id, status = value.split("=", 1)
    if not MISSION_ID.fullmatch(milestone_id) or status not in STATUSES:
        fail("--milestone-status must name a valid milestone id and status")
    return milestone_id, status


def parse_milestone_blocked_reason(value: str) -> Tuple[str, str]:
    if "=" not in value:
        fail("--milestone-blocked-reason must be id=reason")
    milestone_id, reason = value.split("=", 1)
    if not MISSION_ID.fullmatch(milestone_id) or not reason.strip():
        fail("--milestone-blocked-reason must be id=reason")
    return milestone_id, reason


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def evidence_entries(values: Sequence[str], repo_root: Path) -> Dict[str, List[Dict[str, Any]]]:
    entries: Dict[str, List[Dict[str, Any]]] = {}
    for value in values:
        if "=" not in value:
            fail("--evidence must be milestone-id=/explicit/output-file")
        milestone_id, raw_path = value.split("=", 1)
        if not MISSION_ID.fullmatch(milestone_id) or not raw_path:
            fail("--evidence must be milestone-id=/explicit/output-file")
        candidate = Path(raw_path).expanduser()
        if candidate.is_symlink():
            fail("evidence path may not be a symlink")
        try:
            resolved = candidate.resolve(strict=True)
        except OSError as error:
            fail("evidence path must name an existing file: " + str(error))
        if not resolved.is_file():
            fail("evidence path must name a file, not a directory")
        try:
            resolved.relative_to(repo_root)
        except ValueError:
            pass
        else:
            fail("evidence artifacts must be explicitly named files outside the repository")
        metadata = resolved.stat()
        entry = {"path": str(resolved), "sha256": sha256(resolved), "device": metadata.st_dev, "inode": metadata.st_ino}
        bucket = entries.setdefault(milestone_id, [])
        if entry["path"] not in {item["path"] for item in bucket}:
            bucket.append(entry)
    return entries


def validate_evidence(entries: Sequence[Dict[str, Any]], milestone_id: str, repo_root: Path) -> None:
    if not entries:
        fail("milestone %s requires at least one registered evidence file with a hash" % milestone_id)
    for entry in entries:
        path = Path(entry["path"])
        if path.is_symlink():
            fail("registered evidence became a symlink; completion was not recorded")
        try:
            resolved = path.resolve(strict=True)
        except OSError:
            fail("registered evidence is missing; completion was not recorded")
        try:
            resolved.relative_to(repo_root)
        except ValueError:
            pass
        else:
            fail("registered evidence now resolves inside the repository; completion was not recorded")
        metadata = resolved.stat()
        if str(resolved) != entry["path"] or not resolved.is_file() or metadata.st_dev != entry["device"] or metadata.st_ino != entry["inode"] or sha256(resolved) != entry["sha256"]:
            fail("registered evidence changed; completion was not recorded")


def merge_evidence(existing_entries: Sequence[Dict[str, Any]], additions: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Keep registered evidence immutable while allowing idempotent repeats."""
    existing = {entry["path"]: entry for entry in existing_entries}
    for entry in additions:
        prior = existing.get(entry["path"])
        if prior is not None and prior != entry:
            fail("registered evidence changed and cannot be re-registered")
        existing.setdefault(entry["path"], entry)
    return [existing[key] for key in sorted(existing)]


def head_report(state: Dict[str, Any], identity: Dict[str, str]) -> Dict[str, Any]:
    initial = state["repo"].get("initial_head")
    return {"initial": initial, "current": identity["head"], "advanced": initial != identity["head"]}


def output(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, sort_keys=True))


def mutate(state: Dict[str, Any], identity: Dict[str, str], expected: int, action: str, details: Dict[str, Any]) -> None:
    if state["status"] == "complete":
        fail("completed missions are immutable; create a new mission for new scope")
    if state["revision"] != expected:
        fail("stale revision: expected %s, current %s" % (expected, state["revision"]))
    state["revision"] += 1
    state["updated_at"] = now()
    state["repo"]["current_head"] = identity["head"]
    state["history"].append({"revision": state["revision"], "at": state["updated_at"], "action": action, **details})


def command_create(args: argparse.Namespace, root: Path, identity: Dict[str, str]) -> None:
    mission_id = validate_mission_id(args.mission_id)
    if not args.outcome.strip() or not args.next_action.strip():
        fail("outcome and next action must not be blank")
    milestones = [parse_milestone(value) for value in args.milestone]
    if not milestones:
        fail("create requires at least one --milestone")
    if len({item["id"] for item in milestones}) != len(milestones):
        fail("milestone ids must be unique")
    state_path, lock_path = paths(root, identity, mission_id, create=True)
    with locked(lock_path):
        if state_path.exists() or state_path.is_symlink():
            fail("mission already exists; completed missions require a new mission id for new scope")
        timestamp = now()
        state: Dict[str, Any] = {
            "state_version": STATE_VERSION,
            "id": mission_id,
            "revision": 1,
            "created_at": timestamp,
            "updated_at": timestamp,
            "outcome": args.outcome,
            "constraints": args.constraint,
            "next_action": args.next_action,
            "status": "pending",
            "blocked_reason": None,
            "milestones": milestones,
            "decisions": [],
            "repo": {"worktree": identity["worktree"], "common_dir": identity["common_dir"], "initial_head": identity["head"], "current_head": identity["head"]},
            "history": [{"revision": 1, "at": timestamp, "action": "create"}],
        }
        atomic_write(state_path, state)
    output({"mission": state, "head": head_report(state, identity), "warning": "HEAD advanced since creation" if identity["head"] != state["repo"]["initial_head"] else None})


def command_show(args: argparse.Namespace, root: Path, identity: Dict[str, str]) -> None:
    _, _, state = load_for_current(root, identity, validate_mission_id(args.mission_id))
    output({"mission": state, "head": head_report(state, identity), "warning": "HEAD advanced since creation" if identity["head"] != state["repo"]["initial_head"] else None})


def command_checkpoint(args: argparse.Namespace, root: Path, identity: Dict[str, str]) -> None:
    mission_id = validate_mission_id(args.mission_id)
    state_path, lock_path = paths(root, identity, mission_id, create=True)
    with locked(lock_path):
        if not state_path.exists() and foreign_mission(root, identity["id"], mission_id):
            fail("mission belongs to a different repository or worktree")
        state = read_state(state_path)
        assert_bound(state, identity)
        if args.status == "complete":
            fail("use complete only after every milestone is complete and evidence is valid")
        if args.status == "blocked" and (not args.blocked_reason or not args.blocked_reason.strip()):
            fail("blocked status requires --blocked-reason")
        if not args.next_action.strip():
            fail("next action must not be blank")
        status_updates = dict(parse_milestone_status(value) for value in args.milestone_status)
        reasons = dict(parse_milestone_blocked_reason(value) for value in args.milestone_blocked_reason)
        additions = evidence_entries(args.evidence, Path(identity["worktree"]))
        milestones = {item["id"]: item for item in state["milestones"]}
        for milestone_id in set(status_updates) | set(reasons) | set(additions):
            if milestone_id not in milestones:
                fail("unknown milestone id: " + milestone_id)
        for milestone_id, status in status_updates.items():
            if status == "blocked" and milestone_id not in reasons:
                fail("blocked milestone status requires --milestone-blocked-reason id=reason")
            if status == "complete" and milestones[milestone_id]["status"] != "complete" and not additions.get(milestone_id):
                fail("marking a milestone complete requires --evidence milestone-id=/explicit/output-file")
        for milestone_id in reasons:
            if status_updates.get(milestone_id) != "blocked":
                fail("milestone blocked reasons require that milestone's status to be blocked")
        mutate(state, identity, args.expected_revision, "checkpoint", {"status": args.status})
        state["status"] = args.status
        state["blocked_reason"] = args.blocked_reason if args.status == "blocked" else None
        state["next_action"] = args.next_action
        for milestone_id, status in status_updates.items():
            milestone = milestones[milestone_id]
            milestone["status"] = status
            milestone["blocked_reason"] = reasons[milestone_id] if status == "blocked" else None
        for milestone_id, additions_for_milestone in additions.items():
            milestones[milestone_id]["evidence"] = merge_evidence(milestones[milestone_id]["evidence"], additions_for_milestone)
        state["decisions"].extend(args.decision)
        atomic_write(state_path, state)
    output({"mission": state, "head": head_report(state, identity), "warning": "HEAD advanced since creation" if identity["head"] != state["repo"]["initial_head"] else None})


def command_resume(args: argparse.Namespace, root: Path, identity: Dict[str, str]) -> None:
    _, _, state = load_for_current(root, identity, validate_mission_id(args.mission_id))
    next_unfinished = next((item for item in state["milestones"] if item["status"] != "complete"), None)
    inspect_first: Optional[str] = None
    if state["status"] in {"in_progress", "blocked"}:
        reason = state.get("blocked_reason") or "effects may be in progress or uncertain"
        inspect_first = "Inspect current effects before acting: " + reason
    output({
        "mission": state,
        "head": head_report(state, identity),
        "next_unfinished": next_unfinished,
        "next_action": state["next_action"],
        "changes": {"status": state["status"], "decisions_recorded": len(state["decisions"]), "head_advanced": state["repo"]["initial_head"] != identity["head"]},
        "inspect_first": inspect_first,
        "replay_action": False,
    })


def command_complete(args: argparse.Namespace, root: Path, identity: Dict[str, str]) -> None:
    mission_id = validate_mission_id(args.mission_id)
    state_path, lock_path = paths(root, identity, mission_id, create=True)
    with locked(lock_path):
        if not state_path.exists() and foreign_mission(root, identity["id"], mission_id):
            fail("mission belongs to a different repository or worktree")
        state = read_state(state_path)
        assert_bound(state, identity)
        if state["status"] == "complete":
            fail("completed missions are immutable; create a new mission for new scope")
        if state["revision"] != args.expected_revision:
            fail("stale revision: expected %s, current %s" % (args.expected_revision, state["revision"]))
        additions = evidence_entries(args.evidence, Path(identity["worktree"]))
        milestones = {item["id"]: item for item in state["milestones"]}
        for milestone_id, additions_for_milestone in additions.items():
            if milestone_id not in milestones:
                fail("unknown milestone id: " + milestone_id)
            milestones[milestone_id]["evidence"] = merge_evidence(milestones[milestone_id]["evidence"], additions_for_milestone)
        if any(item["status"] != "complete" for item in state["milestones"]):
            fail("all milestones must be complete before completing the mission")
        for milestone in state["milestones"]:
            validate_evidence(milestone["evidence"], milestone["id"], Path(identity["worktree"]))
        mutate(state, identity, args.expected_revision, "complete", {})
        state["status"] = "complete"
        state["blocked_reason"] = None
        atomic_write(state_path, state)
    output({"mission": state, "head": head_report(state, identity), "evidence_note": "Recorded evidence hashes show files were unchanged at completion; they are not independent proof of the outcome."})


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Persist worktree-bound mission continuity as JSON.")
    result.add_argument("--state-dir", default=str(Path.home() / ".local" / "state" / "agent-missions"), help="external directory for mission JSON; never stored in the repository")
    commands = result.add_subparsers(dest="command", required=True)

    create = commands.add_parser("create", help="create one mission with outcome, milestones, and next action")
    create.add_argument("mission_id")
    create.add_argument("--outcome", required=True)
    create.add_argument("--constraint", action="append", default=[])
    create.add_argument("--milestone", action="append", default=[], metavar="ID|DESCRIPTION|ACCEPTANCE")
    create.add_argument("--next-action", required=True)

    show = commands.add_parser("show", help="show a mission and HEAD provenance")
    show.add_argument("mission_id")

    checkpoint = commands.add_parser("checkpoint", help="record status, decisions, next action, milestone state, and optional evidence")
    checkpoint.add_argument("mission_id")
    checkpoint.add_argument("--expected-revision", type=int, required=True)
    checkpoint.add_argument("--status", choices=sorted(STATUSES - {"complete"}), required=True)
    checkpoint.add_argument("--blocked-reason")
    checkpoint.add_argument("--next-action", required=True)
    checkpoint.add_argument("--decision", action="append", default=[])
    checkpoint.add_argument("--milestone-status", action="append", default=[], metavar="ID=STATUS")
    checkpoint.add_argument("--milestone-blocked-reason", action="append", default=[], metavar="ID=REASON")
    checkpoint.add_argument("--evidence", action="append", default=[], metavar="ID=FILE")

    resume = commands.add_parser("resume", help="report next unfinished work; never replay a recorded action")
    resume.add_argument("mission_id")

    complete = commands.add_parser("complete", help="complete only when every milestone and registered evidence is valid")
    complete.add_argument("mission_id")
    complete.add_argument("--expected-revision", type=int, required=True)
    complete.add_argument("--evidence", action="append", default=[], metavar="ID=FILE")
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parser().parse_args(argv)
    try:
        cwd = Path.cwd().resolve()
        identity = repository_identity(cwd)
        root = state_root(args.state_dir, Path(identity["worktree"]))
        commands = {"create": command_create, "show": command_show, "checkpoint": command_checkpoint, "resume": command_resume, "complete": command_complete}
        commands[args.command](args, root, identity)
        return 0
    except MissionError as error:
        print("mission: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
