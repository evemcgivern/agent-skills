# Program Setup

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Design or review the launch of a governance body such as a software governance council, ITAM steering group, or AI governance board — charter, decision rights, membership, intake path, cadence, 90-day launch plan, and success measures. Use when starting a council or when an existing one has become a bottleneck or a rubber stamp.

## What it looks like

Review mode on the draft council charter in the kit's fictional demo estate:

| Step | What's missing | Why it matters | Fix |
|---|---|---|---|
| Sponsor | No executive sponsor named | No sponsor means no enforcement | Name an executive who controls the software budget |
| Decision rights | Purpose says the council oversees software; no decide or advise split, no stated thresholds | Every item can land on the agenda | Fill the decision-rights table, with a cost and risk threshold for each decision |
| Membership | 14 voting members | More than 9 slows decisions | Keep 5 to 9 voting; move the rest to consulted |
| Enforcement | No rule that procurement buys only approved items above threshold | Teams can buy around the council | Add the procurement rule and settle overlaps with other boards in writing |

````text
Decision needed: sponsor sign-off.

```findings
[{"type": "charter_gap", "id": "sponsor"},
 {"type": "charter_gap", "id": "decision-rights"},
 {"type": "charter_gap", "id": "membership-size"}]
```
````

The enforcement gap stays in the table only, because `charter_gap` findings use a fixed list of seven slugs. Review the same charter yourself in [practicum exercise 1](https://evemcgivern.github.io/app-governance-kit/practicum.html#program-setup).

## Install

See the [repository README](../../../../README.md#install) for Claude Code, Codex, other agents that read skill folders (Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot and more), Claude.ai and ChatGPT steps.

## Included

- `SKILL.md` and all workflow reference/template files:
- `SKILL.md`
- `checklist.md`
- `crosswalk.csv`
- `platform-guide.md`
- `sop.md`
- `template.md`
- `themes.md`
- `agents/openai.yaml` for ChatGPT/Codex skill-card metadata.
- `VERSION` and `CHANGELOG.md` for this package snapshot.

Source: [https://github.com/evemcgivern/app-governance-kit](https://github.com/evemcgivern/app-governance-kit).
