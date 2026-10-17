---
name: goal-checklist
description: "Tracks a multi-issue goal as a one-line progress strip: seeds a checklist from issue numbers, adds or drops items, marks state, syncs merged vs shipped from git, and re-emits status unprompted as work advances. Use on /goal-checklist and on phrases like 'where are we on the list', 'status on those issues', 'add #N to the goal'."
---

# Goal Checklist

Turn a list of issue numbers into a single scannable line that updates itself.

The point is not the command. The point is that the human stops asking for
status. Once a checklist is active, you volunteer the strip; they never
request it.

## Symbols

The strip is the store, so the vocabulary is not capped by any tool's state
enum. It is capped by what the human actually needs to tell apart.

**The pipeline**, left to right:

| Symbol | Meaning |
|--------|---------|
| `⬜` | Not started |
| `🔄` | In progress |
| `🟦` | Merged to the integration branch — written and reviewed, not shipped |
| `🚀` | Merged to production and deployed — live, issue closed |
| `✅` | Confirmed working in production |

An item stays `🟦` while a deploy is in flight or has failed — `🚀` requires
the deploy to have finished.

`✅` is never awarded on reasoning alone, only on a run someone watched.
Features can pass every gate and still be dead in production.
Most items stop at `🚀`, which is fine.

**Off-pipeline markers**, which replace the pipeline symbol rather than
adding to it:

| Symbol | Meaning |
|--------|---------|
| `🔍` | Believed fixed, unproven — needs a real run to confirm |
| `⏸️` | Blocked — **must** name the blocker |

`⏸️` is never bare: `⏸️ #104 (blocked on #94)`, not `⏸️ #104`. If the
blocker cannot be named, the item is `⬜`, not blocked. When several items
share one blocker, name it once in full above the strip and let each item
carry the short form — `⏸️ #119 (#130)`.

When a keystone is blocked, say what unblocks it above the strip. A chain
where one decision releases a root that releases five more items is the most
useful sentence the strip can produce, and no arrangement of symbols conveys
it on its own.

**Fractions** for multi-step items: append `n/m` after the number.

```
🔄 #130 1/5
```

Use one only when the steps were enumerated somewhere the human can point
at. An invented denominator is worse than no fraction.

**Annotations** for the one fact that explains the state — an open PR, a
blocker, the missing evidence. Keep it under about five words and put it in
parentheses. Annotate only the items that are not `⬜`.

```
🔄 #106 (PR #135, CI running)
```

**Every `🟦` and `🚀` item carries its merge SHA in parentheses.** This is the
one annotation the tooling reads rather than the human — `--sync` tests it
for ancestry, so an item merged without a recorded SHA can never be checked
and silently stops tracking. Record it at the moment of the merge, when it is
in front of you; recovering it later means searching the log for a squash
commit whose subject may not name the issue at all.

```
🟦 #94 (a1b2c3d4e), #106 (5f6e7d8c9)
```

Short SHAs are fine. When an item has both a SHA and something else worth
saying, the SHA goes first — it is the part that has to survive.

## Storage

Session-only. There is no state file and no cross-session persistence.

**The strip is the store.** The most recently printed strip in the
conversation is the state of record. This works because the strip
round-trips: its symbols, fractions, and annotations encode every item's
state, and the parser accepts its own output. Re-read the last strip, apply
the change, print the new one.

Do not put the checklist in a todo tool, even where one exists. A todo list
carries three states; this vocabulary has seven, so a round-trip through it
would silently flatten `🟦`, `🚀`, `🔍`, and `⏸️` into `completed` or
`pending` and destroy exactly the distinctions the strip exists to make. A
todo tool is fine for the sub-steps of whichever item is `🔄` — those are
not checklist items and never appear in the strip.

Membership is what the store holds; order is computed at render time from
band and issue number, so the store keeps no ordering of its own.

Because state dies with the session, a fresh session re-seeds by pasting the
last strip back in.

## Invocations

| Input | Behavior |
|-------|----------|
| `/goal-checklist 130, 107, 106` | Seed the checklist, replacing any existing one. Print the strip. |
| `/goal-checklist` | Print the strip from current state. Change nothing. |
| `/goal-checklist +140, +141` | Add to the active goal as `⬜`; each lands in its band by number. Print the strip. |
| `/goal-checklist -106` | Drop from the active goal. Print the strip. |
| `/goal-checklist --sync` | Re-derive `🟦` vs `🚀` from git. Print the strip. |
| `/goal-checklist --help` | Print the legend. Change nothing. |

## `--sync`

`🟦 → 🚀` is the one transition a command can settle: a deploy moves many
items at once and needs no action from the human, so it is the one they
forget to report.

Run it on `--sync`, and automatically whenever a deploy is mentioned — not on
every emission, since it can only ever move `🟦 → 🚀`.

**Test each recorded SHA for ancestry, one item at a time:**

