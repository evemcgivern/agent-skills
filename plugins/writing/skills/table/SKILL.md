---
name: table
description: "Presents information as a well-formed table for comparing options, listing items with shared attributes, summarizing findings across cases, or restructuring prose that already carries repeated fields. Use when the human asks for information as a table. Triggers on /table and on phrases like 'put that in a table', 'tabulate this', 'compare these side by side', 'show me the options in a grid'."
---

# Table

Turn information into a table a human can scan in one pass and act on without
reading back into the prose.

A table earns its place when several things share the same attributes. If the
content is a sequence of steps, a single object's description, or one point
made at length, a table hurts — say so and use prose or a list instead.

## What the output is

A `/table` response is exactly these parts, in this order:

1. **The table.** Markdown pipe syntax. Header row names the attributes.
2. **A source line**, when any cell came from a file, command, or measurement:
   where the values came from, so the reader can check them.
3. **Gaps, if any.** One line naming cells you could not fill and why.

Nothing else. No preamble announcing the table, no restatement of the table's
contents underneath it, no closing summary of what the table shows.

## Choosing rows and columns

**Rows are the things being compared.** One row per item, case, option, file,
model, or record.

**Columns are the attributes they share.** Pick the attributes that would
change the reader's decision. Drop attributes where every row says the same
thing — a constant belongs in a sentence above the table, not a column.

If the natural table has more than about seven columns, it is two tables.
Split it by concern rather than shrinking the text.

## Cell contents

| Situation | Do this |
|---|---|
| Value is unknown | `n/a`, not blank |
| Value is unmeasured vs. genuinely zero | `n/a` for unmeasured, `0` for measured zero |
| Long text | Compress to the distinguishing phrase; full detail goes below the table |
| Numbers with units | Include the unit in the header (`Latency (ms)`), keep cells bare |
| Numbers being compared | Same precision down the column |
| A verdict or status | Put it in the leftmost or rightmost column, never buried in the middle |

Bold the cells that carry the answer — the winning option, the failing case,
the outlier. A reader should find the point without reading every cell.

## Ordering

Sort by whatever makes the table answer its question: severity for findings,
magnitude for measurements, the reader's own order when they supplied a list.
Never leave rows in accidental order.

When the table exists to compare against a baseline, the baseline is the first
row.

## When the request is prose that should stay prose

Say it in one line and give the better form:

> That's a sequence, not a comparison — here it is as steps instead.

Do not build a one-column table, a two-row table with one attribute, or a
table whose cells are full sentences. Those are lists wearing a costume.

## Common mistakes

| Mistake | Fix |
|---|---|
| Restating the table in prose below it | Delete the prose; the table is the statement |
| A column where every cell matches | Move it to a sentence above the table |
| Mixed precision in a numeric column | Round the whole column to the least precise value |
| Blank cells | `n/a`, so the reader knows it was considered |
| Sentences inside cells | Compress to the phrase that differs; detail goes below |
| Announcing "Here is a table:" | Start with the table |
