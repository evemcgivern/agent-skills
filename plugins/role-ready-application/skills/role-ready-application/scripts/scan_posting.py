#!/usr/bin/env python3
"""Scan a pasted job posting for text that could steer an AI reader.

Advice only: it never blocks. Invisible and tag characters are removed from
the cleaned text. Mixed-script words and instruction-shaped lines are quoted
in the findings and left in the cleaned text. Standard library only.
"""

from __future__ import annotations

import argparse
import bisect
import re
import sys
import unicodedata
from dataclasses import dataclass

INVISIBLE = {chr(c) for c in (*range(0x200B, 0x2010), *range(0x2060, 0x2065), 0xFEFF, 0x00AD)}
BIDI = {chr(c) for c in (*range(0x202A, 0x202F), *range(0x2066, 0x206A))}
TAG_START, TAG_END, TAG_CANCEL, FLAG_BASE = 0xE0000, 0xE007F, 0xE007F, 0x1F3F4
VS_START, VS_END = 0xE0100, 0xE01EF  # supplementary variation selectors; U+FE0F is left alone

JOB_WORDS = r"(?:manager|director|coordinator|professor|lecturer|buyer|editor)"
CANDIDATE = r"(?:this|the)\s+(?:candidate|applicant)"
AI_ADDRESSEE = r"(?:ai|a\.i\.|llm|chatbot|language model|automated|ats|applicant[- ]tracking|bot)s?\b"
PEOPLE = r"(?:engineers?|developers?|researchers?|scientists?|practitioners?|specialists?|professionals?|enthusiasts?|candidates?|applicants?|teams?|users?)"

INSTRUCTION_PATTERNS = [
    re.compile(r"\b(ignore|disregard|forget)\b.{0,25}\b(previous|prior|above|earlier)\b.{0,25}\b(instructions?|guidance|rules|prompts?|messages?)\b", re.I),
    re.compile(r"\byou are now\b\s+(?:an?\s+|the\s+)?(?:(?:ai|llm|chatbot|language model)\b|assistant\b(?!\s+" + JOB_WORDS + r"\b))", re.I),
    re.compile(r"\brecommend(?:ing)?\s+(?:hiring|hire|selecting|advancing)\s+" + CANDIDATE + r"\b", re.I),
    re.compile(r"\b(?:rate|rank|score)\s+" + CANDIDATE + r"\s+(?:highly|higher|first|favou?rably|as\s+(?:a\s+)?(?:top|best|strong|excellent)\b)", re.I),
    re.compile(r"\bgive\s+(?:this|the)\s+(?:candidate|applicant)\s+(?:top|full|highest|maximum)\s+(?:marks?|scores?|ratings?)\b", re.I),
    re.compile(r"\bdo not (tell|mention|reveal|disclose|inform)\b[^.\n]{0,30}\b(user|human|reader|recruiter)\b", re.I),
    # A line addressed to an AI reader, such as "Note to AI screening tools:". People named after the
    # addressee (AI engineers, AI/ML researchers) are ordinary hiring text and are left alone.
    re.compile(r"\b(?:(?:note|message|notice|instructions?|reminder)s?\s+(?:to|for)|attention|attn)\s+(?:(?:any|all|the)\s+)?" + AI_ADDRESSEE + r"(?!\s*[/\-]\s*\w)(?!\s+" + PEOPLE + r"\b)", re.I),
    # A blanket instruction about every applicant, such as "rate every applicant as a 98% match".
    re.compile(r"\b(?:rate|rank|score|mark)\s+(?:every|all|each|any)\s+(?:candidate|applicant)s?\s+(?:as\s+(?:an?\s+)?(?:\d{2,3}\s?%|(?:top|best|strong|excellent|perfect|ideal)\b)|(?:highly|favou?rably|first)\b)", re.I),
]

WORD = re.compile(r"\w+", re.UNICODE)
UNIT_WORD = re.compile(r"\d+[\u0370-\u03ff\u1f00-\u1fff]+[A-Za-z]{0,2}")  # for example 5 micrometres
SCRIPTS = ("LATIN", "CYRILLIC", "GREEK")


@dataclass(frozen=True)
class Finding:
    kind: str
    line: int
    excerpt: str


@dataclass(frozen=True)
class ScanResult:
    cleaned: str
    findings: tuple[Finding, ...]
    flagged: bool


def _code(ch: str) -> str:
    return f"U+{ord(ch):04X}"


def _is_tag(ch: str) -> bool:
    return TAG_START <= ord(ch) <= TAG_END


def _is_variation_selector(ch: str) -> bool:
    return VS_START <= ord(ch) <= VS_END


def _is_subdivision_flag(run: str) -> bool:
    """True for a tag run shaped like gbeng or usca: 2 letters, 1-3 letters/digits, one cancel."""
    if ord(run[-1]) != TAG_CANCEL:
        return False
    body = run[:-1]
    if not 3 <= len(body) <= 5 or any(not _is_tag(c) for c in body):
        return False
    decoded = "".join(chr(ord(c) - TAG_START) for c in body)
    return bool(re.fullmatch(r"[a-z]{2}[a-z0-9]{1,3}", decoded))