```sh
git fetch <remote> <production> <integration> --quiet
git merge-base --is-ancestor <sha> <remote>/<production>   # exit 0 ⇒ 🚀
git merge-base --is-ancestor <sha> <remote>/<integration>  # exit 0 ⇒ 🟦
```

Fetch first. A stale local branch makes every answer wrong in the same
direction — items look unshipped forever.

Discover the branch and remote names from the repo rather than assuming
them. Production is usually `main`, integration usually `dev`, and the remote
is whatever that repo's own deploy tooling addresses, which is not always
`origin`.

**Never use a `production..integration` commit range for this.** On a repo
that squash-promotes, a commit merged to the integration branch never appears
on production under the same SHA, so the range accumulates nearly every
commit ever merged and reports everything as unshipped. On such a repo,
`<production>..<integration>` can list hundreds of commits, most of which
shipped long ago.
Ancestry per SHA is exact; ranges are not.

**Only items carrying a SHA can sync.** An item merged without one recorded
is invisible to this and stays where the human last put it — say so rather
than leaving them to assume it was checked. If a SHA is on neither branch,
report that plainly; it usually means a force-push or a dropped branch, and
guessing a state from it would be inventing history.

`--sync` never touches `⬜`, `🔄`, `🔍`, or `⏸️`. It moves `🟦` to `🚀` and
nothing else.

### Setting state

One verb per pipeline stage, plus the two off-pipeline markers. Each takes
one or more numbers.

| Verb | Sets | Meaning |
|------|------|---------|
| `todo 107` | `⬜` | Back to not started |
| `wip 107` | `🔄` | Working it now |
| `dev 107` | `🟦` | Merged to the integration branch |
| `shipped 107` | `🚀` | Merged to production and deployed |
| `verified 107` | `✅` | Confirmed working in production |
| `check 107` | `🔍` | Believed done, unproven |
| `block 107` | `⏸️` | Blocked on something outside the list |

`wip 130 1/5` sets the state and the fraction together. `wip 106 (PR
#135)` sets the state and the annotation. Both suffixes are optional and
independent.

### Parsing

Accept every form the human might paste:

- `#130`, `130`, and `🟦 #130` all parse to item `130`.
- Separators: comma, whitespace, newline, or any mix.
- Symbols in the input **set** the state, so pasting a previous strip
  restores it exactly — fractions and annotations included.
- Ignore duplicates — a number already on the list is not added twice.
- `+` on a seed-shaped call is harmless; treat a bare add with no active
  checklist as a seed.
- A bare number with no symbol on a re-seed means `⬜`. When re-seeding a
  list that already exists, say which items lost state rather than silently
  resetting them.

## `--help`

Print the legend verbatim and nothing else — no strip, no status block, no
commentary. The one substitution: replace `<integration>` and `<production>`
with the repo's branch names when you have discovered them (see `--sync`):

```
goal-checklist

  pipeline, left to right
    ⬜ not started
    🔄 in progress
    🟦 merged to <integration> — written and reviewed, not shipped
    🚀 merged to <production> + deployed — live, issue closed
    ✅ confirmed working in production — someone ran it

  off-pipeline, replaces the stage symbol
    🔍 believed done, unproven — needs a real run
    ⏸️  blocked — always names the blocker, e.g.
       ⏸️ #104 (blocked on #94). No blocker named ⇒ it is ⬜.

  suffixes
    1/5            fraction, only when the steps were written down
    (PR #137)      one fact explaining the state, ~5 words
    (a1b2c3d4e)    merge SHA — required on 🟦 and 🚀, --sync reads it

  /goal-checklist 130, 107         seed (replaces the list)
  /goal-checklist                  print the strip
  /goal-checklist +141             add to the goal
  /goal-checklist -37              drop from the goal
  /goal-checklist --sync           re-check 🟦 vs 🚀 against git
  /goal-checklist --help           this legend

  wip · dev · shipped · verified · check · block · todo
    set state, e.g.  wip 130 1/5   ·   dev 106 (PR #135)

  🟦 is not 🚀. A closed issue is not a shipped one — where <integration>
  is the default branch, GitHub closes it at that merge, before it deploys.
```

## Output

Two layouts, chosen by size, both closing with the same tally.

**Flowing**, while the items fit on one line — about five or six:

```
⬜ #112, ⬜ #127, 🔄 #94 (PR #137), 🟦 #106 (5f6e7d8c9)
· 2⬜ not started · 1🔄 in progress · 1🟦 on <integration> · 4 total
```

**Grouped**, the moment the flowing form would wrap. One row per band, the
symbol at the row head instead of on every item:

```
⬜ #37, #112, #127, #134, #136
🔄 #130 1/5 (steps 2-5 designed)
🟦 #94 (a1b2c3d4e), #106 (5f6e7d8c9)
🔍 #107 (needs deploy)
⏸️ on #130: #104, #105, #117, #119, #129
· 5⬜ not started · 1🔄 in progress · 2🟦 on <integration> · 1🔍 unproven · 5⏸️ blocked · 14 total
```

