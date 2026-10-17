"""Black-box coverage for `agent_doctor.py --usage` with synthetic session logs."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "agent_doctor.py"
DAY = 86_400
SECRET = "CONFIDENTIAL-zx81-quokka-marker"
PROJECT_SECRET = "project-name-walrus-42"


def iso(days_ago: float) -> str:
    return datetime.fromtimestamp(time.time() - days_ago * DAY, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def skill_call(name: str, days_ago: float, call_id: str) -> dict:
    return {
        "type": "assistant", "timestamp": iso(days_ago), "uuid": "u-" + call_id,
        "cwd": "/work/" + PROJECT_SECRET,
        "message": {"role": "assistant", "content": [
            {"type": "text", "text": "thinking about " + SECRET},
            {"type": "tool_use", "id": call_id, "name": "Skill", "input": {"skill": name, "args": SECRET}},
        ]},
    }


def slash_command(name: str, days_ago: float, uuid: str) -> dict:
    return {
        "type": "user", "timestamp": iso(days_ago), "uuid": uuid,
        "message": {"role": "user", "content": "<command-name>/%s</command-name>\n<command-args>%s</command-args>" % (name, SECRET)},
    }


class UsageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.home = self.base / "home"
        self.project = self.base / PROJECT_SECRET
        self.home.mkdir()
        self.project.mkdir()
        self.claude_logs = self.home / ".claude" / "projects" / ("-work-" + PROJECT_SECRET)
        self.codex_logs = self.home / ".codex" / "sessions" / "2026" / "01"
        self.claude_logs.mkdir(parents=True)
        self.codex_logs.mkdir(parents=True)
        self.counter = 0

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def make_skill(self, name: str, age_days: float = 400, root: str = ".agents", body: str = "") -> Path:
        skill = self.home / root / "skills" / name
        skill.mkdir(parents=True)
        skill_md = skill / "SKILL.md"
        skill_md.write_text("---\nname: %s\ndescription: test skill %s\n---\n%s\n" % (name, name, body), encoding="utf-8")
        stamp = time.time() - age_days * DAY
        os.utime(skill_md, (stamp, stamp))
        os.utime(skill, (stamp, stamp))
        return skill

    def write_log(self, folder: Path, entries: list, age_days: float = 0, raw_lines: tuple = ()) -> Path:
        self.counter += 1
        path = folder / ("session-%d.jsonl" % self.counter)
        lines = [json.dumps(entry, separators=(",", ":")) for entry in entries] + list(raw_lines)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        stamp = time.time() - age_days * DAY
        os.utime(path, (stamp, stamp))
        return path

    def old_anchor(self, days: float = 200) -> None:
        """An old, untouched log so the logs cover the whole window."""
        self.write_log(self.claude_logs, [{"type": "summary", "timestamp": iso(days)}], age_days=days)

    def run_usage(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--usage", "--home", str(self.home), "--project", str(self.project), *args],
            text=True, capture_output=True,
        )

    def report(self, *args: str) -> dict:
        result = self.run_usage("--format", "json", *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def row(self, report: dict, name: str) -> dict:
        return next(item for item in report["skills"] if item["skill"] == name)

    def test_counts_skill_tool_calls_including_plugin_form(self) -> None:
        self.make_skill("alpha-widget")
        self.old_anchor()
        self.write_log(self.claude_logs, [
            skill_call("alpha-widget", 1, "t1"),
            skill_call("alpha-widget", 2, "t2"),
            skill_call("someplugin:alpha-widget", 3, "t3"),
            skill_call("alpha-widget", 1, "t1"),  # the same call copied into a resumed session
        ])

        row = self.row(self.report(), "alpha-widget")

        self.assertEqual(row["uses"], 3)
        self.assertEqual(row["uses_claude"], 3)
        self.assertEqual(row["verdict"], "ACTIVE")
        self.assertEqual(row["last_used"], iso(1)[:10])

    def test_ignores_tool_definitions_and_replayed_request_blobs(self) -> None:
        self.make_skill("beta-gizmo")
        self.old_anchor()
        definition = {"type": "api-request-shape", "timestamp": iso(1), "shape": {"tools": [{"name": "Skill"}]}}
        blob = dict(skill_call("beta-gizmo", 1, "t9"), type="api-request-blob")
        self.write_log(self.claude_logs, [definition, blob])

        self.assertEqual(self.row(self.report(), "beta-gizmo")["uses"], 0)

    def test_counts_slash_commands_from_user_messages_only(self) -> None:
        self.make_skill("gamma-tool")
        self.old_anchor()
        quoted = {"type": "assistant", "timestamp": iso(1), "message": {"role": "assistant", "content": [
            {"type": "text", "text": "<command-name>/gamma-tool</command-name>"}]}}
        tool_result = {"type": "user", "timestamp": iso(1), "uuid": "r1", "message": {"role": "user", "content": [
            {"type": "tool_result", "content": "<command-name>/gamma-tool</command-name>"}]}}
        self.write_log(self.claude_logs, [
            slash_command("gamma-tool", 1, "c1"), slash_command("gamma-tool", 5, "c2"), quoted, tool_result,
        ])

        self.assertEqual(self.row(self.report(), "gamma-tool")["uses"], 2)

    def test_skips_malformed_lines(self) -> None:
        self.make_skill("delta-kit")
        self.old_anchor()
        self.write_log(
            self.claude_logs, [skill_call("delta-kit", 1, "t1")],
            raw_lines=('{"name":"Skill", broken', "<command-name>/delta-kit</command-name> not json"),
        )

        report = self.report()

        self.assertEqual(self.row(report, "delta-kit")["uses"], 1)
        self.assertEqual(report["logs"]["claude"]["malformed_lines"], 2)

    def test_window_filters_by_entry_timestamp_and_file_mtime(self) -> None:
        self.make_skill("epsilon-aid")
        self.old_anchor()
        # Recent file, but one entry is older than the window.
        self.write_log(self.claude_logs, [skill_call("epsilon-aid", 2, "t1"), skill_call("epsilon-aid", 50, "t2")])
        # Old file is skipped entirely by its modification time.
        self.write_log(self.claude_logs, [skill_call("epsilon-aid", 5, "t3")], age_days=40)

        report = self.report("--days", "30")

        self.assertEqual(self.row(report, "epsilon-aid")["uses"], 1)
        self.assertEqual(report["logs"]["claude"]["files_skipped"], 2)
        self.assertEqual(report["logs"]["claude"]["files_read"], 1)

    def test_entry_without_timestamp_uses_file_mtime(self) -> None:
        self.make_skill("zeta-pal")
        self.old_anchor()
        entry = skill_call("zeta-pal", 1, "t1")
        del entry["timestamp"]
        self.write_log(self.claude_logs, [entry], age_days=3)

        row = self.row(self.report(), "zeta-pal")

        self.assertEqual(row["uses"], 1)
        self.assertEqual(row["last_used"], iso(3)[:10])

    def test_verdict_thresholds_and_new_grace_period(self) -> None:
        for name in ("busy-one", "rare-one", "quiet-one"):
            self.make_skill(name, age_days=400)
        self.make_skill("fresh-one", age_days=5)
        self.old_anchor()
        calls = [skill_call("busy-one", 1, "b%d" % index) for index in range(4)]
        calls += [skill_call("rare-one", 1, "r1"), skill_call("rare-one", 2, "r2")]
        self.write_log(self.claude_logs, calls)

        report = self.report("--min-uses", "3")
        verdicts = {item["skill"]: item["verdict"] for item in report["skills"]}

        self.assertEqual(verdicts, {
            "busy-one": "ACTIVE", "rare-one": "RARELY USED", "quiet-one": "NO CALLS FOUND", "fresh-one": "NEW",
        })
        self.assertEqual([item["skill"] for item in report["skills"]], ["quiet-one", "rare-one", "fresh-one", "busy-one"])
        self.assertEqual(report["totals"]["verdicts"]["NO CALLS FOUND"], 1)
        self.assertTrue(report["window_covered"])

    def test_unknown_window_when_logs_are_younger_than_the_window(self) -> None:
        self.make_skill("eta-thing", age_days=400)
        self.write_log(self.claude_logs, [{"type": "summary", "timestamp": iso(20)}], age_days=1)

        report = self.report("--days", "90")
        text = self.run_usage("--days", "90").stdout

        self.assertEqual(self.row(report, "eta-thing")["verdict"], "UNKNOWN-WINDOW")
        self.assertFalse(report["window_covered"])
        self.assertEqual(report["coverage_days"], 20)
        self.assertIn("Logs only reach back 20 days", text)
        self.assertNotIn("unused", text.lower())
        self.assertIn("No calls found in the logs", text)

    def test_no_logs_at_all_is_unknown_window(self) -> None:
        self.make_skill("theta-bit", age_days=400)

        report = self.report()

        self.assertIsNone(report["coverage_days"])
        self.assertEqual(self.row(report, "theta-bit")["verdict"], "UNKNOWN-WINDOW")

    def test_codex_best_effort_heuristic(self) -> None:
        self.make_skill("iota-helper")
        self.make_skill("kappa-helper")
        self.old_anchor()
        read = {"type": "response_item", "timestamp": iso(1), "payload": {
            "type": "custom_tool_call", "call_id": "x1", "name": "exec",
            "input": "cat ~/.agents/skills/iota-helper/SKILL.md # " + SECRET}}
        mention = {"type": "response_item", "timestamp": iso(2), "payload": {
            "type": "message", "role": "user", "content": [{"type": "input_text", "text": "please run $kappa-helper on " + SECRET}]}}
        injected = {"type": "response_item", "timestamp": iso(2), "payload": {
            "type": "message", "role": "user", "content": [{"type": "input_text", "text": "# AGENTS.md instructions\nalways use $kappa-helper"}]}}
        developer = {"type": "response_item", "timestamp": iso(2), "payload": {
            "type": "message", "role": "developer", "content": [{"type": "input_text", "text": "skills/kappa-helper/SKILL.md $kappa-helper"}]}}
        self.write_log(self.codex_logs, [read, read, mention, injected, developer])

        report = self.report()

        self.assertEqual(self.row(report, "iota-helper")["uses_codex_best_effort"], 1)
        self.assertEqual(self.row(report, "kappa-helper")["uses_codex_best_effort"], 1)
        self.assertIn("best effort", report["logs"]["codex"]["method"])
        self.assertIn("Codex (best effort)", self.run_usage().stdout)

    def test_odd_json_types_do_not_crash(self) -> None:
        self.make_skill("upsilon-odd")
        self.old_anchor()
        weird_id = skill_call("upsilon-odd", 1, "w1")
        weird_id["message"]["content"][1]["id"] = ["not", "hashable"]
        weird_uuid = dict(slash_command("upsilon-odd", 1, "w2"), uuid={"a": 1})
        self.write_log(self.claude_logs, [weird_id, weird_uuid, {"type": "assistant", "message": "text"}],
                       raw_lines=("[1, 2]", '"<command-name>"'))
        self.write_log(self.codex_logs, [
            {"type": "response_item", "payload": {"type": "message", "role": "user", "content": 7, "x": "$a"}},
            {"type": "response_item", "payload": {"type": "custom_tool_call", "call_id": {"x": 1}, "input": "skills/upsilon-odd/SKILL.md"}},
        ])
        (self.home / ".claude" / "plugins").mkdir(parents=True)
        (self.home / ".claude" / "plugins" / "installed_plugins.json").write_text('{"plugins": []}', encoding="utf-8")

        row = self.row(self.report(), "upsilon-odd")

        self.assertEqual((row["uses_claude"], row["uses_codex_best_effort"]), (2, 1))

    def test_lock_file_source_and_age(self) -> None:
        self.make_skill("lambda-pack")
        self.make_skill("mu-pack", age_days=400)
        self.old_anchor()
        lock = {"version": 3, "skills": {
            "lambda-pack": {"source": "example-org/skills", "installedAt": iso(300), "updatedAt": iso(120)},
            "mu-pack": {"source": "example-org/skills", "installedAt": iso(10), "updatedAt": iso(10)},
        }}
        (self.home / ".agents" / ".skill-lock.json").write_text(json.dumps(lock), encoding="utf-8")

        report = self.report()
        lam = self.row(report, "lambda-pack")

        self.assertEqual(lam["source"], "example-org/skills")
        self.assertIn("installed from example-org/skills, last updated 120 days ago: check upstream", lam["notes"])
        self.assertEqual(self.row(report, "mu-pack")["verdict"], "NEW")

    def test_freshness_notes_for_links_and_missing_skills(self) -> None:
        self.make_skill("nu-docs", body="[guide](references/missing.md)\nThen use the `xi-absent` skill and `$nu-docs`.")
        self.old_anchor()

        text = self.run_usage().stdout
        notes = self.row(self.report(), "nu-docs")["notes"]

        self.assertIn("1 broken relative link(s) or missing referenced file(s)", notes)
        self.assertIn("mentions skill(s) not installed: xi-absent", notes)
        self.assertIn("| advisory | nu-docs |", text)

    def test_exclude_option_and_ignore_file(self) -> None:
        for name in ("omicron-a", "omicron-b", "omicron-c"):
            self.make_skill(name)
        self.old_anchor()
        (self.home / ".agent-doctor-ignore").write_text("# kept on purpose\nomicron-b\n", encoding="utf-8")

        report = self.report("--exclude", "omicron-a")

        self.assertEqual([item["skill"] for item in report["skills"]], ["omicron-c"])
        self.assertEqual(sorted(report["excluded"]), ["omicron-a", "omicron-b"])
        self.assertEqual(report["totals"]["excluded"], 2)

    def test_plugin_skills_are_named_with_their_plugin(self) -> None:
        install = self.home / ".claude" / "plugins" / "cache" / "market" / "toolbelt" / "1.0.0"
        (install / "skills" / "pi-skill").mkdir(parents=True)
        (install / "skills" / "pi-skill" / "SKILL.md").write_text("---\nname: pi-skill\ndescription: d\n---\n", encoding="utf-8")
        registry = {"version": 2, "plugins": {"toolbelt@market": [{"installPath": str(install), "installedAt": iso(300)}]}}
        (self.home / ".claude" / "plugins" / "installed_plugins.json").write_text(json.dumps(registry), encoding="utf-8")
        self.old_anchor()
        self.write_log(self.claude_logs, [skill_call("toolbelt:pi-skill", 1, "p1")])

        row = self.row(self.report(), "toolbelt:pi-skill")

        self.assertEqual((row["uses"], row["source"], row["scope"]), (1, "plugin", "plugin"))

    def test_json_output_shape(self) -> None:
        self.make_skill("rho-shape")
        self.old_anchor()

        report = self.report()

        self.assertEqual(set(report), {
            "mode", "window_days", "min_uses", "coverage_days", "window_covered", "logs", "totals", "excluded", "skills",
        })
        self.assertEqual(report["mode"], "usage")
        self.assertEqual(set(report["logs"]["claude"]), {
            "files_found", "files_read", "files_skipped", "malformed_lines", "reaches_back_days", "method",
        })
        self.assertEqual(set(self.row(report, "rho-shape")), {
            "skill", "scope", "uses", "uses_claude", "uses_codex_best_effort", "last_used",
            "skill_md_changed_days", "installed_days", "source", "verdict", "notes",
        })

    def test_never_prints_conversation_text_paths_or_project_names(self) -> None:
        self.make_skill("sigma-safe")
        self.old_anchor()
        self.write_log(self.claude_logs, [skill_call("sigma-safe", 1, "s1"), slash_command("sigma-safe", 1, "s2")])
        self.write_log(self.codex_logs, [{"type": "response_item", "timestamp": iso(1), "payload": {
            "type": "message", "role": "user", "content": [{"type": "input_text", "text": "$sigma-safe " + SECRET}]}}])

        outputs = []
        for fmt in ("text", "json", "markdown"):
            result = self.run_usage("--format", fmt)
            self.assertEqual(result.returncode, 0, result.stderr)
            outputs.append(result.stdout + result.stderr)
        combined = "\n".join(outputs)

        self.assertNotIn(SECRET, combined)
        self.assertNotIn(PROJECT_SECRET, combined)
        self.assertNotIn(".jsonl", combined)
        self.assertNotIn(str(self.home), combined)

    def test_does_not_write_anything(self) -> None:
        self.make_skill("tau-still")
        self.old_anchor()
        before = sorted((path, path.stat().st_mtime) for path in self.base.rglob("*"))

        self.report()

        after = sorted((path, path.stat().st_mtime) for path in self.base.rglob("*"))
        self.assertEqual(after, before)

    def test_rejects_bad_window(self) -> None:
        result = self.run_usage("--days", "0")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--days", result.stderr)


if __name__ == "__main__":
    unittest.main()
