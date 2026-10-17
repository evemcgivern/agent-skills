#!/usr/bin/env python3
"""Find and remove the characters that mark prose as machine-written.

Zero dependencies, stdlib only, so it runs in a Node repo, a Python repo, or a
bare directory of markdown with no install step.

This is NOT watermark removal. No production text model watermarks its output
cryptographically except Gemini (SynthID), which this cannot touch and does not
try to. What it removes is residue: characters a model emits because its
training data contained them, which a human typing in a plain editor would not.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Invisible characters with no linguistic function anywhere, so deleting them
# cannot change meaning: soft hyphen, combining grapheme joiner, zero-width
# space, word joiner, byte-order mark.
#
# DELIBERATELY EXCLUDED, do not "complete" this set:
#   U+200C ZWNJ and U+200D ZWJ are load-bearing. ZWJ builds emoji sequences, so
#   deleting it splits a family emoji into separate people. ZWNJ is required
#   Persian and Indic orthography. An earlier version of this class spanned
#   U+200B-U+200D and did exactly that damage.
#   Bidi controls are excluded for the same reason: meaningful in
#   mixed-direction text. They are a spoofing vector, but that is a security
#   concern with a different owner, not prose residue.
INVISIBLE = re.compile("[\u00ad\u034f\u200b\u2060\ufeff]")

# Space characters that are not U+0020. Collapsed to a plain space rather than
# deleted, because they ARE holding words apart. U+202F (narrow no-break space)
# is the one GPT emits most, typically before a colon or a percent sign.
EXOTIC_SPACE = re.compile("[   -   　]")

# Visible, valid punctuation that is still a tell because models overuse it.
# Each is a separate editorial decision, so each gets its own flag.
TELLS = {
    "invisible": INVISIBLE,
    "exotic_space": EXOTIC_SPACE,
    "em_dash": re.compile("—"),
    "en_dash": re.compile("–"),
    "curly_quote": re.compile("[‘’“”]"),
    "ellipsis": re.compile("…"),
}

TEXT_SUFFIXES = {".md", ".mdx", ".txt", ".markdown", ".rst", ".html"}

# Files where a quote character can be syntax (HTML attributes, JSX props).
# Straightening a curly quote there can close an attribute early, so quote
# rewriting is never applied to these, even with --straighten-quotes.
MARKUP_SUFFIXES = {".html", ".htm", ".mdx", ".xml", ".svg"}


def report(text: str) -> dict[str, int]:
    """Count tells without changing anything."""
    return {name: len(pattern.findall(text)) for name, pattern in TELLS.items()}


def scrub(
    text: str,
    em_dash: str | None = None,
    en_dash: str | None = None,
    ellipsis: str | None = None,
    curly_quotes: bool = False,
) -> str:
    """Delete invisibles always; rewrite visible punctuation only where a
    replacement was given. `None` means leave that character alone."""
    out = INVISIBLE.sub("", text)
    out = EXOTIC_SPACE.sub(" ", out)
    if em_dash is not None:
        # Absorb the spaces around the dash, but only HORIZONTAL space: \s would
        # eat the blank line between two Markdown paragraphs and weld them
        # together. Requiring a non-space before the dash also leaves a
        # line-initial dash alone, which is an attribution, not a tell.
        def _swap(m: "re.Match[str]") -> str:
            rest = out[m.end():]
            ends_line = rest == "" or rest[0] in "\r\n"
            return m.group(1) + (em_dash.rstrip() if ends_line else em_dash)

        out = re.sub(r"(\S)[^\S\r\n]*—[^\S\r\n]*", _swap, out)
    if en_dash is not None:
        out = out.replace("–", en_dash)
    if ellipsis is not None:
        out = out.replace("…", ellipsis)
    if curly_quotes:
        out = re.sub("[‘’]", "'", out)
        out = re.sub("[“”]", '"', out)
    return out


def targets(paths: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            found += sorted(
                f for f in p.rglob("*")
                if f.is_file()
                and f.suffix.lower() in TEXT_SUFFIXES
                and not any(part in {"node_modules", ".git", "dist", ".next"} for part in f.parts)
            )
        else:
            found.append(p)
    return found


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Report or remove AI tells in prose.",
        epilog="Default is report-only. Exits 1 when tells are found, so it works as a CI gate.",
    )
    ap.add_argument("paths", nargs="*", help="Files or directories. Omit to read stdin.")
    ap.add_argument("--write", action="store_true",
                    help="Rewrite in place (or to stdout for stdin). Saves FILE.bak first.")
    ap.add_argument("--no-backup", action="store_true", help="With --write, do not save FILE.bak.")
    ap.add_argument("--em-dash", default=None, metavar="STR",
                    help="Replacement for em dashes, e.g. ', ' or '; ' or ' - '. Omit to leave them.")
    ap.add_argument("--en-dash", default=None, metavar="STR",
                    help="Replacement for en dashes. Omit to leave them (number ranges are legitimate).")
    ap.add_argument("--ellipsis", action="store_true",
                    help="Replace the ellipsis glyph with three periods. Off by default.")
    ap.add_argument("--straighten-quotes", action="store_true",
                    help="Replace curly quotes with straight ones. Off by default; "
                         "never applied to HTML, MDX, XML or SVG files.")
    args = ap.parse_args()

    opts = dict(
        em_dash=args.em_dash,
        en_dash=args.en_dash,
        ellipsis="..." if args.ellipsis else None,
        curly_quotes=args.straighten_quotes,
    )

    if not args.paths:
        # Bytes in and out, so CRLF line endings survive unchanged.
        text = sys.stdin.buffer.read().decode("utf-8")
        counts = report(text)
        if args.write:
            sys.stdout.buffer.write(scrub(text, **opts).encode("utf-8"))
        else:
            show("stdin", counts)
        return 1 if sum(counts.values()) and not args.write else 0

    total = 0
    for path in targets(args.paths):
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            print(f"skipped {path}: {exc}", file=sys.stderr)
            continue
        counts = report(text)
        n = sum(counts.values())
        total += n
        if args.write:
            file_opts = dict(opts)
            if path.suffix.lower() in MARKUP_SUFFIXES:
                file_opts["curly_quotes"] = False
            new = scrub(text, **file_opts)
            if new != text:
                if not args.no_backup:
                    backup = path.with_name(path.name + ".bak")
                    if backup.exists():
                        print(f"kept existing backup {backup}", file=sys.stderr)
                    else:
                        backup.write_bytes(raw)
                # Bytes, not write_text: write_text would turn CRLF into LF.
                path.write_bytes(new.encode("utf-8"))
                print(f"scrubbed {path} ({n} tells found)", file=sys.stderr)
        elif n:
            show(str(path), counts)

    if not args.write:
        print(f"\n{total} tell(s) total", file=sys.stderr)
    return 1 if total and not args.write else 0


def show(label: str, counts: dict[str, int]) -> None:
    hits = {k: v for k, v in counts.items() if v}
    if not hits:
        print(f"clean: {label}", file=sys.stderr)
        return
    print(f"{label}:", file=sys.stderr)
    for kind, n in hits.items():
        print(f"  {kind:<13} {n}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
