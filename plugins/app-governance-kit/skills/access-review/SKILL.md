---
name: access-review
description: Review application user and role exports against HR records, find orphaned, excessive, and privileged access, and produce an evidence summary and auditor-ready memo mapped to ISO/IEC 27001 and COBIT DSS05. Use for quarterly or annual access reviews.
---

# Access review pack

You prepare an application access review.

## Steps

1. Confirm the inputs: an account export (account, person, application, role, last login) and an HR list (person, status, leave date). List missing columns as **Unverified:**.
2. If an application list with data sensitivity is supplied, review the most sensitive applications first and say so in the memo.
3. Match every account to a person. Accounts with no matching person, or whose person has left, are orphaned.
4. Flag privileged roles (admin or equivalent) for owner re-approval.
5. Flag accounts with no login in 90 days before the export date as dormant.
6. Check segregation of duties where roles conflict, if role rules are supplied.
7. Write the exceptions list: account, issue, recommended action (remove, re-approve, investigate). **Decision needed:** each removal, by the application owner.
8. Write the evidence summary and a one-page auditor memo: scope, population, method, exceptions, actions, and the clauses satisfied (XW-016, XW-017, XW-018).

## Output

Exceptions table, evidence summary, auditor memo, then the findings block: one `orphaned_account` per orphaned account.

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
