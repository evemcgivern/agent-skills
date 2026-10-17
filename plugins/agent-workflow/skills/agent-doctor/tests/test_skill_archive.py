"""Black-box coverage for scripts/skill_archive.py in temporary folders."""

from __future__ import annotations

import datetime
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "skill_archive.py"


class SkillArchiveTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.home = self.base / "home"
        self.project = self.base / "project"
        self.archive_root = self.home / ".agents" / "skills-archive"
        self.project.mkdir(parents=True)
        self.home.mkdir()
        self.day_dir = self.archive_root / datetime.date.today().isoformat()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def make_skill(self, name: str, root: str = ".agents") -> Path:
        skill = self.home / root / "skills" / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: %s\ndescription: d\n---\n" % name, encoding="utf-8")
        return skill

    def run_archive(self, *args: str) -> subprocess.CompletedProcess[str]:
        command, rest = args[0], args[1:]
        return subprocess.run(
            [sys.executable, str(SCRIPT), command, "--home", str(self.home), "--project", str(self.project), *rest],
            text=True, capture_output=True,
        )

    def snapshot(self) -> list:
        return sorted(str(path.relative_to(self.base)) for path in self.base.rglob("*"))

    def test_plan_prints_moves_and_changes_nothing(self) -> None:
        skill = self.make_skill("alpha-old")
        before = self.snapshot()

        result = self.run_archive("plan", "alpha-old")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(skill), result.stdout)
        self.assertIn(str(self.day_dir / "alpha-old"), result.stdout)
        self.assertIn("restore alpha-old --from", result.stdout)
        self.assertEqual(self.snapshot(), before)

    def test_archive_refuses_without_yes(self) -> None:
        skill = self.make_skill("beta-old")

        result = self.run_archive("archive", "beta-old")

        self.assertEqual(result.returncode, 1)
        self.assertIn("--yes", result.stderr)
        self.assertTrue(skill.is_dir())
        self.assertFalse(self.archive_root.exists())

    def test_archive_and_restore_round_trip(self) -> None:
        skill = self.make_skill("gamma-old")
        (skill / "notes.md").write_text("keep me", encoding="utf-8")

        archived = self.run_archive("archive", "gamma-old", "--yes")

        self.assertEqual(archived.returncode, 0, archived.stderr)
        self.assertFalse(skill.exists())
        self.assertEqual((self.day_dir / "gamma-old" / "notes.md").read_text(encoding="utf-8"), "keep me")
        record = (self.day_dir / "gamma-old.restore.txt").read_text(encoding="utf-8")
        self.assertIn("restore gamma-old --from %s" % self.day_dir, record)

        restored = self.run_archive("restore", "gamma-old", "--from", str(self.day_dir))

        self.assertEqual(restored.returncode, 0, restored.stderr)
        self.assertEqual((skill / "notes.md").read_text(encoding="utf-8"), "keep me")
        self.assertFalse((self.day_dir / "gamma-old").exists())
        self.assertTrue((self.day_dir / "gamma-old.restore.txt").is_file())

    def test_restore_command_in_record_works_verbatim(self) -> None:
        skill = self.make_skill("gamma-verbatim")
        self.run_archive("archive", "gamma-verbatim", "--yes")
        lines = (self.day_dir / "gamma-verbatim.restore.txt").read_text(encoding="utf-8").splitlines()
        command = next(line for line in lines if " restore " in line and not line.startswith("#"))

        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((skill / "SKILL.md").is_file())

    def test_symlinked_skill_moves_the_link_not_the_target(self) -> None:
        real = self.make_skill("delta-old", ".agents")
        link_parent = self.home / ".claude" / "skills"
        link_parent.mkdir(parents=True)
        link = link_parent / "delta-old"
        link.symlink_to(real)

        result = self.run_archive("archive", "delta-old", "--yes")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(real.exists())
        self.assertFalse(link.is_symlink())
        self.assertTrue((self.day_dir / "delta-old").is_dir())
        self.assertFalse((self.day_dir / "delta-old").is_symlink())
        self.assertTrue((self.day_dir / "delta-old~2").is_symlink())

        restored = self.run_archive("restore", "delta-old", "--from", str(self.day_dir))

        self.assertEqual(restored.returncode, 0, restored.stderr)
        self.assertTrue(link.is_symlink())
        self.assertTrue((link / "SKILL.md").is_file())

    def test_symlink_outside_roots_is_refused_unless_follow_symlinks(self) -> None:
        outside = self.base / "elsewhere" / "epsilon-old"
        outside.mkdir(parents=True)
        (outside / "SKILL.md").write_text("---\nname: epsilon-old\ndescription: d\n---\n", encoding="utf-8")
        root = self.home / ".claude" / "skills"
        root.mkdir(parents=True)
        (root / "epsilon-old").symlink_to(outside)

        refused = self.run_archive("archive", "epsilon-old", "--yes")

        self.assertEqual(refused.returncode, 1)
        self.assertIn("outside the skill roots", refused.stderr)
        self.assertTrue((root / "epsilon-old").is_symlink())

        allowed = self.run_archive("archive", "epsilon-old", "--yes", "--follow-symlinks")

        self.assertEqual(allowed.returncode, 0, allowed.stderr)
        self.assertTrue((self.day_dir / "epsilon-old").is_symlink())
        self.assertTrue((outside / "SKILL.md").is_file())  # the target never moves

    def test_refuses_names_that_are_not_plain(self) -> None:
        self.make_skill("zeta-old")
        for bad in ("../zeta-old", "a/b", "..", ".hidden", "zeta..old", ""):
            result = self.run_archive("archive", bad, "--yes")
            self.assertEqual(result.returncode, 1, bad)
            self.assertIn("plain skill name", result.stderr)
        self.assertFalse(self.archive_root.exists())

    def test_refuses_plugin_managed_skills(self) -> None:
        cached = self.home / ".claude" / "plugins" / "cache" / "market" / "toolbelt" / "1.0.0" / "skills" / "eta-tool"
        cached.mkdir(parents=True)
        (cached / "SKILL.md").write_text("---\nname: eta-tool\ndescription: d\n---\n", encoding="utf-8")

        by_prefix = self.run_archive("archive", "toolbelt:eta-tool", "--yes")
        by_name = self.run_archive("plan", "eta-tool")

        for result in (by_prefix, by_name):
            self.assertEqual(result.returncode, 1)
            self.assertIn("plugin", result.stderr)
            self.assertIn("toolbelt", result.stderr)
        self.assertTrue((cached / "SKILL.md").is_file())

    def test_refuses_symlink_into_plugin_folder(self) -> None:
        cached = self.home / ".claude" / "plugins" / "cache" / "m" / "p" / "1" / "skills" / "theta-tool"
        cached.mkdir(parents=True)
        root = self.home / ".claude" / "skills"
        root.mkdir(parents=True)
        (root / "theta-tool").symlink_to(cached)

        result = self.run_archive("archive", "theta-tool", "--yes", "--follow-symlinks")

        self.assertEqual(result.returncode, 1)
        self.assertIn("plugin", result.stderr)

    def test_unknown_skill_exits_not_found(self) -> None:
        result = self.run_archive("plan", "iota-missing")

        self.assertEqual(result.returncode, 3)

    def test_refuses_when_archive_destination_exists(self) -> None:
        skill = self.make_skill("kappa-old")
        (self.day_dir / "kappa-old").mkdir(parents=True)

        result = self.run_archive("archive", "kappa-old", "--yes")

        self.assertEqual(result.returncode, 1)
        self.assertTrue(skill.is_dir())

    def test_restore_refuses_when_original_exists_again(self) -> None:
        self.make_skill("lambda-old")
        self.run_archive("archive", "lambda-old", "--yes")
        self.make_skill("lambda-old")

        result = self.run_archive("restore", "lambda-old", "--from", str(self.day_dir))

        self.assertEqual(result.returncode, 1)
        self.assertTrue((self.day_dir / "lambda-old").is_dir())

    def test_restore_rejects_tampered_record(self) -> None:
        self.make_skill("mu-old")
        self.run_archive("archive", "mu-old", "--yes")
        record = self.day_dir / "mu-old.restore.txt"
        text = record.read_text(encoding="utf-8")
        original = "\t%s\t" % (self.home / ".agents" / "skills" / "mu-old")
        self.assertIn(original, text)
        record.write_text(text.replace(original, "\t%s\t" % (self.base / "evil" / "mu-old")), encoding="utf-8")

        result = self.run_archive("restore", "mu-old", "--from", str(self.day_dir))

        self.assertEqual(result.returncode, 1)
        self.assertFalse((self.base / "evil").exists())

    def test_restore_rejects_record_that_pulls_from_outside_the_archive(self) -> None:
        self.make_skill("mu-pull")
        self.run_archive("archive", "mu-pull", "--yes")
        record = self.day_dir / "mu-pull.restore.txt"
        private = self.home / "private-stuff"
        private.mkdir()
        text = record.read_text(encoding="utf-8")
        record.write_text(text.replace(str(self.day_dir / "mu-pull") + "\t", str(private) + "\t"), encoding="utf-8")

        result = self.run_archive("restore", "mu-pull", "--from", str(self.day_dir))

        self.assertEqual(result.returncode, 1)
        self.assertTrue(private.is_dir())
        self.assertFalse((self.home / ".agents" / "skills" / "mu-pull").exists())

    def test_never_deletes_files(self) -> None:
        skill = self.make_skill("nu-old")
        (skill / "a.txt").write_text("a", encoding="utf-8")
        files_before = sorted(path.name for path in self.base.rglob("*") if path.is_file())

        self.run_archive("archive", "nu-old", "--yes")
        self.run_archive("restore", "nu-old", "--from", str(self.day_dir))

        files_after = sorted(path.name for path in self.base.rglob("*") if path.is_file())
        self.assertEqual(sorted(set(files_after) - {"nu-old.restore.txt"}), files_before)

    def test_project_skills_are_found(self) -> None:
        skill = self.project / ".claude" / "skills" / "xi-local"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: xi-local\ndescription: d\n---\n", encoding="utf-8")

        result = self.run_archive("archive", "xi-local", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        restored = self.run_archive("restore", "xi-local", "--from", str(self.day_dir))

        self.assertEqual(restored.returncode, 0, restored.stderr)
        self.assertTrue((skill / "SKILL.md").is_file())

    def test_bad_command_line_exits_two(self) -> None:
        result = subprocess.run([sys.executable, str(SCRIPT), "explode"], text=True, capture_output=True)

        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
