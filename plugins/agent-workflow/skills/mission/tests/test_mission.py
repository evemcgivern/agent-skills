"""Black-box coverage for the mission continuity CLI."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "mission.py"


class MissionCliTests(unittest.TestCase):
    def run_mission(self, cwd: Path, state_dir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--state-dir", str(state_dir), *args],
            cwd=cwd,
            text=True,
            capture_output=True,
        )

    def success(self, cwd: Path, state_dir: Path, *args: str) -> dict:
        result = self.run_mission(cwd, state_dir, *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def init_repo(self, root: Path) -> Path:
        repo = root / "repo"
        repo.mkdir()
        for args in (("init",), ("config", "user.email", "test@example.invalid"), ("config", "user.name", "Test User")):
            result = subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        (repo / "README.md").write_text("initial\n", encoding="utf-8")
        result = subprocess.run(["git", "add", "README.md"], cwd=repo, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run(["git", "commit", "-m", "initial"], cwd=repo, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return repo

    def create(self, repo: Path, state_dir: Path, mission_id: str = "release-notes") -> dict:
        return self.success(
            repo, state_dir, "create", mission_id,
            "--outcome", "Publish accurate release notes",
            "--constraint", "Do not change source files",
            "--milestone", "draft|Draft notes|Notes name every user-facing change",
            "--milestone", "review|Review notes|A reviewer approves the notes",
            "--next-action", "Draft the release notes",
        )

    def revision(self, repo: Path, state_dir: Path, mission_id: str = "release-notes") -> int:
        return self.success(repo, state_dir, "show", mission_id)["mission"]["revision"]

    def checkpoint(self, repo: Path, state_dir: Path, revision: int, *extra: str) -> dict:
        return self.success(
            repo, state_dir, "checkpoint", "release-notes", "--expected-revision", str(revision),
            "--status", "in_progress", "--next-action", "Review the draft", *extra,
        )

    def test_create_checkpoint_restart_resume_and_complete_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir, evidence_dir = self.init_repo(base), base / "state", base / "evidence"
            evidence_dir.mkdir()
            artifact = evidence_dir / "notes.txt"
            artifact.write_text("release notes\n", encoding="utf-8")

            created = self.create(repo, state_dir)
            self.assertEqual(created["mission"]["status"], "pending")
            revision = created["mission"]["revision"]
            changed = self.checkpoint(repo, state_dir, revision, "--milestone-status", "draft=complete", "--evidence", f"draft={artifact}", "--decision", "Use customer language")
            self.assertEqual(changed["mission"]["milestones"][0]["status"], "complete")
            resumed = self.success(repo, state_dir, "resume", "release-notes")
            self.assertEqual(resumed["next_unfinished"]["id"], "review")
            self.assertFalse(resumed["replay_action"])

            revision = changed["mission"]["revision"]
            registered = self.checkpoint(repo, state_dir, revision, "--milestone-status", "review=complete", "--evidence", f"review={artifact}")
            completed = self.success(
                repo, state_dir, "complete", "release-notes", "--expected-revision", str(registered["mission"]["revision"])
            )
            self.assertEqual(completed["mission"]["status"], "complete")
            self.assertEqual(completed["mission"]["milestones"][0]["evidence"][0]["sha256"], hashlib.sha256(artifact.read_bytes()).hexdigest())

    def test_state_changes_do_not_change_git_and_normal_head_advances_warn(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir = self.init_repo(base), base / "state"
            before = subprocess.run(["git", "status", "--porcelain"], cwd=repo, text=True, capture_output=True).stdout
            self.create(repo, state_dir)
            after = subprocess.run(["git", "status", "--porcelain"], cwd=repo, text=True, capture_output=True).stdout
            self.assertEqual(after, before)

            (repo / "README.md").write_text("advanced\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-m", "advance"], cwd=repo, check=True)
            shown = self.success(repo, state_dir, "show", "release-notes")
            self.assertTrue(shown["head"]["advanced"])
            self.checkpoint(repo, state_dir, self.revision(repo, state_dir))

    def test_stale_revision_and_concurrent_writers_fail_safely(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir = self.init_repo(base), base / "state"
            revision = self.create(repo, state_dir)["mission"]["revision"]
            first = self.checkpoint(repo, state_dir, revision)
            stale = self.run_mission(
                repo, state_dir, "checkpoint", "release-notes", "--expected-revision", str(revision),
                "--status", "in_progress", "--next-action", "Still review",
            )
            self.assertNotEqual(stale.returncode, 0)
            self.assertIn("revision", stale.stderr)

            args = (
                "checkpoint", "release-notes", "--expected-revision", str(first["mission"]["revision"]),
                "--status", "in_progress", "--next-action", "Concurrent review",
            )
            one = subprocess.Popen([sys.executable, str(SCRIPT), "--state-dir", str(state_dir), *args], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            two = subprocess.Popen([sys.executable, str(SCRIPT), "--state-dir", str(state_dir), *args], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            outcomes = [one.communicate(), two.communicate()]
            self.assertEqual(sum(process.returncode == 0 for process in (one, two)), 1, outcomes)

    def test_wrong_worktree_blocks_resume_and_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir = self.init_repo(base), base / "state"
            self.create(repo, state_dir)
            other = base / "other-worktree"
            result = subprocess.run(["git", "worktree", "add", "-b", "other", str(other)], cwd=repo, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            resumed = self.run_mission(other, state_dir, "resume", "release-notes")
            self.assertNotEqual(resumed.returncode, 0)
            self.assertIn("worktree", resumed.stderr)
            mutation = self.run_mission(other, state_dir, "checkpoint", "release-notes", "--expected-revision", "1", "--status", "in_progress", "--next-action", "Wrong place")
            self.assertNotEqual(mutation.returncode, 0)

    def test_rejects_path_traversal_and_state_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir = self.init_repo(base), base / "state"
            invalid = self.run_mission(repo, state_dir, "create", "../escape", "--outcome", "x", "--milestone", "a|b|c", "--next-action", "x")
            self.assertNotEqual(invalid.returncode, 0)
            self.create(repo, state_dir)
            state_file = next(state_dir.rglob("release-notes.json"))
            target = base / "outside.json"
            state_file.unlink()
            state_file.symlink_to(target)
            result = self.run_mission(repo, state_dir, "show", "release-notes")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stderr)
            self.assertFalse(target.exists())

    def test_corrupted_json_is_preserved_and_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir = self.init_repo(base), base / "state"
            self.create(repo, state_dir)
            state_file = next(state_dir.rglob("release-notes.json"))
            bad = "{ definitely not JSON"
            state_file.write_text(bad, encoding="utf-8")
            result = self.run_mission(repo, state_dir, "checkpoint", "release-notes", "--expected-revision", "1", "--status", "in_progress", "--next-action", "Nope")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(state_file.read_text(encoding="utf-8"), bad)

    def test_changed_or_missing_evidence_rejects_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir, evidence_dir = self.init_repo(base), base / "state", base / "evidence"
            evidence_dir.mkdir()
            artifact = evidence_dir / "result.txt"
            artifact.write_text("v1", encoding="utf-8")
            created = self.create(repo, state_dir)
            registered = self.checkpoint(repo, state_dir, created["mission"]["revision"], "--milestone-status", "draft=complete", "--milestone-status", "review=complete", "--evidence", f"draft={artifact}", "--evidence", f"review={artifact}")
            artifact.write_text("v2", encoding="utf-8")
            changed = self.run_mission(repo, state_dir, "complete", "release-notes", "--expected-revision", str(registered["mission"]["revision"]))
            self.assertNotEqual(changed.returncode, 0)
            artifact.unlink()
            missing = self.run_mission(repo, state_dir, "complete", "release-notes", "--expected-revision", str(registered["mission"]["revision"]))
            self.assertNotEqual(missing.returncode, 0)

    def test_symlinked_evidence_swap_to_repo_file_rejects_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir, evidence_dir = self.init_repo(base), base / "state", base / "evidence"
            evidence_dir.mkdir()
            artifact = evidence_dir / "result.txt"
            inside = repo / "README.md"
            artifact.write_bytes(inside.read_bytes())
            created = self.success(
                repo, state_dir, "create", "one-proof",
                "--outcome", "Prove one thing", "--milestone", "proof|Create proof|Proof exists",
                "--next-action", "Create proof",
            )
            checkpointed = self.success(
                repo, state_dir, "checkpoint", "one-proof", "--expected-revision", str(created["mission"]["revision"]),
                "--status", "in_progress", "--next-action", "Complete", "--milestone-status", "proof=complete",
                "--evidence", f"proof={artifact}",
            )
            artifact.unlink()
            artifact.symlink_to(inside)
            completed = self.run_mission(repo, state_dir, "complete", "one-proof", "--expected-revision", str(checkpointed["mission"]["revision"]))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("evidence", completed.stderr)

    def test_changed_evidence_cannot_be_reregistered_by_checkpoint_or_complete(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir, evidence_dir = self.init_repo(base), base / "state", base / "evidence"
            evidence_dir.mkdir()
            artifact = evidence_dir / "result.txt"
            artifact.write_text("v1", encoding="utf-8")
            created = self.success(
                repo, state_dir, "create", "one-proof",
                "--outcome", "Prove one thing", "--milestone", "proof|Create proof|Proof exists",
                "--next-action", "Create proof",
            )
            checkpointed = self.success(
                repo, state_dir, "checkpoint", "one-proof", "--expected-revision", str(created["mission"]["revision"]),
                "--status", "in_progress", "--next-action", "Complete", "--milestone-status", "proof=complete",
                "--evidence", f"proof={artifact}",
            )
            artifact.write_text("v2", encoding="utf-8")
            checkpoint = self.run_mission(
                repo, state_dir, "checkpoint", "one-proof", "--expected-revision", str(checkpointed["mission"]["revision"]),
                "--status", "in_progress", "--next-action", "Retry", "--evidence", f"proof={artifact}",
            )
            self.assertNotEqual(checkpoint.returncode, 0)
            self.assertIn("evidence", checkpoint.stderr)
            complete = self.run_mission(
                repo, state_dir, "complete", "one-proof", "--expected-revision", str(checkpointed["mission"]["revision"]),
                "--evidence", f"proof={artifact}",
            )
            self.assertNotEqual(complete.returncode, 0)
            self.assertIn("evidence", complete.stderr)
            self.assertEqual(self.revision(repo, state_dir, "one-proof"), checkpointed["mission"]["revision"])

    def test_completion_requires_evidence_for_each_completed_milestone(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir, evidence_dir = self.init_repo(base), base / "state", base / "evidence"
            evidence_dir.mkdir()
            artifact = evidence_dir / "proof.txt"
            artifact.write_text("proof", encoding="utf-8")
            created = self.create(repo, state_dir)
            missing = self.run_mission(
                repo, state_dir, "checkpoint", "release-notes", "--expected-revision", str(created["mission"]["revision"]),
                "--status", "in_progress", "--next-action", "Review", "--milestone-status", "draft=complete",
            )
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("evidence", missing.stderr)
            recorded = self.checkpoint(repo, state_dir, created["mission"]["revision"], "--milestone-status", "draft=complete", "--evidence", f"draft={artifact}")
            self.assertEqual(recorded["mission"]["milestones"][0]["evidence"][0]["path"], str(artifact.resolve()))

    def test_milestone_blocked_state_requires_its_own_reason(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir = self.init_repo(base), base / "state"
            created = self.create(repo, state_dir)
            result = self.run_mission(
                repo, state_dir, "checkpoint", "release-notes", "--expected-revision", str(created["mission"]["revision"]),
                "--status", "in_progress", "--next-action", "Investigate", "--milestone-status", "draft=blocked",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("reason", result.stderr)

    def test_resume_never_executes_actions_and_flags_uncertain_states(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir = self.init_repo(base), base / "state"
            created = self.create(repo, state_dir)
            marker = repo / "executed.txt"
            in_progress = self.checkpoint(repo, state_dir, created["mission"]["revision"], "--next-action", f"touch {marker}")
            resumed_in_progress = self.success(repo, state_dir, "resume", "release-notes")
            self.assertFalse(marker.exists())
            self.assertTrue(resumed_in_progress["inspect_first"])
            paused = self.checkpoint(repo, state_dir, in_progress["mission"]["revision"], "--status", "blocked", "--blocked-reason", "Waiting for review", "--next-action", f"touch {marker}")
            # Use the revision returned by the in-progress checkpoint; a stale write must not be retried.
            self.assertEqual(paused["mission"]["revision"], in_progress["mission"]["revision"] + 1)
            resumed = self.success(repo, state_dir, "resume", "release-notes")
            self.assertFalse(marker.exists())
            self.assertTrue(resumed["inspect_first"])
            self.assertIn("Waiting for review", resumed["inspect_first"])
            self.assertEqual(paused["mission"]["status"], "blocked")

    def test_rejects_valid_json_that_breaks_state_schema_without_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir = self.init_repo(base), base / "state"
            self.create(repo, state_dir)
            state_file = next(state_dir.rglob("release-notes.json"))
            original = json.loads(state_file.read_text(encoding="utf-8"))
            for field, value in (("milestones", []), ("history", "not-a-list"), ("status", "surprise"), ("unexpected", "untrusted")):
                damaged = dict(original)
                damaged[field] = value
                bytes_before = json.dumps(damaged, sort_keys=True)
                state_file.write_text(bytes_before, encoding="utf-8")
                result = self.run_mission(repo, state_dir, "checkpoint", "release-notes", "--expected-revision", "1", "--status", "in_progress", "--next-action", "No mutation")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("corrupted", result.stderr)
                self.assertEqual(state_file.read_text(encoding="utf-8"), bytes_before)
            completed_without_evidence = json.loads(json.dumps(original))
            completed_without_evidence["milestones"][0]["status"] = "complete"
            bytes_before = json.dumps(completed_without_evidence, sort_keys=True)
            state_file.write_text(bytes_before, encoding="utf-8")
            result = self.run_mission(repo, state_dir, "checkpoint", "release-notes", "--expected-revision", "1", "--status", "in_progress", "--next-action", "No mutation")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("corrupted", result.stderr)
            self.assertEqual(state_file.read_text(encoding="utf-8"), bytes_before)

    def test_malformed_json_types_and_invalid_utf8_are_concise_and_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir = self.init_repo(base), base / "state"
            self.create(repo, state_dir)
            state_file = next(state_dir.rglob("release-notes.json"))
            original = json.loads(state_file.read_text(encoding="utf-8"))
            malformed = []
            for field, value in (("id", None), ("id", []), ("status", None), ("status", {})):
                damaged = json.loads(json.dumps(original))
                damaged[field] = value
                malformed.append(json.dumps(damaged, sort_keys=True).encode("utf-8"))
            for field, value in (("id", {}), ("status", [])):
                damaged = json.loads(json.dumps(original))
                damaged["milestones"][0][field] = value
                malformed.append(json.dumps(damaged, sort_keys=True).encode("utf-8"))
            damaged = json.loads(json.dumps(original))
            damaged["milestones"][0]["evidence"] = [{"path": [], "sha256": {}}]
            malformed.append(json.dumps(damaged, sort_keys=True).encode("utf-8"))
            for status in ([], {}, None):
                damaged = json.loads(json.dumps(original))
                damaged["history"][0].update(action="checkpoint", status=status)
                malformed.append(json.dumps(damaged, sort_keys=True).encode("utf-8"))
            malformed.append(b"\xff")
            for bytes_before in malformed:
                state_file.write_bytes(bytes_before)
                result = self.run_mission(repo, state_dir, "checkpoint", "release-notes", "--expected-revision", "1", "--status", "in_progress", "--next-action", "No mutation")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("corrupted", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(state_file.read_bytes(), bytes_before)

    def test_rejects_state_inside_repo_and_intermediate_state_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo = self.init_repo(base)
            inside = repo / ".mission-state"
            result = self.run_mission(repo, inside, "create", "release-notes", "--outcome", "x", "--milestone", "draft|Draft|Done", "--next-action", "Draft")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("outside", result.stderr)
            self.assertFalse(inside.exists())

            state_dir, outside = base / "state", base / "outside"
            state_dir.mkdir()
            outside.mkdir()
            (state_dir / "worktrees").symlink_to(outside, target_is_directory=True)
            result = self.run_mission(repo, state_dir, "create", "release-notes", "--outcome", "x", "--milestone", "draft|Draft|Done", "--next-action", "Draft")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stderr)
            self.assertFalse(any(outside.iterdir()))

            symlinked_repo = base / "symlinked-repo"
            symlinked_repo.symlink_to(repo, target_is_directory=True)
            result = self.run_mission(repo, symlinked_repo / ".mission-state", "create", "release-notes", "--outcome", "x", "--milestone", "draft|Draft|Done", "--next-action", "Draft")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("outside", result.stderr)

    @unittest.skipUnless(os.name == "posix", "fcntl locking is POSIX-only")
    def test_os_lock_is_released_after_holder_exits(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            repo, state_dir = self.init_repo(base), base / "state"
            created = self.create(repo, state_dir)
            lock = next(state_dir.rglob("*.lock"))
            holder = subprocess.run(
                [sys.executable, "-c", "import fcntl,sys; f= open(sys.argv[1], 'a+'); fcntl.flock(f, fcntl.LOCK_EX)", str(lock)],
                text=True,
                capture_output=True,
            )
            self.assertEqual(holder.returncode, 0, holder.stderr)
            recovered = self.checkpoint(repo, state_dir, created["mission"]["revision"])
            self.assertEqual(recovered["mission"]["revision"], created["mission"]["revision"] + 1)


if __name__ == "__main__":
    unittest.main()
