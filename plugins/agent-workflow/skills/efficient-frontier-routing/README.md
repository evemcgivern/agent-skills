# Efficient Frontier Routing

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.2.0-informational.svg)](CHANGELOG.md)

Routes each task to a suitable model tier in Claude Code, Codex, or another agent host, following the user's routing preferences. Keeps small tasks local, delegates discovery, routine coding, and testing to cheaper subagents, and sends difficult decisions and risky reviews to a stronger one. Use when deciding whether to delegate, writing subagent handoffs, or setting routing preferences, or when asked to "save tokens", "use cheaper models", "fan out subagents", "stay inside my quota", or "efficient-frontier-routing help".

## What it looks like

How one task gets routed with the default settings:

```mermaid
flowchart TD
    A[New task] --> B{Quicker to do than to hand off?}
    B -->|Yes| C[Do it in the main session]
    B -->|No| D{Hard judgment or high risk?}
    D -->|No| E[Cheaper subagent gets a handoff packet]
    D -->|Yes| F[Stronger model decides or reviews]
    E -->|Evidence conflicts or two failed tries| F
    E --> G[Main session checks the evidence]
    F --> G
    C --> H[Report to the user]
    G --> H
```

High risk means auth, billing, permissions, security, migrations, data loss, shared state, caching, concurrency, cross-module behavior, public APIs, or user-visible workflows. Your own routing preferences (which models, how many subagents, whether escalation needs approval) override these defaults.

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder as `efficient-frontier-routing/`; keep every file in it together.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `references/configuration.md` — help text: saving the main model, effort, and routing preferences in Claude Code and Codex, a reusable review agent, and troubleshooting.
- `VERSION` and `CHANGELOG.md` — package version history.
