# Fable Chief Agent

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)
> The Claude app and ChatGPT have no documented subagents, so the delegation loop cannot run. Other agents: needs subagents on a chosen model (Gemini CLI, Antigravity CLI, Cursor, OpenCode); others not verified.

Makes the most capable, most expensive model in a session the senior decision-maker. It keeps that model's reasoning for intent, architecture, decomposition, tradeoffs, final review, and synthesis, and routes discovery, implementation, tests, logs, and verification to cheaper agents by tier. For high-risk work it recommends a review by a model from a different vendor when one is available, and otherwise a fresh same-vendor reviewer, labelled as not cross-vendor.

## What it looks like

Who does what. Tier names follow the Claude 5 family; with another provider, map them to its strong, standard, and small models.

| Tier | Owns | Does not |
|---|---|---|
| Fable (the top model in the session) | Real intent, scope, approach, task order, tradeoffs, hidden risks, settling disagreements, final review and answer | Search, read, edit, test, or verify when someone cheaper can |
| Opus | Hardest delegated work: complex implementation, deep debugging, cross-module, security, concurrency, reviewing cheaper agents | Hold final authority |
| Sonnet | Scoped implementation, tests, local refactors, clear failures, following existing patterns | Make product calls or change architecture |
| Haiku | Repo discovery, file and log summaries, checklist checks, edge-case scans | Decide direction: it reports facts |

The boundary in one line:

> If the task is mostly searching, reading, editing, testing, or verifying, it belongs to another agent. If it involves intent, design, tradeoffs, risk, disagreement, or final approval, it belongs to Fable.

For high-risk work (auth, billing, migrations, data loss and the like), Fable decides, Opus handles or reviews the hard parts, and a reviewer from a different vendor is recommended when available. A same-vendor review is labelled as not cross-vendor.

## Install

Copy this complete folder to `~/.claude/skills/fable-chief-agent/` for Claude Code (CLI and local desktop sessions), or to `~/.agents/skills/fable-chief-agent/` for Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and OpenCode. For one repository only, copy it to `.claude/skills/fable-chief-agent/` or `.agents/skills/fable-chief-agent/` (Windsurf also reads `.agents/skills`); Cline reads `.cline/skills/fable-chief-agent/` or `.claude/skills/fable-chief-agent/`. The delegation needs subagents on a chosen model: Claude Code, Codex, Gemini CLI and Antigravity CLI have them; other agents are not verified. Supporting files in this folder may be required. See the [collection README](../../../../README.md#install) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
