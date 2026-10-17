# Cert Prep

![Version](https://img.shields.io/badge/version-0.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

[![Claude: full](https://img.shields.io/badge/Claude-full-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-full-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-full-brightgreen)](../../../../README.md#compatibility)

Coach a learner preparing for CAMP, CSAM, CHAMP, AIGP, ITIL 4 Foundation, or the IAM Certificate with scenario drills on the Halden demo estate, then log gaps and plan the next drills. Use for weekly study sessions or a readiness check. Not exam content and not a pass guarantee.

## What it looks like

One drill from a study session. The learner's answers are invented; the device data comes from the kit's fictional demo estate.

````text
Learner: CHAMP. Two years in IT support, 3 hours a week, no exam date.
Coach:   Drill 1: retire hardware with data-wipe evidence. Attach devices.csv.
         Ten devices are marked retired and finance wants the disposal
         closed this week. What do you check first?
Learner: That every retired device has a retirement date.
Coach:   Partial. All ten have dates, but DEV-011 and DEV-042 have no
         confirmed wipe, so the disposal cannot close yet. Wipe or
         destruction evidence comes first (XW-010, retirement and
         decommissioning). Logged as a gap; next drill: practicum 07.
...      (two to four more drills on different tasks)
Coach:   Gaps, most important first: disposal evidence, ...
         This is practice, not a prediction of your exam result.
         Decision needed: which gap to work first, and whether to book.

```findings
[{"type": "knowledge_gap", "id": "disposal-evidence"}]
```
````

The [field guide](https://evemcgivern.github.io/app-governance-kit/field-guide.html#cert-heading) compares the six certifications, and the [practicum](https://evemcgivern.github.io/app-governance-kit/practicum.html) holds the matching exercises.

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
