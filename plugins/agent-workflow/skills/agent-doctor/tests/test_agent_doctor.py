"""Black-box coverage for the agent-doctor CLI."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "agent_doctor.py"


class AgentDoctorCliTests(unittest.TestCase):
    def run_doctor(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args], text=True, capture_output=True
        )

    def json_report(self, project: Path, home: Path, *args: str) -> dict:
        home.mkdir(exist_ok=True)
        result = self.run_doctor(
            "--project", str(project), "--home", str(home), "--format", "json", *args
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def make_skill(self, root: Path, folder: str, text: str) -> Path:
        skill = root / folder
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(text, encoding="utf-8")
        return skill

    def codes(self, report: dict) -> set[str]:
        return {finding["code"] for finding in report["findings"]}

    def test_project_argument_is_required(self) -> None:
        result = self.run_doctor()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--project", result.stderr)

    def test_reports_broken_relative_markdown_reference_with_line(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            self.make_skill(
                root,
                "broken",
                "---\nname: broken\ndescription: broken reference\n---\n[missing](docs/nope.md)\n",
            )

            report = self.json_report(project, home, "--skill-root", str(root))

            finding = next(item for item in report["findings"] if item["code"] == "broken_markdown_reference")
            self.assertEqual(finding["line"], 5)
            self.assertNotIn("missing](", json.dumps(report))

    def test_allows_existing_sibling_reference_and_skips_fenced_templates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            (root / "README.md").parent.mkdir(parents=True)
            (root / "README.md").write_text("reference", encoding="utf-8")
            self.make_skill(
                root,
                "linked",
                "---\nname: linked\ndescription: links\n---\n[pack](../README.md)\n```md\n[template](missing.md)\n```\n",
            )

            report = self.json_report(project, home, "--skill-root", str(root))

            self.assertNotIn("broken_markdown_reference", self.codes(report))

    def test_allows_namespaced_skills_with_same_local_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            one, two = base / "one", base / "two"
            self.make_skill(one, "check", "---\nname: alpha:check\ndescription: alpha\n---\n")
            self.make_skill(two, "check", "---\nname: beta:check\ndescription: beta\n---\n")

            report = self.json_report(project, home, "--skill-root", str(one), "--skill-root", str(two))

            self.assertNotIn("duplicate_skill_name", self.codes(report))

    def test_plugin_skill_roots_namespace_same_declared_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            alpha = base / "plugins" / "alpha" / "skills"
            beta = base / "plugins" / "beta" / "skills"
            self.make_skill(alpha, "check", "---\nname: check\ndescription: alpha\n---\n")
            self.make_skill(beta, "check", "---\nname: check\ndescription: beta\n---\n")

            report = self.json_report(project, home, "--skill-root", str(alpha), "--skill-root", str(beta))

            self.assertNotIn("duplicate_skill_name", self.codes(report))

    def test_reports_different_flat_skills_with_same_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            one, two = base / "one", base / "two"
            self.make_skill(one, "check", "---\nname: check\ndescription: one\n---\n")
            self.make_skill(two, "check", "---\nname: check\ndescription: two\n---\n")

            report = self.json_report(project, home, "--skill-root", str(one), "--skill-root", str(two))

            self.assertIn("duplicate_skill_name", self.codes(report))

    def test_deduplicates_same_canonical_skill_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            self.make_skill(root, "check", "---\nname: check\ndescription: check\n---\n")
            alias = base / "alias"
            alias.symlink_to(root, target_is_directory=True)

            report = self.json_report(project, home, "--skill-root", str(root), "--skill-root", str(alias))

            skills = [source for source in report["sources"] if source["kind"] == "skill"]
            self.assertEqual(len(skills), 1)
            self.assertGreaterEqual(len(skills[0]["aliases"]), 2)
            self.assertNotIn("duplicate_skill_name", self.codes(report))

    def test_reports_and_skips_symlink_that_escapes_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, outside = base / "project", base / "home", base / "outside"
            project.mkdir()
            outside.mkdir()
            (outside / "AGENTS.md").write_text("secret material", encoding="utf-8")
            (project / "AGENTS.md").symlink_to(outside / "AGENTS.md")

            report = self.json_report(project, home)

            self.assertIn("symlink_outside_allowed_root", self.codes(report))
            self.assertNotIn("secret material", json.dumps(report))

    def test_skips_instruction_symlink_into_project_credential_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            credential = project / ".ssh" / "credentials"
            credential.parent.mkdir()
            credential.write_text("TOP_SECRET_TOKEN_123", encoding="utf-8")
            (project / "AGENTS.md").symlink_to(credential)

            report = self.json_report(project, home)

            self.assertFalse(any(item["path"] == str(credential) for item in report["sources"]))
            self.assertIn("sensitive_source_skipped", self.codes(report))
            self.assertNotIn("TOP_SECRET_TOKEN_123", json.dumps(report))

    def test_skips_instruction_symlink_to_dotenv_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            dotenv = project / ".env"
            dotenv.write_text("TOP_SECRET_TOKEN_123", encoding="utf-8")
            (project / "AGENTS.md").symlink_to(dotenv)

            report = self.json_report(project, home)

            self.assertFalse(any(item["path"] == str(dotenv) for item in report["sources"]))
            self.assertIn("sensitive_source_skipped", self.codes(report))
            self.assertNotIn("TOP_SECRET_TOKEN_123", json.dumps(report))

    def test_does_not_emit_secret_file_contents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            secret = "TOP_SECRET_TOKEN_123"
            (project / "AGENTS.md").write_text(secret, encoding="utf-8")

            report = self.json_report(project, home)

            self.assertNotIn(secret, json.dumps(report))
            self.assertTrue(any(source["kind"] == "instruction" for source in report["sources"]))

    def test_json_and_markdown_report_same_finding_codes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            self.make_skill(root, "bad", "---\nname: bad\ndescription: bad\n---\n[bad](no.md)\n")

            report = self.json_report(project, home, "--skill-root", str(root))
            markdown = self.run_doctor(
                "--project", str(project), "--home", str(home), "--skill-root", str(root), "--format", "markdown"
            )

            self.assertEqual(markdown.returncode, 0, markdown.stderr)
            for code in self.codes(report):
                self.assertIn(code, markdown.stdout)

    def test_model_role_mismatch_is_advisory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            self.make_skill(
                root,
                "role",
                "---\nname: role\ndescription: role check\n---\nYou are Fable 5.\n",
            )

            report = self.json_report(project, home, "--skill-root", str(root), "--model", "builder")

            finding = next(item for item in report["findings"] if item["code"] == "model_role_mismatch")
            self.assertEqual(finding["severity"], "advisory")
            self.assertEqual(finding["line"], 5)

    def test_does_not_treat_generic_roles_or_code_examples_as_model_identities(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            self.make_skill(
                root,
                "role",
                "---\nname: role\ndescription: role check\nmodel: reviewer\n---\n```text\nYou are Fable 5.\n```\n",
            )

            report = self.json_report(project, home, "--skill-root", str(root), "--model", "builder")

            self.assertNotIn("model_role_mismatch", self.codes(report))

    def test_matches_bounded_claude_identity_without_trailing_prose(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            self.make_skill(
                root,
                "role",
                "---\nname: role\ndescription: role check\n---\nYou are Claude and must inspect files.\n",
            )

            report = self.json_report(project, home, "--skill-root", str(root), "--model", "Claude")

            self.assertNotIn("model_role_mismatch", self.codes(report))

    def test_discovers_project_local_agent_skill_folder(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            self.make_skill(
                project / ".agents" / "skills",
                "local",
                "---\nname: local\ndescription: project local\n---\n",
            )

            report = self.json_report(project, home)

            self.assertTrue(any(source.get("skill_name") == "local" for source in report["sources"]))

    def test_discovers_project_local_gemini_skill_folder(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            self.make_skill(
                project / ".gemini" / "skills",
                "local",
                "---\nname: local\ndescription: project local\n---\n",
            )

            report = self.json_report(project, home)

            self.assertTrue(any(source.get("skill_name") == "local" for source in report["sources"]))

    def test_discovers_project_local_github_skill_folder(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            self.make_skill(
                project / ".github" / "skills",
                "local",
                "---\nname: local\ndescription: project local\n---\n",
            )

            report = self.json_report(project, home)

            self.assertTrue(any(source.get("skill_name") == "local" for source in report["sources"]))

    def test_discovers_global_gemini_skill_folder(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            self.make_skill(
                home / ".gemini" / "skills",
                "personal",
                "---\nname: personal\ndescription: global gemini\n---\n",
            )

            report = self.json_report(project, home)

            self.assertTrue(any(source.get("skill_name") == "personal" for source in report["sources"]))

    def test_reads_nested_and_global_gemini_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            (project / "GEMINI.md").write_text("# Project\n", encoding="utf-8")
            (home / ".gemini").mkdir(parents=True)
            (home / ".gemini" / "GEMINI.md").write_text("# Global\n", encoding="utf-8")

            report = self.json_report(project, home)

            paths = {
                Path(source["path"]).resolve()
                for source in report["sources"] if source["kind"] == "instruction"
            }
            self.assertIn((project / "GEMINI.md").resolve(), paths)
            self.assertIn((home / ".gemini" / "GEMINI.md").resolve(), paths)

    def test_reports_skill_once_through_symlinked_cursor_folder(self) -> None:
        # The Skills CLI installs one canonical copy and symlinks each agent's folder to it.
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            self.make_skill(
                project / ".agents" / "skills",
                "shared",
                "---\nname: shared\ndescription: shared\n---\n",
            )
            (project / ".cursor").mkdir()
            (project / ".cursor" / "skills").symlink_to(
                project / ".agents" / "skills", target_is_directory=True,
            )

            report = self.json_report(project, home)

            skills = [item for item in report["sources"] if item["kind"] == "skill"]
            self.assertEqual(len(skills), 1)
            self.assertGreaterEqual(len(skills[0]["aliases"]), 2)
            self.assertNotIn("duplicate_skill_name", self.codes(report))
            self.assertNotIn("symlink_outside_allowed_root", self.codes(report))

    def test_deduplicates_global_claude_alias_to_agents_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            self.make_skill(home / ".agents" / "skills", "shared", "---\nname: shared\ndescription: shared\n---\n")
            (home / ".claude").symlink_to(home / ".agents", target_is_directory=True)

            report = self.json_report(project, home)

            skills = [source for source in report["sources"] if source["kind"] == "skill"]
            self.assertEqual(len(skills), 1)
            self.assertGreaterEqual(len(skills[0]["aliases"]), 2)

    def test_deduplicates_per_skill_claude_alias_to_agents_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            source = self.make_skill(
                home / ".agents" / "skills",
                "sample-check",
                "---\nname: sample-check\ndescription: shared\n---\n",
            )
            claude_skills = home / ".claude" / "skills"
            claude_skills.mkdir(parents=True)
            (claude_skills / "sample-check").symlink_to(source, target_is_directory=True)

            report = self.json_report(project, home)

            skills = [source for source in report["sources"] if source["kind"] == "skill"]
            self.assertEqual(len(skills), 1)
            self.assertGreaterEqual(len(skills[0]["aliases"]), 2)
            self.assertNotIn("symlink_outside_allowed_root", self.codes(report))

    def test_deduplicates_project_per_skill_claude_alias_to_agents_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            source = self.make_skill(
                project / ".agents" / "skills",
                "sample-check",
                "---\nname: sample-check\ndescription: shared\n---\n",
            )
            claude_skills = project / ".claude" / "skills"
            claude_skills.mkdir(parents=True)
            (claude_skills / "sample-check").symlink_to(source, target_is_directory=True)

            report = self.json_report(project, home)

            skills = [item for item in report["sources"] if item["kind"] == "skill"]
            self.assertEqual(len(skills), 1)
            self.assertGreaterEqual(len(skills[0]["aliases"]), 2)
            self.assertNotIn("symlink_outside_allowed_root", self.codes(report))

    def test_allows_reverse_global_native_root_aliases(self) -> None:
        for alias_name, native_name in ((".agents", ".claude"), (".codex", ".agents")):
            with self.subTest(alias_name=alias_name), tempfile.TemporaryDirectory() as directory:
                base = Path(directory)
                project, home = base / "project", base / "home"
                project.mkdir()
                self.make_skill(
                    home / native_name / "skills",
                    "shared",
                    "---\nname: shared\ndescription: shared\n---\n",
                )
                home.mkdir(exist_ok=True)
                (home / alias_name).symlink_to(home / native_name, target_is_directory=True)

                report = self.json_report(project, home)

                skills = [item for item in report["sources"] if item["kind"] == "skill"]
                self.assertEqual(len(skills), 1)
                self.assertGreaterEqual(len(skills[0]["aliases"]), 2)
                self.assertNotIn("symlink_outside_allowed_root", self.codes(report))

    def test_skips_global_claude_alias_outside_agent_roots(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, outside = base / "project", base / "home", base / "outside"
            project.mkdir()
            home.mkdir()
            self.make_skill(
                outside / "skills",
                "secret",
                "---\nname: secret\ndescription: TOP_SECRET_TOKEN_123\n---\n",
            )
            (home / ".claude").symlink_to(outside, target_is_directory=True)

            report = self.json_report(project, home)

            self.assertIn("symlink_outside_allowed_root", self.codes(report))
            self.assertNotIn("TOP_SECRET_TOKEN_123", json.dumps(report))

    def test_scan_limits_are_reported_when_file_cap_is_hit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            for index in range(140):
                folder = project / f"area-{index}"
                folder.mkdir()
                (folder / "AGENTS.md").write_text("x", encoding="utf-8")

            report = self.json_report(project, home, "--max-files", "128")

            self.assertIn("scan_limit_reached", self.codes(report))

    def test_skips_hidden_credential_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            secret = "TOP_SECRET_TOKEN_123"
            credential_dir = project / ".ssh"
            credential_dir.mkdir()
            (credential_dir / "AGENTS.md").write_text(secret, encoding="utf-8")

            report = self.json_report(project, home)

            self.assertFalse(any(source["path"].endswith(".ssh/AGENTS.md") for source in report["sources"]))
            self.assertNotIn(secret, json.dumps(report))

    def test_directory_limit_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            for index in range(10):
                (project / f"area-{index}").mkdir()

            report = self.json_report(project, home, "--max-directories", "4")

            self.assertIn("scan_limit_reached", self.codes(report))

    def test_limit_still_checks_discovered_skills_and_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            for index in range(10):
                (project / f"area-{index}").mkdir()
            self.make_skill(root, "a", "---\nname: same\ndescription: one\n---\n[missing](nope.md)\n")
            self.make_skill(root, "b", "---\nname: same\ndescription: two\n---\n")

            report = self.json_report(
                project, home, "--skill-root", str(root), "--max-directories", "4"
            )

            codes = self.codes(report)
            self.assertIn("scan_limit_reached", codes)
            self.assertIn("broken_markdown_reference", codes)
            self.assertIn("duplicate_skill_name", codes)

    def test_byte_limit_still_reports_duplicates_among_read_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            self.make_skill(root, "a", "---\nname: same\ndescription: one\n---\n")
            self.make_skill(root, "b", "---\nname: same\ndescription: two\n---\n")
            self.make_skill(root, "c", "---\nname: big\ndescription: big\n---\n" + "x" * 500)

            report = self.json_report(
                project, home, "--skill-root", str(root), "--max-bytes", "200"
            )

            codes = self.codes(report)
            self.assertIn("scan_limit_reached", codes)
            self.assertIn("duplicate_skill_name", codes)

    def test_uri_scheme_and_titled_links_are_not_broken_references(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            skill = self.make_skill(
                root,
                "links",
                "---\nname: links\ndescription: links\n---\n"
                "[mail](mailto:someone@example.com)\n"
                "[tel](tel:+15555550100)\n"
                "[readme](README.md \"Read me\")\n"
                "[angle](<README.md>)\n",
            )
            (skill / "README.md").write_text("ok", encoding="utf-8")

            report = self.json_report(project, home, "--skill-root", str(root))

            self.assertNotIn("broken_markdown_reference", self.codes(report))

    def test_titled_link_to_missing_file_is_still_broken(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            self.make_skill(
                root, "links", "---\nname: links\ndescription: links\n---\n[gone](gone.md \"Gone\")\n"
            )

            report = self.json_report(project, home, "--skill-root", str(root))

            self.assertIn("broken_markdown_reference", self.codes(report))

    def test_multiline_yaml_descriptions_are_metadata(self) -> None:
        cases = {
            "folded": "description: >\n  Folded text\n  continues here.\n",
            "literal": "description: |-\n  Literal text\n",
            "plain": "description:\n  Plain text on the next line\n",
        }
        for folder, description in cases.items():
            with self.subTest(folder=folder), tempfile.TemporaryDirectory() as directory:
                base = Path(directory)
                project, home, root = base / "project", base / "home", base / "skills"
                project.mkdir()
                self.make_skill(root, folder, f"---\nname: {folder}\n{description}---\nBody.\n")

                report = self.json_report(project, home, "--skill-root", str(root))

                self.assertNotIn("missing_skill_metadata", self.codes(report))

    def test_empty_block_description_is_missing_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            self.make_skill(root, "empty", "---\nname: empty\ndescription: >\nmodel: x\n---\n")

            report = self.json_report(project, home, "--skill-root", str(root))

            self.assertIn("missing_skill_metadata", self.codes(report))

    def test_model_id_matches_display_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home, root = base / "project", base / "home", base / "skills"
            project.mkdir()
            self.make_skill(
                root, "role", "---\nname: role\ndescription: role check\n---\nYou are Claude Opus 5.5.\n"
            )

            same = self.json_report(project, home, "--skill-root", str(root), "--model", "claude-opus-5-5")
            other = self.json_report(project, home, "--skill-root", str(root), "--model", "claude-sonnet-5")

            self.assertNotIn("model_role_mismatch", self.codes(same))
            self.assertIn("model_role_mismatch", self.codes(other))

    def test_does_not_write_to_project_or_home(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project, home = base / "project", base / "home"
            project.mkdir()
            home.mkdir()
            before = sorted(path.relative_to(base).as_posix() for path in base.rglob("*") if path.is_file())

            self.json_report(project, home)

            after = sorted(path.relative_to(base).as_posix() for path in base.rglob("*") if path.is_file())
            self.assertEqual(after, before)

    def test_invalid_project_returns_nonzero(self) -> None:
        result = self.run_doctor("--project", "/definitely/not/a/project")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--project", result.stderr)


if __name__ == "__main__":
    unittest.main()