Express the threshold as "the items no longer fit on one line", not as a
number.

### Grouped layout rules

- **Bands in lifecycle order, then off-pipeline** — `⬜ 🔄 🟦 🚀 ✅ 🔍 ⏸️`,
  the same order as the tally and `--help`. Omit empty bands entirely; a band
  never renders as an empty row.
- **The row head is the label.** Two characters, no words — the tally
  underneath spells them out.
- **Within a row, issue number ascending.** Always, no exceptions.
- **Items are comma-separated, always** — `⬜ #37, #112, #127` — whether
  or not they carry annotations. The comma sits outside the parentheses, so
  `#94 (a1b2c3d4e), #106 (5f6e7d8c9)` stays unambiguous.
- ` · ` is reserved for a level above items: between blocker sub-groups in
  the `⏸️` row, and between fields in the tally.
- **Factor shared blockers.** When two or more items in the `⏸️` row wait on
  the same thing, collapse them: `on #130: #105, #117, #119, #129`.
  Sub-groups ordered largest first, which puts the critical path at the left
  edge. A blocker unique to one item stays a normal parenthetical. Only the
  grouped layout can show a keystone issue.
- **Wrap inside a row by continuing on the next line with a leading space.**
  Never repeat the row head; a repeated symbol reads as a new band.

### Position

**Band, then number ascending.** That is the whole rule. Nothing holds a
fixed position — the list is not stable, since issues get filed and dropped.

### Tally

```
· 5⬜ not started · 2🔄 in progress · 1🔍 unproven · 5⏸️ blocked · 13 total
```

Rules:

- **The tally is per state, not a fraction.** Count each symbol present and
  omit the states with none.
- **The tally is also the key**, so there is no separate legend line. Scope
  it to symbols actually in use — all seven runs to ~105 columns and wraps
  even on a three-state strip. The full legend stays in `--help`.
- **Labels, in pipeline order, then the two off-pipeline states:**

  ```
  ⬜ not started · 🔄 in progress · 🟦 on <integration> · 🚀 shipped ·
  ✅ verified · 🔍 unproven · ⏸️ blocked
  ```

  Use these words verbatim — not "deployed" or "live" — with
  `<integration>` replaced by the repo's integration branch name.
- Keep the count glued to its symbol (`4⬜`). No abbreviations.
- **The tally line does not wrap.** Let it run long. The item rows wrap;
  this one does not.
- Never pad the tally into aligned columns. `⏸️` and `✅` carry a variation
  selector and occupy one or two columns depending on the terminal, so any
  alignment drifts between machines.
- No heading, no bullet list, no prose restating what the symbols show. The
  strip is the recap.
- When one line would explain the whole picture — a blocker, an overlap
  between two items, a deploy that would move several at once — put that one
  line above the strip, never below it.
- If a bare `/goal-checklist` arrives with no active checklist, say so in one
  line and ask for the numbers. Do not invent a list.

## The standing instruction

Once a checklist is active, **end any response in which an item changed
state with the strip** — unprompted, every time. A change means an item
advanced a stage, picked up or lost a marker, gained a fraction step, or was
added or dropped.

Responses that change nothing get no strip. Do not repeat it turn after turn
while grinding on one item; that is noise, not status.

Placement relative to the status block from the quick-recap skill, if
installed, is set by the repo's agent instructions.

## Working the list

- Mark `🔄` the moment work on an item starts, not when it finishes. More
  than one `🔄` is allowed — real work parks a half-finished item to unblock
  another — but three or more is a signal to say so, not a state to keep
  quiet about.
- Advance one stage at a time and only on the event that earns it: a merge
  for `🟦`, a finished deploy for `🚀`, a real run for `✅`. Never skip a
  stage to make the strip look further along.
- `+` and `-` both change the goal itself, not just the display. `+` adds new
  scope to the active goal; `-` takes scope out of it. Neither disturbs the
  state of the items that remain.
- Added items enter as `⬜` and take their place by band, then number, like
  every other item. Dropped items are gone — removed from
  the list, not marked skipped, and out of the total. Say which numbers you
  dropped in one line above the strip so a mistyped removal is visible
  immediately.
- Never advance an item to make the strip look better. A `⬜` that stays `⬜`
  with a one-line reason is the honest output, and a `🟦` that has sat there
  for days is information — say that a deploy would move five items at once
  rather than quietly promoting them.
- When the human's own account of an item conflicts with the strip, their
  account wins and the strip is wrong. Correct it without argument.
- **An item's scope can move to another issue, which makes any earlier
  description of it stale.** Before holding an item back as partially done,
  read the issues — a newer one may have been filed specifically to take the
  remainder, in which case the original is complete. An hour-old account of
  what an issue covers is not evidence about what it covers now.
