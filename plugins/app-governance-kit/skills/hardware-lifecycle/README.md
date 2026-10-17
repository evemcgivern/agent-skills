# Hardware Lifecycle

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Check a device fleet for hardware overdue for refresh and retired devices missing a confirmed data wipe, estimate replacement cost, and produce a disposal-readiness summary. Use for a refresh cycle review, before a hardware budget request, or before closing out a disposal.

## What it looks like

Example output on the kit's fictional demo estate (60 devices, checked 2026-09-01):

````text
Devices needing action
Device   Type     Status   Issue                                 Recommendation
DEV-008  server   active   Refresh was due 2026-03-05            Replace, upgrade or extend
DEV-027  mobile   active   Refresh was due 2026-03-05            Replace, upgrade or extend
DEV-045  laptop   active   Refresh was due 2026-03-05            Replace, upgrade or extend
DEV-011  mobile   retired  Retired 2023-02-19, wipe not confirmed  Wipe or certified destruction
DEV-042  desktop  retired  Retired 2025-01-09, wipe not confirmed  Wipe or certified destruction

Refresh cost: 3 devices, from 10,240 USD at original purchase cost.
Unverified: current replacement prices, which set the top of the range.
Decision needed: the asset owner picks replace, upgrade or extend.

Blocking disposal: DEV-011, DEV-042. Neither can be marked disposed
until wipe evidence is attached.
Decision needed: confirmation from whoever is accountable for disposal.

```findings
[{"type": "overdue_refresh", "id": "DEV-008"},
 {"type": "overdue_refresh", "id": "DEV-027"},
 {"type": "overdue_refresh", "id": "DEV-045"},
 {"type": "unwiped_retired_device", "id": "DEV-011"},
 {"type": "unwiped_retired_device", "id": "DEV-042"}]
```
````

Work the same fleet yourself in [practicum exercise 7](https://evemcgivern.github.io/app-governance-kit/practicum.html#hardware-lifecycle).

## Install

See the [repository README](../../../../README.md#install) for Claude Code, Codex, other agents that read skill folders (Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and more), Claude.ai and ChatGPT steps.

## Included

- `SKILL.md` and all workflow reference/template files:
- `SKILL.md`
- `checklist.md`
- `crosswalk.csv`
- `platform-guide.md`
- `sop.md`
- `template.csv`
- `themes.md`
- `agents/openai.yaml` for ChatGPT/Codex skill-card metadata.
- `VERSION` and `CHANGELOG.md` for this package snapshot.

Source: [https://github.com/evemcgivern/app-governance-kit](https://github.com/evemcgivern/app-governance-kit).
