#!/usr/bin/env python3
"""List words in a draft resume that come from the job posting but not from the candidate's source resume.

Every such word is a claim the source does not back, or a posting word that needs a recorded
same-meaning equivalent. The script only counts and lists; a person or the skill decides what
to remove, replace with the source's own term, or keep as an approved equivalent. It is a
word-overlap check: plural, -ing and -ed forms count as the same word, any other derived form
counts as a different word ("reconciliation" is not "reconciled"), words under four letters are
skipped (so it cannot check SQL or AWS), and it can list harmless words and cannot judge meaning.

Usage:
  check_terms.py --source SOURCE --posting POSTING --resume DRAFT
Each argument is a .txt, .md or .docx file. Text before a line reading "=== NOTES ===" is used
for the draft. Standard library only.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import zipfile

STOP = set(
    "the and for with that this from have been into your their about which while where when also such than them "
    "these those they what more most other some only over under between through during across within without "
    "around after before being were will would could should may can any all each both our out its his her you who "
    "how why not are was has had but per via using used use made make many much very own same just like".split()
)
# Words that name parts of a resume or are generic verbs; they carry no claim.
STRUCTURAL = set("summary skills skill experience education certification certifications present progress include includes including".split())
WORD = re.compile(r"[a-z][a-z0-9&\-]{2,}")


def read(path: str) -> str:
    if path.lower().endswith(".docx"):
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "replace")
        paragraphs = re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S)
        return "\n".join(html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))) for p in paragraphs)
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def stem(word: str) -> str:
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        word = word[:-1]
    for suffix in ("ing", "ed"):
        if word.endswith(suffix) and len(word) > len(suffix) + 3:
            return word[: -len(suffix)]
    return word


def words(text: str) -> list[str]:
    return [w.strip("-&") for w in WORD.findall(text.lower())]


def stems(text: str) -> set[str]:
    return {stem(w) for w in words(text) if w not in STOP}


def matches(term_stem: str, pool: set[str]) -> bool:
    return term_stem in pool


def check(source: str, posting: str, draft: str) -> list[tuple[str, str]]:
    """Return (term, first draft line containing it) for posting words in the draft but not the source."""
    draft = draft.partition("=== NOTES ===")[0]
    src, post = stems(source), stems(posting)
    found: dict[str, str] = {}
    for line in draft.splitlines():
        for w in words(line):
            if w in STOP or w in STRUCTURAL or len(w) < 4:
                continue
            s = stem(w)
            if matches(s, post) and not matches(s, src) and w not in found:
                found[w] = line.strip()
    return sorted(found.items())


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", required=True)
    parser.add_argument("--posting", required=True)
    parser.add_argument("--resume", required=True)
    args = parser.parse_args(argv[1:])
    found = check(read(args.source), read(args.posting), read(args.resume))
    print("term check: clean" if not found else f"term check: {len(found)} posting-only term(s), FLAGGED")
    for term, line in found:
        print(f"- {term}: {line[:140]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
