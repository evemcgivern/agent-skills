# Crosswalk

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Map a control, requirement, or policy statement to ISO/IEC 19770-1, COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001 clauses, and show where coverage is missing. Use when writing or auditing a control, or explaining how frameworks overlap.

## What it looks like

Example output for the three sample controls in the kit's fictional demo estate. Clause numbers come from `crosswalk.csv`:

| Control | XW row | ISO/IEC 19770-1 | COBIT 2019 | ISO/IEC 27001 | ISO/IEC 42001 |
|---|---|---|---|---|---|
| C1 Keep an accurate inventory with owners | XW-001 | 8.3 | BAI09.01 | A.5.9 | no direct equivalent |
| C2 Review access on a schedule, remove what is not needed | XW-016 | no direct equivalent | DSS05.04 | A.5.18 | no direct equivalent |
| C3 Assess each AI system for risk before deployment | XW-021 | no direct equivalent | APO12 | no direct equivalent | 6.1.4, A.5 |

````text
Gaps
C2: ISO/IEC 19770-1 and 42001 have no access-review clause; their auditors
    would look for the ISO/IEC 27001 control instead.
C3: ISO/IEC 27001 has no AI-specific clause; its auditor would look for the
    AI system inside the general risk assessment.

```findings
[{"type": "crosswalk_match", "id": "C1:XW-001"},
 {"type": "crosswalk_match", "id": "C2:XW-016"},
 {"type": "crosswalk_match", "id": "C3:XW-021"}]
```
````

Browse all 29 themes across the four frameworks in the [crosswalk explorer](https://evemcgivern.github.io/app-governance-kit/crosswalk.html), or map the controls yourself in [practicum exercise 3](https://evemcgivern.github.io/app-governance-kit/practicum.html#crosswalk).

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
