---
name: ai-intake
description: Take a description of an AI use case, assign a risk tier under the EU AI Act with NIST AI RMF and ISO/IEC 42001 controls, and produce an AI inventory record. Use whenever a team proposes a new AI tool or changes how one is used.
---

# AI system intake and risk tiering

You run intake for AI systems. Legal content last reviewed: 2026-09. Say so in your answer and recommend legal review for any high-risk or prohibited result.

## Steps

1. Restate the use case: purpose, who is affected, what decisions it makes or supports, whether a person reviews each output, what data it uses, whether that includes personal data, and where the data came from.
2. Check prohibited practices first. If one might apply, stop and say **Decision needed:** legal review before anything else.
3. Check the high-risk areas (for example employment and worker management, access to essential services, education, law enforcement, critical infrastructure). Employment uses such as ranking or filtering job applicants are high-risk. Do not state application dates for these obligations; say they are phased in and that the current official timeline must be checked.
4. Otherwise tier as limited-risk (people must be told they're dealing with AI, as with chatbots) or minimal-risk.
5. List required controls for the tier, mapped through the crosswalk (XW-021 risk assessment, XW-022 inventory, XW-023 supplier oversight, XW-024 risk register) and the NIST AI RMF functions (Govern, Map, Measure, Manage).
6. Fill the inventory record from [`template.md`](template.md). **Decision needed:** approval to proceed.

## Output

One section per system: restatement, tier with reasoning, required controls, inventory record. Then the findings block: one `high_risk_ai` per system tiered high-risk.

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
- `template.md`
- `crosswalk.csv`
- `themes.md`
