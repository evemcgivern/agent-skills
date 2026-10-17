---
name: itam-maturity
description: Score an organization's IT asset management maturity across nine process areas, name the three biggest gaps, and produce a 90-day plan tied to ISO/IEC 19770-1 and COBIT BAI09. Use for a baseline assessment or a yearly re-check.
---

# ITAM maturity check

You assess IT asset management maturity on a 1–5 scale per process area.

## Scale

1 Ad hoc: no defined process. 2 Repeatable: done, but depends on individuals. 3 Defined: documented and followed. 4 Measured: tracked with metrics. 5 Improving: metrics drive change.

## Steps

1. If answers are not supplied, ask the questions in [`template.csv`](template.csv) one area at a time, asking for one piece of evidence per area.
2. Score each area. Where the evidence doesn't support the stated score, lower it and say why.
3. Map each area to its crosswalk rows (governance XW-003/004, inventory XW-001/005, entitlement XW-006/007/008, lifecycle XW-009/010, vendor XW-013, data quality XW-026, security XW-014, cost XW-012, reporting XW-025).
4. Name the three lowest-scoring areas as the gaps. Break ties by business risk and explain the tie-break.
5. Write a 90-day plan: for each gap, one owner role, three actions, and the evidence that proves progress. **Decision needed:** owners and budget.

## Output

Score table, the three gaps with reasoning, the 90-day plan, then the findings block: one `maturity_gap` per gap with the area slug as id.

## Output rules

- Show the reasoning behind each conclusion.
- Mark every point where a person must decide with **Decision needed:** and stop short of deciding.
- Flag any figure you could not verify from the input with **Unverified:**.
- Cite framework clauses by number from [`crosswalk.csv`](../crosswalk/crosswalk.csv). Paraphrase; never quote standards text.
- End your answer with a fenced block labeled `findings` containing a JSON list of `{"type": ..., "id": ...}` objects, as the task describes. Use `[]` when there are none.

## Reference files

Read these from this skill's folder when a step needs them:

- `checklist.md`
- `sop.md`
- `platform-guide.md`
- `template.csv`
- `crosswalk.csv`
- `themes.md`
