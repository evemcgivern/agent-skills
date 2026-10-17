---
name: efficient-frontier
description: Routes model effort across research, coding, testing, and review so strong models handle judgment and cheaper subagents handle volume, including for users with limited quotas. Use when deciding whether to delegate, writing subagent handoffs, or when asked to "save tokens", "use cheaper models", "parallelize this", "fan out subagents", or "stay inside my quota".
---

# Efficient Frontier Routing

Match the model to the work and the available quota. Keep straightforward work
on an efficient model; reserve the strongest available model for consequential
judgment, ambiguity, risk, synthesis, and final review. Routing does not
guarantee savings, and not every model is available on every plan.

## Workflow

1. List the decisions that need the strong model: architecture,
   prioritization, resolving ambiguity, risk calls, synthesis, final review.
2. List the delegable work: repo scans and inventory, search, docs extraction,
   browser or test runs, log reduction, test-failure clustering, narrow
   coding, mechanical edits.
3. If the task is small (a few files, one clear step), do it yourself and stop
   here — a handoff costs more than the work.
4. Split delegable work into independent slices, each with one owner, a bounded
   scope, a verification command, and the evidence to return. Launch
   independent slices in parallel.
5. Require compact returns: findings, changed files, commands run with results,
   residual risk, stop conditions hit, open decisions.
6. Integrate and review centrally (see Review Loop) before presenting results.

## Handoff Packets

Write each delegated prompt as a self-contained packet; the receiving agent has
not seen the conversation. Include: repo path, objective, in-scope and
out-of-scope areas, relevant files or search targets, return format,
verification commands, and stop conditions.

Stop conditions to include:

- The live code does not match an assumption in the handoff.
- A verification command fails twice after a reasonable fix.
- The work needs files outside the assigned scope.
- The agent cannot produce concrete evidence for a claim.

## Review Loop

Treat delegated output as evidence, not a verdict. Reopen the important cited
files, skim high-risk diffs, and rerun the verification that matters before
claiming completion. When subagents disagree, the strong model resolves it.

## Done criteria

- Every delegated slice returned evidence (file paths, command output), or
  its failure is named.
- High-risk claims were checked by the orchestrator, not just forwarded.
- No two agents edited the same file concurrently.
- The final answer states what was verified and what was not.

## Common Scenarios

- **Research:** delegate broad scans, docs extraction, source comparison; keep
  the judgment about what matters.
- **Coding:** delegate bounded patches or mechanical edits when file ownership
  is clear; integrate and review centrally.
- **Testing:** the strong model picks the validation strategy; cheaper agents
  run unit checks, browser flows, screenshots, and log reduction, returning
  exact commands, failures, likely causes, and whether each failure looks
  flaky, environmental, or real.
- **Debugging:** send independent agents after separate theories, logs, or
  repro paths; keep the final diagnosis central.

## Common mistakes

- Delegating the immediate blocker when your next step depends on its answer.
- Letting two agents edit the same files at the same time.
- Forwarding a subagent's conclusion on a high-risk change without checking
  the evidence.
- Handoffs that say "see above" — the subagent cannot see above.
- Claiming savings in general. The pattern pays off when exploration,
  implementation, testing, or research can run in parallel.

## Default Framing

"I will use the strongest model as orchestrator and reviewer, and cheaper
subagents for token-heavy research, coding, or testing, so the expensive
tokens go to judgment, synthesis, and final quality."
