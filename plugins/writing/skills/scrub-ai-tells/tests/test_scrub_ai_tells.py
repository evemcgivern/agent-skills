"""Tests for scrub_ai_tells.py. Run: python3 -m unittest discover (from this folder)."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scrub_ai_tells.py"

ZWSP = chr(0x200B)
LDQ, RDQ, RSQ = chr(0x201C), chr(0x201D), chr(0x2019)
ELLIPSIS = chr(0x2026)


def run(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, "-I", str(SCRIPT), *args], capture_output=True
    )


class WriteTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, name: str, text: str) -> Path:
        path = self.dir / name
        path.write_bytes(text.encode("utf-8"))
        return path

    def test_crlf_preserved(self) -> None:
        path = self.write("a.md", f"one{ZWSP} line\r\ntwo\r\n")
        run(str(path), "--write")
        self.assertEqual(path.read_bytes(), "one line\r\ntwo\r\n".encode("utf-8"))

    def test_quotes_and_ellipsis_untouched_by_default(self) -> None:
        text = f"She said {LDQ}hi{RDQ} and it{RSQ}s fine{ELLIPSIS}{ZWSP}\n"
        path = self.write("a.md", text)
        run(str(path), "--write")
        self.assertEqual(path.read_text(encoding="utf-8"), text.replace(f"{ZWSP}", ""))

    def test_flags_rewrite_quotes_and_ellipsis(self) -> None:
        path = self.write("a.md", f"{LDQ}hi{RDQ} it{RSQ}s{ELLIPSIS}\n")
        run(str(path), "--write", "--straighten-quotes", "--ellipsis")
        self.assertEqual(path.read_text(encoding="utf-8"), '"hi" it\'s...\n')

    def test_backup_created(self) -> None:
        original = f"x{ZWSP}y\n"
        path = self.write("a.md", original)
        run(str(path), "--write")
        backup = self.dir / "a.md.bak"
        self.assertTrue(backup.is_file())
        self.assertEqual(backup.read_text(encoding="utf-8"), original)

    def test_no_backup_flag(self) -> None:
        path = self.write("a.md", f"x{ZWSP}y\n")
        run(str(path), "--write", "--no-backup")
        self.assertFalse((self.dir / "a.md.bak").exists())

    def test_html_quotes_never_straightened(self) -> None:
        text = f'<p title="say {LDQ}hi{RDQ}">ok</p>\n'
        path = self.write("a.html", text)
        run(str(path), "--write", "--straighten-quotes")
        self.assertEqual(path.read_text(encoding="utf-8"), text)

    def test_stdin_crlf_preserved(self) -> None:
        proc = subprocess.run(
            [sys.executable, "-I", str(SCRIPT), "--write"],
            input=f"a{ZWSP}b\r\nc\r\n".encode("utf-8"),
            capture_output=True,
        )
        self.assertEqual(proc.stdout, b"ab\r\nc\r\n")

    def test_report_exits_1_on_tells(self) -> None:
        path = self.write("a.md", f"x{ZWSP}y\n")
        self.assertEqual(run(str(path)).returncode, 1)
        self.assertEqual(path.read_text(encoding="utf-8"), f"x{ZWSP}y\n")


if __name__ == "__main__":
    unittest.main()
