---
name: efficient-frontier-routing
description: Routes each task to a suitable model tier in Claude Code, Codex, or another agent that can start subagents on a chosen model (for example Gemini CLI or Antigravity CLI), following the user's routing preferences. Keeps small tasks local, delegates discovery, routine coding, and testing to cheaper subagents, and sends difficult decisions and risky reviews to a stronger one. Use when deciding whether to delegate, writing subagent handoffs, or setting routing preferences, or when asked to "save tokens", "use cheaper models", "fan out subagents", "stay inside my quota", or "efficient-frontier-routing help".
---

# Efficient Frontier Routing

Match the model to the work in Claude Code, Codex, or another agent that can
start subagents on a chosen model (for example Gemini CLI or Antigravity CLI),
regardless of the main session's model. A cheaper main session can coordinate
routine work and consult a stronger agent; a stronger main session can
delegate routine work to cheaper agents.
Keep small tasks local when a handoff would cost more than doing the work.

## Help And Configuration

When invoked with `help` or `--help`, read [configuration help](references/configuration.md),
explain the controls and examples, then stop. Do not start delegated work or
change settings for a help request. For configuration questions, read the same
reference; for ordinary tasks, skip it.

Apply routing preferences from the user's request and applicable instruction
files. For this skill's preferences, use explicit task instructions first,
then project preferences, then global preferences, then the defaults below.
Host permissions, model availability, and enforced limits still apply.
Users can choose the discovery, implementation, and review models; per-agent
effort; escalation triggers and retry count; a maximum number of concurrent
subagents; and whether escalation requires approval. Honor a configured model
ceiling or no-delegation preference. If a required review cannot run within
those limits, report the unmet review instead of silently substituting it.
These are instructions interpreted by the assistant, not JSON settings or a
hard spending cap. Do not edit persistent preferences unless requested.

## Workflow

1. Identify decisions requiring stronger judgment: architecture, ambiguity,
   risk, conflicting evidence, and final technical review. Handle them in the
   main session when it is suited to the task; otherwise delegate upward.
2. Identify delegable work: research scans, repository inventory, search, docs
   extraction, browser/testing passes, log reduction, test failure clustering,
   narrow coding, and mechanical edits.
3. Spawn subagents for justified handoffs, parallelizing independent slices
   with clear ownership, bounded scope, verification gates, and evidence.
4. Require compact returns: findings, changed files, commands run, residual
   risk, stop conditions hit, and decisions needing synthesis or escalation.
5. Integrate and review centrally before presenting the result.

## Handoff Packets

Write delegated prompts as self-contained packets. Assume the receiving agent
has not seen the conversation. Include the repo path, objective, scope,
out-of-scope areas, relevant files or search targets, expected return format,
verification commands, and stop conditions.

Useful stop conditions:

- The live code does not match the assumption in the handoff.
- A verification command reaches the configured retry limit (default: two
  failed attempts after reasonable fixes).
- The work appears to require files outside the assigned scope.
- The agent cannot produce concrete evidence for its claim.

## Review Loop

Treat delegated output as evidence to inspect, not a verdict to forward. Reopen
important cited files, skim high-risk diffs, and rerun or spot-check the
verification that matters before claiming completion. If delegated agents
disagree on a difficult technical question, use a stronger reviewer with the
evidence. Keep product choices and scope changes with the user.

## Common Scenarios

Use these as soft suggestions:

- Research: delegate broad repo scans, docs extraction, and source comparison;
  the main session prioritizes the results and escalates difficult judgments.
- Coding: delegate bounded patches, refactors, or mechanical edits when file
  ownership is clear; integrate and review centrally.
- Testing: choose the validation strategy at the appropriate reasoning tier,
  then use cheaper agents to run unit checks, browser flows, screenshots, and
  log reduction. Ask them to return exact commands, failures, likely causes, and
  whether the signal looks flaky, environmental, or product-relevant.
- Debugging: send independent agents after separate theories, logs, or repro
  paths; escalate the diagnosis when the evidence remains conflicting.

## Worked Example

