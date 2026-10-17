# Rationalization

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Recommend tolerate, invest, migrate, or eliminate for each application in an inventory, find duplicates and license problems, and summarize savings and risk. Use for portfolio reviews, budget cycles, or post-merger cleanup.

## What it looks like

Example output on the kit's fictional demo estate (60 apps, licenses checked 2026-09-01). The per-app TIME table and data disposition are left out here:

````text
Duplicates (same category)               Keep     Why
APP-008 + APP-041  Contract management   APP-041  more users, lower cost
APP-014 + APP-052  E-signature           APP-014  more users, lower cost
APP-022 + APP-037  Endpoint management   open     022 has 345 more users;
                                                  037 costs 61,200 USD less
APP-029 + APP-058  Transport management  APP-058  more users, lower cost
APP-033 + APP-046  Customs brokerage     APP-046  more users, lower cost
Decision needed: final keep or retire calls.

Licenses
LIC-044  APP-044  expired 2025-12-31  97 entitlements for 748 users
LIC-017  APP-017  expired 2026-03-31  246 entitlements for 649 users
Far above users: 7 licenses, for example LIC-025 (350 for 45 users)

Potential savings: 294,200 to 355,400 USD a year from retiring one app
in each pair, depending on the endpoint call. A range, not a promise.

```findings
[{"type": "duplicate_app", "id": "APP-008+APP-041"},
 {"type": "duplicate_app", "id": "APP-014+APP-052"},
 {"type": "duplicate_app", "id": "APP-022+APP-037"},
 {"type": "duplicate_app", "id": "APP-029+APP-058"},
 {"type": "duplicate_app", "id": "APP-033+APP-046"},
 {"type": "expired_license", "id": "LIC-044"},
 {"type": "expired_license", "id": "LIC-017"}]
```
````

Run the same portfolio review yourself in [practicum exercise 4](https://evemcgivern.github.io/app-governance-kit/practicum.html#rationalization).

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
