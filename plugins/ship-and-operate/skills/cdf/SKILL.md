---
name: cdf
description: Use when the user types /cdf or $cdf, or asks for issue numbers "comma-delimited". Output any list of GitHub issues as one plain comma-separated line of numbers, nothing else added.
---

# CDF (comma-delimited format)

Output issue lists as a comma-separated line so they paste straight into
`gh`, a track file, or another prompt.

## Rules

- Numbers only, no `#`: `6411, 279, 4544`.
- One line, `, ` between items. No bullets, no table, no trailing comma.
- Keep the user's order. Drop duplicates.
- Lead with the list. One short line after it only for things the list
  cannot carry (e.g. "9149 is a PR"). No recap.
- Empty result: write `none`.

## Combining with another request

`/cdf` works on top of any other ask. Do the ask, then present the issue
output in this format.

- "what's still open? /cdf" → only the open numbers, one line.
- "open vs closed /cdf" → two lines, each labeled: `Open: 1, 2` and
  `Closed: 3, 4`.
- Bare `/cdf` after a prior answer → reformat the issues from that answer.

## State must be live

If the list depends on open/closed state, check it with `gh` first. Never
answer from memory.
