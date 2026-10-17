# Ambition

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Reconsiders a project or shelved idea against what tools and models can do now. It proposes three different, grounded outcomes, separates observed facts from assumptions, recommends one, and designs the smallest experiment that would settle its hardest uncertainty. It is advisory: it never starts work, spends money, or expands an assignment on its own. It can hand a chosen outcome to the mission skill, if installed.

## What it looks like

Example output, invented data, shortened. The reply is a short context, an options table, the experiment for the recommended option, and the decision left to you.

Context: offline editing was shelved because merging edits needed a server rewrite (observed: `docs/roadmap.md`).

| # | Outcome, who benefits | Constraint challenged | Hardest uncertainty | Effort, downside |
|---|---|---|---|---|
| 1 | Offline editing for field staff | Merging needed a server rewrite (observed) | Whether a client-side merge handles the note format (untested capability) | Weeks (estimate); risk of lost edits |
| 2 | Read-only offline cache | None; feasible today | Whether users need to edit offline (assumed) | Days (estimate); small upside |
| 3 | Leave the scope alone | - | - | None |

Recommended: 1. Option 2 is cheaper but skips what field staff asked for.

```text
1. Hypothesis: a client-side merge keeps every edit in recorded conflicts.
2. Smallest artifact: a script that merges 50 recorded edit pairs.
3. Procedure: the script does not exist yet, so writing it is the work.
   Baseline: the current server merge on the same 50 pairs.
4. Pass/fail: zero lost edits passes; any silent loss fails.
5. Resources: proposed ceiling of one day, no spend; needs the edit samples.
6. Next decision: pass, plan option 1; fail, offer option 2;
   inconclusive, widen the sample.

Decision needed: run the experiment, yes or no?
```

Nothing starts until you answer: the skill only advises.

## Install

Copy this complete folder to `~/.claude/skills/ambition/` for Claude Code (CLI and local desktop sessions), or to `~/.agents/skills/ambition/` for Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and OpenCode. For one repository only, copy it to `.claude/skills/ambition/` or `.agents/skills/ambition/` (Windsurf also reads `.agents/skills`); Cline reads `.cline/skills/ambition/` or `.claude/skills/ambition/`. Supporting files in this folder may be required. See the [collection README](../../../../README.md#install) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
