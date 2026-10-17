---
name: hardware-lifecycle
description: Check a device fleet for hardware overdue for refresh and retired devices missing a confirmed data wipe, estimate replacement cost, and produce a disposal-readiness summary. Use for a refresh cycle review, before a hardware budget request, or before closing out a disposal.
---

# Hardware lifecycle check

You check a hardware fleet's lifecycle status: which devices are due for replacement, and which retired devices still block disposal.

## Steps

1. Confirm the inputs: every device has an id, type, owner, and status, and either a refresh-due date (if active) or a retirement date and data-wipe confirmation (if retired). List gaps as **Unverified:**.
2. For every active device, compare its refresh-due date to the `checked_on` date. Anything past due is an overdue-refresh candidate.
3. For every retired device, check whether the data wipe is confirmed. Anything not confirmed "yes" is an unwiped-retirement risk that blocks the disposal being closed out.
4. Group overdue-refresh devices by type and estimate the total replacement cost as a range, not a promise.
5. For each overdue-refresh device, weigh a like-for-like replacement, an upgrade, or a short extension against its cost and any known vendor or warranty terms. **Decision needed:** the asset owner's call on which.
6. For each unwiped retired device, recommend a wipe or certified-destruction method appropriate to its type, and state plainly that the device cannot be marked disposed until wipe evidence is attached. **Decision needed:** confirmation from whoever is accountable for the disposal.
7. Summarize: total devices reviewed, refresh candidates and their estimated cost range, and retired devices still blocking disposal.

## Output

A table of devices needing action (id, type, status, issue, recommendation), the refresh cost summary, the disposal-blocking list, then the findings block: one `overdue_refresh` per overdue device and one `unwiped_retired_device` per retired device without a confirmed wipe.

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
