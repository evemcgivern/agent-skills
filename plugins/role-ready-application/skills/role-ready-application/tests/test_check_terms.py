"""Coverage for the term-provenance check script."""

from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import check_terms  # noqa: E402

SOURCE = "Ran governance for 2,000+ applications. Maintained the application register and an audit cycle. Traced lineage."
POSTING = "Maintain the AI use case intake and repository. Coordinate with legal. Support audit readiness and lineage."


def flagged(draft: str) -> list[str]:
    return [term for term, _ in check_terms.check(SOURCE, POSTING, draft)]


class CheckTermsTests(unittest.TestCase):
    def test_posting_word_missing_from_source_is_flagged(self) -> None:
        self.assertEqual(flagged("Managed intake and legal review."), ["intake", "legal"])

    def test_words_the_source_uses_are_not_flagged(self) -> None:
        self.assertEqual(flagged("Ran the audit cycle and traced lineage for the register."), [])

    def test_plural_and_tense_variants_match_the_source(self) -> None:
        self.assertEqual(flagged("Audits and tracing of applications."), [])

    def test_words_only_in_the_resume_are_not_flagged(self) -> None:
        self.assertEqual(flagged("Wrote a data glossary."), [])

    def test_notes_after_the_marker_are_ignored(self) -> None:
        self.assertEqual(flagged("Ran the audit cycle.\n=== NOTES ===\nAdded intake and legal."), [])

    def test_structural_words_are_not_flagged(self) -> None:
        self.assertEqual(check_terms.check("Ran audits.", "Summary of skills and experience.", "SUMMARY\nSkills and experience."), [])

    def test_docx_input_is_read(self) -> None:
        path = Path(tempfile.mkdtemp()) / "r.docx"
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("word/document.xml", '<w:document xmlns:w="w"><w:body><w:p><w:r><w:t>Handled legal intake</w:t></w:r></w:p></w:body></w:document>')
        self.assertIn("legal", [t for t, _ in check_terms.check(SOURCE, POSTING, check_terms.read(str(path)))])


if __name__ == "__main__":
    unittest.main()
