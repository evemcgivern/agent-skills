# Sonnet Prompt Improver

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Rewrites a prompt, system prompt, agent definition or skill so Claude Sonnet 5.5 does what you meant. It frames the request problem-first, adds only the fixes that match a symptom you have seen, and suggests effort and thinking settings. The fixes paraphrase Anthropic's [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5) guide (read 2026-10-03, rechecked 2026-10-17). Use on `/sonnet-prompt-improver` or when asked to "improve this prompt for Sonnet".

## What it looks like

Example, invented prompt. What you type, including the symptom you have seen:

```text
/sonnet-prompt-improver Fix the date bug in the CSV export. Last time it also
added tests and docs I didn't ask for.
```

What comes back: the prompt framed problem-first, plus only the fix that matches the symptom, then one line per change.

```text
Problem: Fix the date bug in the CSV export.
Evidence: [ ] (the wrong date and the expected one)
Autonomy: If you have a solution you are happy with, do it. If you are unsure,
give me options or mocks and stop.
Done means: [ ]
When the asked work is done and checked, stop and report; mention extras at
the end instead of doing them.

- treated this as a message you type to an agent
- added an evidence slot and a done slot
- added the autonomy line
- added the stop-and-report line: it adds tests and docs nobody asked for
```

For a system prompt, agent definition, or JSON API call, the reply also suggests effort and thinking settings in one line, such as starting at high effort and sweeping levels against real evals.

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder as `sonnet-prompt-improver/`; keep every file in it together.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
