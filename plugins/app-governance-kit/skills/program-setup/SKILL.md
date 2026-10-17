---
name: program-setup
description: Design or review the launch of a governance body such as a software governance council, ITAM steering group, or AI governance board — charter, decision rights, membership, intake path, cadence, 90-day launch plan, and success measures. Use when starting a council or when an existing one has become a bottleneck or a rubber stamp.
---

# Stand up a governance program

You help stand up a governance body that makes real decisions without becoming a bottleneck.

## Mode

If given a draft charter, review it against the steps below and report gaps. Otherwise ask for: the body's purpose, the organization's size, who would sponsor it, and what currently goes wrong without it. Then draft.

## Steps

1. Purpose: one sentence on what goes wrong today that this body fixes.
2. Sponsor: an executive who controls the relevant budget. No sponsor means no enforcement; flag it.
3. Decision rights: what the body decides, what it only advises on, and the thresholds (cost, risk, AI use) that send an item to it. Everything below threshold is decided by a named role, not the council.
4. Membership: 5–9 voting members (typically IT, security, procurement, finance, legal, architecture, one or two business leads). More than 9 voting members slows decisions; move the rest to non-voting or consulted.
5. Intake path: one request form; triage by a named role; only exceptions, high-cost, and high-risk items reach the meeting.
6. Enforcement: procurement will not buy what the body hasn't approved above threshold. Overlaps with other boards (for example an architecture review board) are settled in writing.
7. Cadence and agenda: meeting frequency, standing agenda, decision log, and an out-of-cycle path for urgent items.
8. Escalation: where disputes go and who breaks ties.
9. Success measures: time from request to decision, share of software bought through the intake path, savings, and exceptions granted.
10. 90-day launch plan: charter approval, members named, intake live, first three meetings, first metrics review. **Decision needed:** sponsor sign-off.

## Output

Draft mode: the charter from [`template.md`](template.md), the decision-rights table, and the 90-day plan. Review mode: a gap table (step, what's missing, why it matters, fix). Either way, end with the findings block: one `charter_gap` per gap found, using the slugs decision-rights, sponsor, membership-size, intake-path, cadence, metrics, escalation. Those seven are the only slugs a `charter_gap` finding may use; a gap that doesn't fit one of them still belongs in the gap table, just not in the findings block.

Present any drafted charter wording as plain text or in a table, not in quotation marks.

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
