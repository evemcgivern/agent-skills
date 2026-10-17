---
name: scrub-ai-tells
description: "Find and remove the characters that mark prose as machine-written — zero-width spaces, narrow no-break spaces, em dashes, curly quotes, ellipsis glyphs. Use before publishing a blog post, doc, or README written or edited with AI help, and when someone says text looks like AI wrote it, asks about AI watermarks, or wants invisible Unicode stripped."
---

# Scrub AI tells

If the current repo has its own `.claude/skills/scrub-ai-tells/`, that version is authoritative — follow it instead.

## What this actually is

**It is not watermark removal.** Say so plainly if the user assumes otherwise, because the assumption changes what they should do:

| Vendor | Text output | Image output |
|---|---|---|
| Anthropic (Claude) | No watermark | n/a |
| OpenAI (GPT) | No watermark shipped — one was built, never released | C2PA metadata |
| Google (Gemini) | **SynthID, deployed and real** | SynthID + C2PA |

Verify against current vendor docs before repeating the table; it drifts.

Nothing here touches SynthID, which is statistical and lives in token choice, not characters. What this removes is **residue**: characters a model emits because its training data contained them, and which a human typing in a plain editor would not produce.

Two classes, and the difference matters:

1. **Invisible characters** — zero-width space, word joiner, BOM, soft hyphen, and non-breaking spaces including U+202F (collapsed to a plain space). Always safe to remove. The script deliberately keeps zero-width joiner and non-joiner (emoji sequences and Persian/Indic text need them) and bidi controls. They carry no meaning in English prose and they actively break search, diffing, `grep`, and PDF text extraction. No editorial judgement involved.
2. **Visible punctuation** — em dash, en dash, curly quotes, the ellipsis glyph. Legitimate typography that is only a tell because models overuse it. **Every one of these is a voice decision. Never rewrite them without asking.**

## Invocation

Invoked as `/scrub-ai-tells [target] [--write]`. Read the arguments and run the command yourself; the user should never type the interpreter path.

| The user types | You run |
|---|---|
| `/scrub-ai-tells` | Report on the file under discussion if one is obvious, or on pasted text piped through stdin |
| `/scrub-ai-tells draft.md` | Report on that path |
| `/scrub-ai-tells content/blog/` | Report across the tree |
| `/scrub-ai-tells draft.md --write` | Apply, then show the diff |

Report-only unless `--write` is present. Exits 1 when tells are found, so it doubles as a CI gate.

The script ships next to this file. Set `S` to `scrub_ai_tells.py` inside this skill's folder (wherever the skill is installed):

```bash
S=<this skill's folder>/scrub_ai_tells.py

python3 "$S" draft.md                             # report
python3 "$S" content/blog/                        # tree (.md .mdx .txt .rst .html)
python3 "$S" < pasted.txt                         # report on pasted text (stdin)
python3 "$S" draft.md --write --em-dash " - "     # apply, default replacement
python3 "$S" --write --em-dash " - " < pasted.txt > clean.txt
```

Optional clipboard use: on macOS, `pbpaste | python3 "$S"` reports on the clipboard and `pbpaste | python3 "$S" --write --em-dash " - " | pbcopy` scrubs it in place. On Linux use `xclip -selection clipboard -o` to read and `xclip -selection clipboard` to write (or `wl-paste` / `wl-copy` on Wayland); on Windows PowerShell use `Get-Clipboard | python "$S"` and `| Set-Clipboard`. The file and stdin forms above work everywhere.

Stdlib only, no install. Flags: `--em-dash STR`, `--en-dash STR`, `--ellipsis` (glyph to three periods), `--straighten-quotes`, `--no-backup`. Every punctuation rewrite is off unless its flag is passed.

`--write` on a file saves the original as `FILE.bak` first (an existing `.bak` is kept, not overwritten) unless `--no-backup` is given, and keeps line endings exactly as they were, CRLF included. Curly quotes are never straightened in `.html`, `.htm`, `.mdx`, `.xml` or `.svg` files, even with `--straighten-quotes`, because a quote there can be attribute syntax.

## Procedure

1. **Report first, always.** Run without `--write` and show the counts. The counts are the interesting part — they say whether the prose is drifting, and a writer who sees "31 em dashes" learns something a silent rewrite would have hidden.
2. **Scrub invisibles without asking.** `--write` with no punctuation flags does exactly this and nothing else. It cannot damage prose.
3. **Em dashes become `" - "`.** Offer this as the default when you ask, and pass `--em-dash " - "` only after the user agrees or has already stated that preference (or the repository's instructions do). The reasoning, in case someone challenges it: the semicolon is what most style guides want but is the worst *automatic* choice, because a model's em dash often is not joining two independent clauses and the substitution then produces a grammatically wrong semicolon. The comma yields comma splices on the same sentences. The spaced hyphen preserves the intended break exactly and can never make a sentence ungrammatical. It reads slightly informal; that is the accepted cost.
4. **Re-read the diff after any punctuation rewrite.** Mechanical replacement is safe, not good — a human editor should still restructure the sentence. Errors of judgement do not show up in the counts.

## Not this skill

- **"Humanize this" / "make it sound less like AI"** is a rewrite of sentence *structure* and rhythm — cadence, burstiness, hedging, the tricolon habit. Use the writing or voice skill for that. This skill only touches characters, and a text can be fully scrubbed and still read as machine-written.
- **Image or video provenance** (C2PA, EXIF, visible vendor badges) is a different problem with different tools. Note that stripping provenance metadata can conflict with an image provider's terms of service; flag that rather than doing it silently.

## Wiring it into a repo

Copy `scrub_ai_tells.py` into the repo (or point at the installed skill folder) and add a `package.json` script or `Makefile` target that runs it, and put the report mode in CI on the docs/blog directory. Report mode's exit code is designed for this. Do not put `--write` in CI — a pipeline that silently edits prose is worse than the tells.