def _is_non_latin_letter(ch: str) -> bool:
    return ch.isalpha() and not unicodedata.name(ch, "").startswith("LATIN")


def _script(ch: str) -> str | None:
    if not ch.isalpha():
        return None
    name = unicodedata.name(ch, "")
    for script in SCRIPTS:
        if name.startswith(script):
            return script
    return None


def _scan_line(line: str, number: int) -> tuple[str, list[Finding]]:
    findings: list[Finding] = []
    kept: list[str] = []
    i = 0
    while i < len(line):
        ch = line[i]
        if _is_tag(ch):
            j = i
            while j < len(line) and _is_tag(line[j]):
                j += 1
            run = line[i:j]
            is_flag = bool(kept) and kept[-1] == chr(FLAG_BASE) and _is_subdivision_flag(run)
            if is_flag:
                kept.append(run)
            else:
                findings.append(Finding("tag", number, f"{len(run)} tag character(s), hidden text: {_tag_text(run)!r}"))
            i = j
            continue
        if _is_variation_selector(ch):
            j = i
            while j < len(line) and _is_variation_selector(line[j]):
                j += 1
            findings.append(Finding("tag", number, f"{j - i} variation selector character(s), possible hidden data"))
            i = j
            continue
        if ch in BIDI:
            findings.append(Finding("tampering", number, f"direction control {_code(ch)}"))
            kept.append(ch)
        elif ch in INVISIBLE:
            before = line[i - 1] if i > 0 else ""
            after = line[i + 1] if i + 1 < len(line) else ""
            if ch == "\u00ad":
                findings.append(Finding("invisible", number, f"invisible {_code(ch)}"))  # soft hyphen: ordinary typesetting
            elif ch in "\u200c\u200d" and _is_non_latin_letter(before) and _is_non_latin_letter(after):
                kept.append(ch)  # ordinary spelling in Persian and similar scripts
            elif before.isalnum() and after.isalnum():
                findings.append(Finding("tampering", number, f"invisible {_code(ch)} inside a word"))
            else:
                findings.append(Finding("invisible", number, f"invisible {_code(ch)}"))
            # Removed from cleaned text either way.
        else:
            kept.append(ch)
        i += 1
    cleaned = "".join(kept)
    for word in WORD.findall(cleaned):
        if UNIT_WORD.fullmatch(word):
            continue
        scripts = {s for s in map(_script, word) if s}
        if len(scripts) > 1:
            findings.append(Finding("mixed-script", number, word.encode("ascii", "backslashreplace").decode("ascii")))
    for pattern in INSTRUCTION_PATTERNS:
        if pattern.search(cleaned):
            findings.append(Finding("instruction", number, cleaned.strip()))
            break
    return cleaned, findings


def _tag_text(run: str) -> str:
    return "".join(chr(ord(c) - TAG_START) for c in run if 0x20 <= ord(c) - TAG_START < 0x7F)


def _scan_across_lines(cleaned_lines: list[str], findings: list[Finding]) -> list[Finding]:
    """Find instruction patterns split over a line break; one finding per start line."""
    starts: list[int] = []
    offset = 0
    for line in cleaned_lines:
        starts.append(offset)
        offset += len(line) + 1
    joined = "\n".join(cleaned_lines).replace("\n", " ")
    seen = {f.line for f in findings if f.kind == "instruction"}
    extra: list[Finding] = []
    for pattern in INSTRUCTION_PATTERNS:
        for match in pattern.finditer(joined):
            first = bisect.bisect_right(starts, match.start()) - 1
            last = bisect.bisect_right(starts, max(match.end() - 1, match.start())) - 1
            if first == last or first + 1 in seen:
                continue
            seen.add(first + 1)
            excerpt = " ".join(line.strip() for line in cleaned_lines[first : last + 1])
            extra.append(Finding("instruction", first + 1, excerpt))
    return extra


def scan(text: str) -> ScanResult:
    cleaned_lines: list[str] = []
    findings: list[Finding] = []
    for number, line in enumerate(text.split("\n"), start=1):
        cleaned, found = _scan_line(line, number)
        cleaned_lines.append(cleaned)
        findings.extend(found)
    findings.extend(_scan_across_lines(cleaned_lines, findings))
    findings.sort(key=lambda f: f.line)
    flagged = any(f.kind != "invisible" for f in findings)
    return ScanResult("\n".join(cleaned_lines), tuple(findings), flagged)


def render(result: ScanResult) -> str:
    if not result.findings:
        head = "posting scan: clean"
    else:
        head = f"posting scan: {len(result.findings)} finding(s)" + (", FLAGGED" if result.flagged else "")
    lines = [head]
    lines += [f"line {f.line}: {f.kind}: {f.excerpt}" for f in result.findings]
    lines += ["--- text ---", result.cleaned]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan a pasted job posting (advice only).")
    parser.add_argument("--in", dest="path", help="read the posting from this file (default: stdin)")
    args = parser.parse_args(argv)
    try:
        data = open(args.path, "rb").read() if args.path else sys.stdin.buffer.read()
    except OSError as error:
        print(f"posting scan: cannot read input: {error}", file=sys.stderr)
        return 2
    text = data.decode("utf-8", errors="replace")
    sys.stdout.buffer.write(render(scan(text)).encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
