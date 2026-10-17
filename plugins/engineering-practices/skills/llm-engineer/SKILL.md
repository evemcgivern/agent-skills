---
name: llm-engineer
description: "Evidence-based diagnosis of language-model behavior, serving/runtime configuration, tool-call protocols, and agent evaluation, turning a failure into a bounded, falsifiable experiment. Use when asked to 'evaluate a local language model', 'debug tool calling', 'diagnose an agent that keeps exploring', 'compare LLM runtimes', 'test context compaction', 'measure a prompt change', or 'design an LLM experiment'."
---

# LLM Engineer

Diagnose the interaction between a language model, its serving runtime, its
prompt and context, and the application driving it. Turn an observed failure
into a bounded, falsifiable experiment. Optimize verified task completion and
useful recovery before optimizing throughput or reducing intervention counts.

Apply this skill as a workflow for the current assistant. Treat a skill as
instructions, not as a newly registered agent type or a different model.
Use an available specialist only when a bounded independent review warrants it.
Preserve the user's chosen main model and existing routing preferences.

## Define the assignment

Start with a concrete symptom, the user's intended outcome, and the evidence
already available. Distinguish requested implementation, read-only diagnosis,
offline testing, and authorized live inference. Carry existing authorization
forward; avoid requesting the same permission twice. Treat a no-rerun instruction
or an exhausted explicit experiment allowance as binding.

Extract the task's acceptance criteria before inspecting model output. Identify
what would prove success independently: an externally controlled test, a checked
repository change, an accurate sourced answer, or a justified no-change result.
Do not let a model-authored test, summary, or completion label redefine success.

Classify the assignment by its primary uncertainty:

- Use this workflow for model behavior, context handling, tool protocols,
  serving compatibility, quantization comparisons, and experiment validity.
- Consult an AI-application specialist, if one is available, for application
  architecture, retrieval integration, orchestration interfaces, or
  product-level agent design.
- Consult an ML-engineering specialist, if one is available, for training
  pipelines, datasets, feature engineering, model packaging, and general
  serving operations.
- Consult backend or security reviewers when the change crosses authorization,
  process ownership, persistence, isolation, or shared-state boundaries.

Keep narrow debugging local when a handoff would add more work than it saves.
Give any reviewer a bounded question, exact evidence, allowed tools, and a return
contract. Do not recruit a domain agent merely because its name appears in an
inherited task template.

## Ground the system

Read the repository's instructions, current configuration schema, relevant source,
and tests. Treat dated notes and previous benchmarks as pointers to evidence,
not current host state. Check what is actually installed and loaded before making
runtime or model claims. Never infer identity from a display label alone.

Record the artifact revision or hash, quantization, tokenizer and chat template,
runtime build, requested context, effective sampling parameters, concurrency,
and exposed tool set. Separate requested settings from values confirmed in the
actual request or serving response. Record unavailable fields as unknown.

Use local source and installed help for implementation details. Verify changing
compatibility claims against official documentation or model/runtime sources
when external research is needed. Date those claims. Keep rankings, prices,
model IDs, and version-specific workarounds out of durable guidance unless they
are explicitly scoped and supported by evidence.

Read [runtime diagnosis](references/runtime-diagnosis.md) when investigating
loading, streaming, reasoning, tool calls, latency, memory, or cancellation.
Avoid changing the model and runtime together when trying to attribute a result.

## Separate failure layers

Reconstruct one complete attempt from input through terminal state. Identify the
last verified successful boundary, then test the next boundary. Distinguish:

1. **Task or evidence failure:** missing requirements, an invalid oracle, stale
   source, inaccessible dependencies, or a task that cannot be completed offline.
2. **Harness failure:** incomplete capture, wrong deadlines, bad accounting,
   grading errors, instrumentation changes, or invalid comparison conditions.
3. **Runtime or protocol failure:** model loading, template mismatch, streaming
   framing, tool-call parsing, context rejection, queueing, or failed cancellation.
4. **Agent-policy failure:** repeated exploration, unavailable-tool assumptions,
   discarded evidence, premature completion, or inappropriate fallback.
5. **Model-output failure:** an incorrect or insufficient response despite a
   functioning harness, supported configuration, and adequate task evidence.

Allow multiple contributing causes. Label the demonstrated cause separately
from plausible contributing factors. Preserve errors and unsuccessful attempts;
do not erase them through reruns or report only the best completion.

Check observable state before declaring a process stopped. A terminal result,
process check, and empty serving queue answer different questions. Do not treat
an idle UI, a missing log update, or a client disconnect as proof generation ended.

## Diagnose exploration without forcing edits

