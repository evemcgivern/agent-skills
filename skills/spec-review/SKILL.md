---
name: spec-review
description: Use when a design spec, plan, or requirements doc is drafted/ratified/about-to-be-implemented and you want a rigorous second-model review that verifies the spec's claims against the real codebase — catching wrong data-model assumptions (scalar-vs-M2M), unverified schema/API claims, missing acceptance criteria, ambiguity, and internal contradictions before code is written. The spec-world analog of /codex:review for PRs.
---

# spec-review

## Overview

Runs a **Codex second-model review against a specification document**, the way
`/codex:review` runs Codex against a PR diff. A spec is not a diff — so instead
of `git diff`, this feeds Codex the spec file(s) and runs read-only against the
repo, so Codex can **verify every claim the spec makes against the actual code**
(schema, migrations, types, routes). Review-only: it never edits anything.

Why a different model: it reads the codebase fresh, with no investment in the
spec's framing. The most expensive spec defect is a data-model claim that's
wrong — treating an M2M relationship as scalar, naming a column or field that
doesn't exist. Six agent reviewers reasoning forward from a spec missed exactly
that can be caught when a reviewer verifies the schema before implementation.

## When to Use

- A `design.md` / `requirements.md` / `tasks.md` is drafted or freshly ratified.
- About to write the implementation plan or first code off a spec.
- A spec touches multi-table relationships, schema, or an existing API surface.
- You want an adversarial "does this hold up against reality?" pass.

Not for: reviewing code changes (use `/codex:review`); pure prose/marketing docs.

## Usage

```bash
~/.claude/skills/spec-review/spec-review.sh [TARGET] [-- extra focus text]
```

- `TARGET` = a spec **file**, a spec **folder** (bundles requirements+design+tasks),
  a **bare name** searched across known spec dirs, or **omitted** to auto-detect
  the most-recently-modified spec.
- Text after `--` is appended as extra reviewer focus.
- Output is Codex's verdict **verbatim**. Relay it; do not silently fix the
  findings — the user decides what to act on.

```bash
# explicit file
spec-review.sh docs/superpowers/specs/2026-05-30-foo-design.md
# folder spec (.spec-workflow style)
spec-review.sh .spec-workflow/specs/MVP-plot-lifecycle
# bare name + focus
spec-review.sh plot-lifecycle -- scrutinize the credit-deduction math
# auto-detect newest spec
spec-review.sh
```

## What it checks

Data-model claims (scalar-vs-M2M, missing columns/fields) · untested assumptions
about existing behavior · missing/weak acceptance criteria · ambiguity · internal
contradictions · dependency ordering & migration idempotency · auth/RLS/compliance
· testability & rollback. Each finding is tagged CRITICAL/HIGH/MEDIUM/LOW with
spec-section + verified `file:line` evidence, plus a "Verified OK" list.

## Searched spec dirs (auto-detect / bare-name)

`.spec-workflow/specs`, `docs/superpowers/specs`, `docs/superpowers/plans`,
`docs/specs`, `docs/plans`, `specs`, `plans`. Extend via `SPEC_REVIEW_DIRS`
(colon-separated). Override the model via `SPEC_REVIEW_MODEL`.

## Requirements

- `codex` CLI authenticated (`codex exec` runs non-interactively). The MCP/auth
  lines on stderr are unrelated server noise — the script discards stderr and
  reads the clean verdict from Codex's `-o` output file.
- Run from inside the target git repo (the script `cd`s to the repo root so
  Codex can read the code it's verifying against).

## Common Mistakes

- **Reviewing a spec for a different repo.** Codex verifies against the CWD's
  repo. Run it from the repo the spec targets.
- **Treating findings as auto-fixes.** Review-only. Return the verdict; let the
  human triage. A "DO NOT SHIP" means the spec needs revision, not that you
  start patching code.
- **Huge folder specs timing out.** Large multi-file specs can take minutes;
  give the run a generous timeout.
