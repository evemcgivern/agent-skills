#!/usr/bin/env python3
"""Find text hidden by formatting in a DOCX or HTML file (standard library only).

Hidden text is read by a parser or an AI but not by a person: white or near-white color, a font size
under 4 pt, Word's hidden-text flag, display:none, zero-size or transparent styles, and comments.
Findings are possible matches. Quote them and let the candidate judge. A clean result does not prove
the file has no hidden text, and PDF files are not covered (mark them UNVERIFIED).

Usage: scan_hidden_text.py FILE.docx|FILE.html
"""

from __future__ import annotations

import re
import sys
import zipfile
from dataclasses import dataclass
from html import unescape

MIN_PT = 4  # below this size, text is not meant to be read
NEAR_WHITE = re.compile(r"^(?:f[0-9a-f]){3}$|^(?:white|ffffff)$", re.I)


@dataclass(frozen=True)
class Finding:
    reason: str
    text: str


def _near_white(value: str) -> bool:
    value = value.strip().lstrip("#").lower()
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    return bool(NEAR_WHITE.match(value)) and (value in ("white", "ffffff") or all(int(value[i : i + 2], 16) >= 0xF0 for i in (0, 2, 4)))


def scan_docx(path: str) -> list[Finding]:
    findings: list[Finding] = []
    with zipfile.ZipFile(path) as z:
        parts = [n for n in z.namelist() if n.startswith("word/") and n.endswith(".xml") and re.search(r"document|header|footer|footnotes|endnotes|comments", n)]
        for name in parts:
            xml = z.read(name).decode("utf-8", "replace")
            for run in re.findall(r"<w:r[ >].*?</w:r>", xml, flags=re.S):
                text = unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", run))).strip()
                if not text:
                    continue
                props = re.search(r"<w:rPr>.*?</w:rPr>", run, flags=re.S)
                p = props.group(0) if props else ""
                why = []
                if re.search(r"<w:vanish\b(?!\s+w:val=\"(?:0|false)\")", p):
                    why.append("hidden-text flag")
                color = re.search(r"<w:color w:val=\"([0-9A-Fa-f]{6}|auto)\"", p)
                if color and color.group(1) != "auto" and _near_white(color.group(1)):
                    why.append(f"near-white color {color.group(1)}")
                size = re.search(r"<w:sz w:val=\"(\d+)\"", p)
                if size and int(size.group(1)) / 2 < MIN_PT:
                    why.append(f"font size {int(size.group(1)) / 2:g} pt")
                if re.search(r"<w:w w:val=\"(?:[0-9]|1[0-9])\"", p):
                    why.append("text scaled to under 20%")
                if why:
                    findings.append(Finding(f"{name}: " + ", ".join(why), text))
            if name.endswith("comments.xml"):
                body = unescape(" ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml))).strip()
                if body:
                    findings.append(Finding(f"{name}: reviewer comments", body))
    return findings


def scan_html(path: str) -> list[Finding]:
    html = open(path, encoding="utf-8", errors="replace").read()
    findings: list[Finding] = [Finding("HTML comment", c.strip()) for c in re.findall(r"<!--(.*?)-->", html, flags=re.S) if c.strip()]
    hidden = r"display\s*:\s*none|visibility\s*:\s*hidden|font-size\s*:\s*0(?:px|pt|em|rem)?(?![\d.])|opacity\s*:\s*0(?![.\d])|color\s*:\s*(?:white|#f{3}\b|#f{6}\b)|text-indent\s*:\s*-\d{3,}"
    for m in re.finditer(r"<(\w+)([^>]*?(?:style\s*=\s*\"[^\"]*(?:" + hidden + r")[^\"]*\"|hidden|aria-hidden\s*=\s*\"true\")[^>]*)>(.*?)</\1>", html, flags=re.S | re.I):
        text = unescape(re.sub(r"<[^>]+>", " ", m.group(3))).strip()
        if text:
            findings.append(Finding("hidden by style or attribute", " ".join(text.split())))
    return findings


def render(path: str, findings: list[Finding]) -> str:
    head = "hidden text scan: clean" if not findings else f"hidden text scan: {len(findings)} finding(s), FLAGGED"
    return "\n".join([head, *(f"{f.reason}: {f.text}" for f in findings)])


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    path = argv[1]
    if path.lower().endswith(".docx"):
        findings = scan_docx(path)
    elif path.lower().endswith((".html", ".htm")):
        findings = scan_html(path)
    else:
        print("hidden text scan: UNVERIFIED (only DOCX and HTML are covered)")
        return 0
    print(render(path, findings))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
