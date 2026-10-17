#!/usr/bin/env python3
"""Move installed skills into a dated archive folder and back. Never deletes.

Commands:
  plan NAME...                 print exactly what `archive` would move; changes nothing
  archive NAME... --yes        move each skill into <archive-root>/<YYYY-MM-DD>/<name>
  restore NAME --from DIR      move an archived skill back to where it came from

Exit codes:
  0  success (or a plan was printed)
  1  refused: no --yes, a bad name, a plugin-managed skill, a symlink that
     points outside the skill roots, or a destination that already exists
  2  bad command line
  3  skill or archive record not found
  4  a move failed (for example, the archive root is on another disk)
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import shlex
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

PLAIN_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
RECORD_SUFFIX = ".restore.txt"
EXIT_OK, EXIT_REFUSED, EXIT_USAGE, EXIT_NOT_FOUND, EXIT_MOVE_FAILED = 0, 1, 2, 3, 4


class Refusal(Exception):
    def __init__(self, message: str, code: int = EXIT_REFUSED) -> None:
        super().__init__(message)
        self.code = code


def skill_roots(home: Path, project: Path) -> List[Path]:
    roots = []
    for base in (home, project):
        for folder in (".agents", ".codex", ".claude"):
            roots.append(base / folder / "skills")
    return list(dict.fromkeys(roots))


def within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def check_name(name: str) -> None:
    if ":" in name:
        plugin = name.split(":", 1)[0]
        raise Refusal(
            "%s is installed by the plugin %r. Uninstall or disable the plugin instead "
            "(Claude Code: /plugin)." % (name, plugin)
        )
    if not PLAIN_NAME.match(name) or ".." in name:
        raise Refusal("%r is not a plain skill name (no path separators or '..')." % name)


def plugin_owner(name: str, home: Path) -> Optional[str]:
    """Return the plugin that ships a skill folder with this name, if any."""
    cache = home / ".claude" / "plugins" / "cache"
    if not cache.is_dir():
        return None
    for skill_md in sorted(cache.glob("*/*/*/skills/%s/SKILL.md" % name)):
        return skill_md.parents[3].name
    return None


def locate(name: str, home: Path, project: Path, follow_symlinks: bool) -> List[dict]:
    """Find every installed copy of a skill and decide how each one would move."""
    check_name(name)
    roots = skill_roots(home, project)
    real_roots = []
    for root in roots:
        try:
            real_roots.append(root.resolve(strict=True))
        except OSError:
            continue
    plugins_dir = (home / ".claude" / "plugins").resolve()
    found = []
    seen_parents = set()
    for root in roots:
        entry = root / name
        if not (entry.is_symlink() or entry.exists()):
            continue
        parent = root.resolve()
        if parent in seen_parents:
            continue  # the same folder reached through an aliased skill root
        seen_parents.add(parent)
        item = {"source": entry, "kind": "directory", "target": None}
        if entry.is_symlink():
            target = Path(os.readlink(entry))
            resolved = (entry.parent / target).resolve()
            item.update(kind="symlink", target=str(target))
            if within(resolved, plugins_dir):
                raise Refusal(
                    "%s points into the Claude Code plugin folder, so a plugin manages it. "
                    "Uninstall or disable that plugin instead (Claude Code: /plugin)." % entry
                )
            if not any(within(resolved, root_real) for root_real in real_roots) and not follow_symlinks:
                raise Refusal(
                    "%s is a symlink to %s, outside the skill roots. Pass --follow-symlinks to "
                    "archive the symlink itself (the target is never moved)." % (entry, resolved)
                )
        elif not entry.is_dir():
            continue
        elif within(entry.resolve(), plugins_dir):
            raise Refusal("%s is managed by a plugin. Uninstall or disable that plugin instead." % entry)
        found.append(item)
    if not found:
        plugin = plugin_owner(name, home)
        if plugin:
            raise Refusal(
                "%s is installed by the plugin %r, not as a standalone skill. Uninstall or disable "
                "the plugin instead (Claude Code: /plugin)." % (name, plugin)
            )
        raise Refusal("No installed skill named %r in the skill roots." % name, EXIT_NOT_FOUND)
    # Move real folders before symlinks so the plain <name> slot holds the skill itself.
    found.sort(key=lambda item: (item["kind"] != "directory", str(item["source"])))
    return found


def plan_moves(name: str, items: List[dict], day_dir: Path) -> List[Tuple[dict, Path]]:
    moves = []
    for index, item in enumerate(items):
        dest = day_dir / (name if index == 0 else "%s~%d" % (name, index + 1))
        if dest.exists() or dest.is_symlink():
            raise Refusal("Archive destination %s already exists; nothing was moved." % dest)
        moves.append((item, dest))
    record = day_dir / (name + RECORD_SUFFIX)
    if record.exists():
        raise Refusal("Archive record %s already exists; nothing was moved." % record)
    return moves


def restore_command(name: str, day_dir: Path, args: argparse.Namespace) -> str:
    parts = [
        "python3", str(Path(__file__).resolve()), "restore", name, "--from", str(day_dir),
        "--home", str(args.home), "--project", str(args.project),
    ]
    return " ".join(shlex.quote(part) for part in parts)


def describe(item: dict) -> str:
    if item["kind"] == "symlink":
        return "symlink to %s; only the link moves, never its target" % item["target"]
    return "directory"


def gather(args: argparse.Namespace) -> List[Tuple[str, List[Tuple[dict, Path]]]]:
    day_dir = args.archive_root / datetime.date.today().isoformat()
    plans = []
    for name in dict.fromkeys(args.names):
        items = locate(name, args.home, args.project, args.follow_symlinks)
        plans.append((name, plan_moves(name, items, day_dir)))
    return plans


def cmd_plan(args: argparse.Namespace) -> int:
    plans = gather(args)
    print("Plan only: nothing has moved. Archiving needs `archive ... --yes`.")
    for name, moves in plans:
        day_dir = moves[0][1].parent
        print("\n%s" % name)
        for item, dest in moves:
            print("  would move %s (%s)\n          to %s" % (item["source"], describe(item), dest))
        print("  would write %s" % (day_dir / (name + RECORD_SUFFIX)))
        print("  restore with: %s" % restore_command(name, day_dir, args))
    return EXIT_OK


def undo(done: List[Tuple[Path, Path]]) -> List[str]:
    """Move already-moved items back; return the ones that could not be moved."""
    stuck = []
    for moved_to, moved_from in reversed(done):
        try:
            if moved_from.exists() or moved_from.is_symlink():
                raise OSError(17, "occupied")
            os.rename(moved_to, moved_from)
        except OSError:
            stuck.append(str(moved_to))
    return stuck


def cmd_archive(args: argparse.Namespace) -> int:
    if not args.yes:
        raise Refusal("Refusing to archive without --yes. Run `plan` first and show it to the owner.")
    plans = gather(args)  # every check runs before anything moves
    for name, moves in plans:
        day_dir = moves[0][1].parent
        day_dir.mkdir(parents=True, exist_ok=True)
        record_lines = [
            "# Skill archive record for %s, written %s." % (name, datetime.datetime.now().isoformat(timespec="seconds")),
            "# Restore it with:",
            restore_command(name, day_dir, args),
            "# Moves, as: move<TAB>archived path<TAB>original path<TAB>kind",
        ]
        record_lines += ["move\t%s\t%s\t%s" % (dest, item["source"], item["kind"]) for item, dest in moves]
        record = day_dir / (name + RECORD_SUFFIX)
        try:
            # The record is written first so no move can happen without a way back.
            with record.open("x", encoding="utf-8") as handle:
                handle.write("\n".join(record_lines) + "\n")
        except OSError as error:
            raise Refusal("Could not write %s (%s); nothing was moved." % (record, error.strerror), EXIT_MOVE_FAILED)
        done = []
        for item, dest in moves:
            try:
                if dest.exists() or dest.is_symlink():
                    raise OSError(17, "destination appeared during the move")
                os.rename(item["source"], dest)
            except OSError as error:
                stuck = undo(done)
                detail = (
                    " These could not be moved back, see %s: %s" % (record, ", ".join(stuck)) if stuck
                    else " Nothing for %s stays archived; choose an --archive-root on the same disk." % name
                )
                raise Refusal(
                    "Could not move %s to %s (%s).%s" % (item["source"], dest, error.strerror, detail),
                    EXIT_MOVE_FAILED,
                )
            done.append((dest, item["source"]))
        for item, dest in moves:
            print("archived %s -> %s" % (item["source"], dest))
        print("record: %s" % record)
        print("restore with: %s" % restore_command(name, day_dir, args))
    return EXIT_OK


def read_record(name: str, source: Path) -> Tuple[Path, List[Tuple[Path, Path]]]:
    candidates = [source / (name + RECORD_SUFFIX)]
    if source.name == name:
        candidates.append(source.parent / (name + RECORD_SUFFIX))
    for record in candidates:
        if record.is_file():
            moves = []
            for line in record.read_text(encoding="utf-8").splitlines():
                parts = line.split("\t")
                if len(parts) == 4 and parts[0] == "move":
                    moves.append((Path(parts[1]), Path(parts[2])))
            if moves:
                return record, moves
    raise Refusal("No archive record for %r in %s." % (name, source), EXIT_NOT_FOUND)


def cmd_restore(args: argparse.Namespace) -> int:
    check_name(args.name)
    record, moves = read_record(args.name, args.source)
    roots = skill_roots(args.home, args.project)
    day_dir = record.parent
    allowed_names = {args.name} | {"%s~%d" % (args.name, index) for index in range(2, 100)}
    if len({original for _, original in moves}) != len(moves) or len({archived for archived, _ in moves}) != len(moves):
        raise Refusal("Record %s lists a path twice; nothing was restored." % record)
    for archived, original in moves:
        if archived.parent != day_dir or archived.name not in allowed_names:
            raise Refusal("Record %s points outside its archive folder; nothing was restored." % record)
        if not (archived.exists() or archived.is_symlink()):
            raise Refusal("Archived copy %s is missing; nothing was restored." % archived, EXIT_NOT_FOUND)
        if original.exists() or original.is_symlink():
            raise Refusal("%s already exists; nothing was restored." % original)
        if original.name != args.name or not any(original.parent == root for root in roots):
            raise Refusal("Record %s points outside the skill roots; nothing was restored." % record)
    done = []
    for archived, original in moves:
        try:
            original.parent.mkdir(parents=True, exist_ok=True)
            if original.exists() or original.is_symlink():
                raise OSError(17, "the original location is occupied")
            os.rename(archived, original)
        except OSError as error:
            stuck = undo(done)
            raise Refusal(
                "Could not move %s back (%s).%s" % (
                    archived, error.strerror,
                    " Also stuck: %s" % ", ".join(stuck) if stuck else " Nothing was restored.",
                ),
                EXIT_MOVE_FAILED,
            )
        done.append((original, archived))
        print("restored %s -> %s" % (archived, original))
    print("The record %s was kept." % record)
    return EXIT_OK


def parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--home", type=Path, help="Home folder whose skill roots to use (default: your home).")
    common.add_argument("--project", type=Path, help="Project whose .claude/.agents/.codex skills to include (default: current folder).")
    common.add_argument("--archive-root", type=Path, help="Archive folder (default <home>/.agents/skills-archive).")
    top = argparse.ArgumentParser(
        description="Archive installed skills into a dated folder, or restore them. Never deletes.",
        epilog="Exit codes: 0 ok, 1 refused, 2 bad command line, 3 not found, 4 move failed.",
    )
    commands = top.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan", parents=[common], help="Print what archive would move.")
    plan.add_argument("names", nargs="+", metavar="NAME")
    plan.add_argument("--follow-symlinks", action="store_true", help="Allow symlinks whose target is outside the skill roots.")
    archive = commands.add_parser("archive", parents=[common], help="Move skills into the archive (needs --yes).")
    archive.add_argument("names", nargs="+", metavar="NAME")
    archive.add_argument("--yes", action="store_true", help="Confirm the owner approved this exact plan.")
    archive.add_argument("--follow-symlinks", action="store_true", help="Allow symlinks whose target is outside the skill roots.")
    restore = commands.add_parser("restore", parents=[common], help="Move an archived skill back.")
    restore.add_argument("name", metavar="NAME")
    restore.add_argument("--from", dest="source", type=Path, required=True, help="Dated archive folder that holds the skill.")
    return top


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parser().parse_args(argv)
    args.home = (args.home or Path.home()).absolute()
    args.project = (args.project or Path.cwd()).absolute()
    args.archive_root = (args.archive_root or args.home / ".agents" / "skills-archive").absolute()
    try:
        if args.command == "plan":
            return cmd_plan(args)
        if args.command == "archive":
            return cmd_archive(args)
        args.source = args.source.absolute()
        return cmd_restore(args)
    except Refusal as refusal:
        print("refused: %s" % refusal, file=sys.stderr)
        return refusal.code


if __name__ == "__main__":
    sys.exit(main())
