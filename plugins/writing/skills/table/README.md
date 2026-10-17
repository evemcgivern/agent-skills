# Table

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: full](https://img.shields.io/badge/Claude-full-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-full-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-full-brightgreen)](../../../../README.md#compatibility)

Turns information into a table a reader can scan in one pass: rows are the things compared, columns are the attributes that change the decision, unknown cells are marked, and the answer is bolded. It also says when content should stay prose or a list. Use on `/table` or when asked to "put that in a table", "tabulate this", or "compare these side by side".

## What it looks like

A messy comparison turned into a table. Example output, invented data.

**Before**

```text
- option A is $20/mo, deploys from git, has a free tier, no EU region i think
- B: 25 a month, git deploys yes, EU region yes
- option C has a free tier and git deploy, paid plan $7/mo, EU region not sure
we need EU hosting
```

**After**

All three options deploy from git.

| Option | Paid plan (USD/month) | Free tier | EU region | Fits EU need |
|---|---|---|---|---|
| A | 20 | yes | no | no |
| **B** | **25** | n/a | **yes** | **yes** |
| C | 7 | yes | n/a | n/a |

Gaps: B's free tier and C's EU region are not in the list.

Rows keep the reader's order, the shared git-deploy attribute moves to a sentence above the table, unknown cells say `n/a`, the unit sits in the header, the verdict is the last column, and the answer is bold.

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder as `table/`; keep every file in it together.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
