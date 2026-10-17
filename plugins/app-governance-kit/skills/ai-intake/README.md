# Ai Intake

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![Claude Code](https://img.shields.io/badge/Claude%20Code-supported-6B4FBB) ![Codex](https://img.shields.io/badge/Codex-supported-111111) ![ChatGPT](https://img.shields.io/badge/ChatGPT-skill%20upload-74AA9C) ![License](https://img.shields.io/badge/license-MIT-green)

Take a description of an AI use case, assign a risk tier under the EU AI Act with NIST AI RMF and ISO/IEC 42001 controls, and produce an AI inventory record. Use whenever a team proposes a new AI tool or changes how one is used.

## What it looks like

Example output for one of the six AI systems in the kit's fictional demo estate:

````text
AI-004 (owner: HR)
Restatement: ranks job applicants' CVs and shortlists candidates for
interview. Affects job applicants. Uses CVs, which hold personal data.
Unverified: whether a person reviews each shortlist; where the data came from.

Prohibited practices: none apparent.
Tier: HIGH-RISK. Ranking or filtering job applicants is an employment use.
Obligations are phased in; check the current official timeline.
Legal content last reviewed: 2026-09. Legal review recommended.

Required controls: XW-021 risk assessment before deployment, XW-022 AI
inventory, XW-023 supplier oversight, XW-024 risk register; NIST AI RMF
Govern, Map, Measure, Manage.

Inventory record (template.md): id AI-004, owner HR, personal data yes,
risk tier high, approval pending.
Decision needed: approval to proceed.

```findings
[{"type": "high_risk_ai", "id": "AI-004"}]
```
````

The other five systems each get the same section. The website chat that answers shipment questions, for example, tiers as limited-risk because people must be told they are talking to AI. Practice the tiering in [practicum exercise 6](https://evemcgivern.github.io/app-governance-kit/practicum.html#ai-intake).

## Install

See the [repository README](../../../../README.md#install) for Claude Code, Codex, Claude.ai and ChatGPT steps.

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