Distinguish useful localization evidence from progress toward completion. A newly
read file or scope can be relevant evidence without advancing reproduction,
implementation, or verification. Preserve legitimate observations through
compaction; do not require discarding them to detect a stall.

Build an evidence chain: task requirement, suspected behavior, relevant symbol
or call path, attempted reproduction, observed result, next discriminating action.
Separate an observed failing assertion from a shell error, denied tool, missing
package, timeout, or an unsupported diagnosis written in prose.

For an exploration loop, inspect whether the retained context states a specific
question and a concrete next action. Prefer a narrow reproduction or a precise
blocker once enough localization evidence exists. Preserve read-only tasks and
already-correct controls. Never require a code edit solely because a counter or
elapsed-time threshold was reached.

Test at least four trajectories offline: legitimate new localization that leads
to a reproduction; an endless sequence of novel but unproductive reads; a failing
reproduction that supports a patch and independent verification; and a correct
implementation that should remain unchanged. Add missing-dependency and denied-
tool cases when they affect the actual failure. Check behavior after compaction
and cancellation, not just the initial prompt text.

Use scripted model responses to prove the application follows its policy and
preserves evidence. State explicitly that scripted responses cannot establish
whether a real model will choose those actions. Reserve model-effectiveness
claims for a valid live evaluation under the authorized budget.

## Design the smallest decisive experiment

Write one causal hypothesis and a result that would disprove it. Freeze a baseline
and one change. Select task instances and negative controls that exercise the
mechanism rather than merely resemble the motivating prompt. Keep criteria and
grade inputs under evaluator control and outside the agent's writable workspace.

Use [evaluation design](references/evaluation-design.md) to define provenance,
budget, accounting, controls, artifacts, and advancement gates. Prepare a concrete
packet using [the experiment template](examples/experiment-packet.md). Do not
invent measurements to fill its fields; use unknown or not run.

Qualify the evaluator before spending inference time. Prove the known-broken
control fails and a known-good control passes. Exercise the complete transport
and supervision path with a fake endpoint, including both comparison arms,
auxiliary calls, long messages, multi-turn tool use, cancellation, and overflow.
Do not assume a passing proxy unit test validates the application/runtime exchange.

Separate per-arm and control allowances. Account for warming, embeddings, model
listing, summarization, retries, and delegated inference as well as ordinary
iterations. State when a limit is merely an operational admission cap rather than
a proof all enabled paths fit. Bound elapsed time, request count, disk use, and
cleanup independently. Never silently enlarge a frozen limit during a run.

Launch live inference only within the user's current scope and allowance. Keep
original attempts intact. Stop at the specified failure or exhaustion condition.
Do not turn an infrastructure failure into an unapproved retry, or spend unused
budget on a new hypothesis without checking the applicable scope.

## Interpret results and implement carefully

Compare the complete assigned set, including failures, interruptions, and controls.
Separate finished, incorrect, blocked, cancelled, timed out, and instrumentation-
invalid outcomes. Report the state at cutoff without predicting the unobserved
remainder. Do not compare speed across invalid timing controls or unequal workloads.

Prioritize independently verified completion, regressions, unnecessary changes,
human interventions, recovery quality, and truthful terminal states. Report latency,
context use, memory, and cleanup with their measurement method and uncertainty.
Avoid treating more tokens, more reads, lower latency, or a passing build as a
proxy for task completion. Do not infer quantization damage solely from malformed
JSON until template, parser, runtime, and sampling causes are checked.

Implement the smallest change supported by the diagnosis. Preserve tool-level
permissions, protected paths, existing escalation gates, and explicit overrides.
Use meaningful regressions that fail without the fix. Keep behavior changes and
harness repairs separately attributable; retain old binaries and frozen inputs
when repairing instrumentation.

Require held-out or fresh-task confirmation and a no-change control before broad
adoption when the project calls for them. Treat a single diagnostic pair as limited
evidence. Prepare a reversible configuration change and verify the actual installed
artifact after an authorized rollout. Keep deployment claims separate from build,
commit, merge, installation, and runtime verification.

## Return a compact engineering decision

Lead with the observed outcome and the next justified action. Include:

- The symptom, verified cause, and unresolved hypotheses.
- Exact evidence locations, revisions, commands, and completed checks.
- Results against frozen criteria, including excluded or interrupted work.
- Whether the evidence supports a harness fix, application fix, live experiment,
  adoption, or no change.
- Remaining work, its budget or prerequisites, and rollback where relevant.

Use precise wording: “offline regression passed” for policy mechanics,
“candidate had no patch at cutoff” for an interrupted run, and “verified task
completed” only when the task's independent criteria passed. Keep speculative
model capability claims out of the conclusion.
