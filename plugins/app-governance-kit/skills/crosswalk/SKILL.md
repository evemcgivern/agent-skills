---
name: crosswalk
description: Map a control, requirement, or policy statement to ISO/IEC 19770-1, COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001 clauses, and show where coverage is missing. Use when writing or auditing a control, or explaining how frameworks overlap.
---

# Governance framework crosswalk

You map governance controls across four frameworks using [`crosswalk.csv`](crosswalk.csv).

## Steps

1. Restate the control in one plain sentence. If it bundles several obligations, split it and map each part.
2. Find the best-matching crosswalk row by theme and summary. Name a second row only if it adds a framework the first lacks.
3. For each framework, give the clause number from the row, or "no direct equivalent".
4. Name the gap: which framework has no equivalent, and what an auditor from that framework would ask for instead.
5. If no row fits, say so and propose a new row (theme and one-sentence summary). **Decision needed:** whether to add it.

## Output

A table per control: framework, clause, what it asks for in your own words. Then gaps. Then the findings block, one `crosswalk_match` per control with id `<control label>:<XW id>`.

## Output rules

- Show the reasoning behind each conclusion.
- Mark every point where a person must decide with **Decision needed:** and stop short of deciding.
- Flag any figure you could not verify from the input with **Unverified:**.
- Cite framework clauses by number from [`crosswalk.csv`](crosswalk.csv). Paraphrase; never quote standards text.
- End your answer with a fenced block labeled `findings` containing a JSON list of `{"type": ..., "id": ...}` objects, as the task describes. Use `[]` when there are none.

## Reference files

Read these from this skill's folder when a step needs them:

- `checklist.md`
- `sop.md`
- `platform-guide.md`
- `template.md`
- `crosswalk.csv`
- `themes.md`
