---
name: rationalization
description: Recommend tolerate, invest, migrate, or eliminate for each application in an inventory, find duplicates and license problems, and summarize savings and risk. Use for portfolio reviews, budget cycles, or post-merger cleanup.
---

# Application rationalization

You rationalize an application portfolio using the TIME model: Tolerate, Invest, Migrate, Eliminate.

## Steps

1. Check the inventory: every app has an id, category, owner or cost. List gaps as **Unverified:**.
2. Find functional duplicates: apps in the same category, or doing the same job under different names. Report each pair once.
3. Check licenses against the `checked_on` date: expired, expiring within 90 days, and entitlements far above users.
4. Score each app on business value (users, category criticality) and technical fit (duplicate, license state). State the scoring you used.
5. Assign TIME. For each duplicate pair, recommend which app to keep and why. **Decision needed:** final keep/retire calls.
6. For every Eliminate or Migrate app, note what data it holds and its sensitivity, and recommend archive, migrate, or delete with a retention period. **Decision needed:** the data owner's disposition call.
7. Summarize: annual cost of Eliminate and Migrate apps as potential savings (a range, not a promise), and the top risks of acting.

## Output

A table of apps with TIME and one-line reason, a duplicates section, a license section, the savings and risk summary, then the findings block: `duplicate_app` per pair (`APP-x+APP-y`) and `expired_license` per expired license.

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
