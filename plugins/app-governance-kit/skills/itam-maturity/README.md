# Itam Maturity

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![Claude Code](https://img.shields.io/badge/Claude%20Code-supported-6B4FBB) ![Codex](https://img.shields.io/badge/Codex-supported-111111) ![ChatGPT](https://img.shields.io/badge/ChatGPT-skill%20upload-74AA9C) ![License](https://img.shields.io/badge/license-MIT-green)

Score an organization's IT asset management maturity across nine process areas, name the three biggest gaps, and produce a 90-day plan tied to ISO/IEC 19770-1 and COBIT BAI09. Use for a baseline assessment or a yearly re-check.

## What it looks like

Example output on the stated scores in the kit's fictional demo estate (1 ad hoc, 5 improving):

````text
Area                                  Score
Governance and policy                   3
Inventory and discovery                 3
Entitlement and license management      1   gap
Lifecycle, request to retirement        2   gap
Vendor and contract management          4
Data quality and reconciliation         1   gap
Risk and security integration           3
Cost and financial management           4
Reporting and improvement               3
Unverified: scores are as stated; no evidence was supplied to support them.

Gaps: entitlement (XW-006, XW-007, XW-008), data quality (XW-026),
lifecycle (XW-009, XW-010). Entitlement and data quality tie at 1;
entitlement goes first because license gaps carry audit exposure.

90-day plan, entitlement
Owner role: software asset manager
Actions: match purchase records to installs for the top ten products;
record an expiry date for every license; review renewals monthly.
Evidence: an entitlement position report for those ten products.
Decision needed: owners and budget.

```findings
[{"type": "maturity_gap", "id": "entitlement"},
 {"type": "maturity_gap", "id": "data-quality"},
 {"type": "maturity_gap", "id": "lifecycle"}]
```
````

Score the same answers yourself in [practicum exercise 2](https://evemcgivern.github.io/app-governance-kit/practicum.html#itam-maturity).

## Install

See the [repository README](../../../../README.md#install) for Claude Code, Codex, Claude.ai and ChatGPT steps.

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
