# Access Review

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: full](https://img.shields.io/badge/Claude-full-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-full-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-full-brightgreen)](../../../../README.md#compatibility)

Review application user and role exports against HR records, find orphaned, excessive, and privileged access, and produce an evidence summary and auditor-ready memo mapped to ISO/IEC 27001 and COBIT DSS05. Use for quarterly or annual access reviews.

## What it looks like

Example output on the kit's fictional demo estate (120 accounts, 80 HR records, export checked 2026-09-01). Accounts on confidential applications come first:

````text
Exceptions
Account  Person   App      Issue                                  Action
ACC-063  EMP-072  APP-003  Left 2026-07-02, logged in 2026-08-08  Remove
ACC-104  EMP-099  APP-044  No matching person in the HR list      Investigate
ACC-019  EMP-071  APP-019  Left 2026-05-15, logged in 2026-08-20  Remove
7 admin accounts: ACC-017, 034, 051, 068, 085, 102, 119           Re-approve
Dormant (no login in 90 days): none
Segregation of duties: not checked, no role rules supplied

Decision needed: each removal, by the application owner.
Clauses: XW-016 periodic review, XW-017 leaver removal,
XW-018 privileged access.

```findings
[{"type": "orphaned_account", "id": "ACC-063"},
 {"type": "orphaned_account", "id": "ACC-104"},
 {"type": "orphaned_account", "id": "ACC-019"}]
```
````

A full run also writes the evidence summary and a one-page auditor memo. Try the same review yourself in [practicum exercise 5](https://evemcgivern.github.io/app-governance-kit/practicum.html#access-review).

## Install

See the [repository README](../../../../README.md#install) for Claude Code, Codex, other agents that read skill folders (Gemini CLI, Cursor, GitHub Copilot and more), Claude.ai and ChatGPT steps.

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