A Sonnet main session gets "fix the failing checkout tests and tighten the
refund rule while you're there", with project preferences of Haiku for
discovery, Sonnet for implementation, Opus at high effort for risky review,
and at most two concurrent subagents.

1. Discovery goes to a Haiku subagent: run the test suite, cluster the
   failures, and return the failing tests, the files they touch, and the exact
   commands. A second Haiku subagent maps where refund logic lives.
2. The failures cluster on a stale fixture. That is a bounded, mechanical fix,
   so the main session makes it locally rather than paying for a handoff.
3. The refund rule touches billing, which is high-risk. Before editing, the
   main session sends Opus (requested explicitly, `effort: high`) a packet
   with the refund files, the proposed change, the current tests, and one
   question: does this change break any existing refund path?
4. The main session applies the change, reruns the tests itself, reopens the
   two files Opus flagged, and reports which model ran each step, so the user
   can see that the stronger review actually happened.

## Tier Matching

Use the host's available models and the user's mappings to choose the cheapest
suitable tier, above or below the main session's model:

| Work | Required capability | Claude examples | Codex and other hosts |
| --- | --- | --- | --- |
| Discovery, summaries, factual checks | Fast, accurate extraction | Haiku | A fast available model suited to factual work |
| Scoped implementation and tests | Reliable coding within established patterns | Sonnet | An available coding model suited to the scope |
| Architecture, deep debugging, risky review | Strong reasoning across systems | Opus, or Fable where available | A stronger available reasoning model |

Claude names are examples for Claude sessions, not aliases to pass to Codex.
Do not invent Codex model IDs or assume a permanent one-to-one mapping between
vendors. Inspect the host's available model choices and use explicit valid
names. Stay with the current provider for ordinary routing unless the user
asks otherwise; apply the separate different-vendor review rule when needed.
Select effort independently from the model and honor the user's effort limits.
Do not default all agents to the highest effort.

A stronger main session can make difficult decisions directly. From a cheaper
session, delegate the difficult decision or review with a compact evidence
packet, then integrate the result and run the required checks. If the host
exposes only one model, keep work on it and report any unmet stronger-review
requirement. Do not claim a higher model tier merely because effort increased.

## Escalation From A Cheaper Main Session

Escalate before implementing an unfamiliar architectural change or a change to
a high-risk invariant, subject to the user's escalation policy. Also escalate
when evidence conflicts or the retry limit is reached (default: two reasonable
attempts on the same technical problem). Reuse gathered evidence;
do not pay for another broad exploration of the same files.

Treat auth, billing, permissions, security, migrations, data loss, shared
state, caching, concurrency, cross-module behavior, public APIs, and
user-visible workflows as high-risk. Use the strongest suitable tier for
the decision or technical review. When the user requires a review by a
different vendor's model for high-risk work, keep that review; it adds a
different model's perspective.

In Claude Code, explicitly request the subagent's `model` in the Agent call or
use a custom agent with `model: opus` (and `effort: high` when appropriate).
An unspecified model can inherit the cheaper main model. Use an ordinary
subagent with a focused handoff; a conversation fork uses the main model.
Check the reported model, using `/tasks` when available. In Codex or another
host, explicitly set the model and reasoning effort through the host's
supported per-agent selector. Use a focused task handoff if inheriting the
full conversation would prevent a model override. Check the reported
selection; if the host cannot select models per agent, report that limitation
instead of simulating routing.

Keep the main session on its chosen model. This is a routing instruction, not
an automatic runtime router or a guarantee that the cheaper model will detect
every hard case. If the required model is unavailable or restricted, report
the limitation instead of silently claiming a stronger review occurred.

## Guardrails

- For an immediate blocker, work locally unless stronger expertise or context
  isolation justifies a sequential handoff. Do independent work while waiting
  when available.
- Do not ask multiple agents to edit the same files at the same time.
- Do not trust subagent conclusions blindly when the risk is high; inspect the
  important evidence yourself.
- Do not claim universal savings. The pattern works best when exploration and
  implementation, testing, or research can be parallelized.

## Default Framing

"I will keep routine work on the current or a cheaper model and delegate
difficult decisions or risky reviews to a stronger agent when needed."
