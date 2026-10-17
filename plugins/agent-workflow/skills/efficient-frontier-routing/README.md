# Efficient Frontier Routing

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.2.0-informational.svg)](CHANGELOG.md)

Routes each task to a suitable model tier in Claude Code, Codex, or another agent host, following the user's routing preferences. Keeps small tasks local, delegates discovery, routine coding, and testing to cheaper subagents, and sends difficult decisions and risky reviews to a stronger one. Use when deciding whether to delegate, writing subagent handoffs, or setting routing preferences, or when asked to "save tokens", "use cheaper models", "fan out subagents", "stay inside my quota", or "efficient-frontier-routing help".

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder as `efficient-frontier-routing/`; keep every file in it together.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `references/configuration.md` — help text: saving the main model, effort, and routing preferences in Claude Code and Codex, a reusable review agent, and troubleshooting.
- `VERSION` and `CHANGELOG.md` — package version history.
