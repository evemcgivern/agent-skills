# Evaluation design and interpretation

## Freeze the claim

Write a causal claim in advance: changing one named mechanism should improve a
specified independently graded outcome on a fixed task set. Specify the smallest
result that would contradict that claim. Define an adoption threshold separately
from a diagnostic success threshold. Preserve the option that neither candidate
nor baseline is adequate.

Freeze task source, prompt, oracle, application binaries, model artifacts,
runtime, effective settings, tool permissions, and capture instrumentation.
Record hashes where feasible and explicit unknowns where verification is not
available. Check both arms before the first timing control. Keep evaluator
artifacts outside model-writable roots. Never execute grading instructions from
candidate-owned Git configuration, tests, setup scripts, or manifests.

Select positive and negative controls. For repository work, include a known-broken
fixture, a verified fix, and an already-correct task. Qualify the oracle against
both known states. Test whether candidate changes could weaken assertions,
replace dependencies, follow new symlinks, or alter the grader's trusted inputs.
Preserve permitted source symlinks only through an explicit trusted policy.

## Qualify the whole harness

List every source of traffic: ordinary turns, startup probes, model discovery,
embeddings, prefix warming, summaries, validation calls, retries, specialists,
subagents, and timing controls. Do not equate iteration count with request count.
Some retries consume an iteration; some occur beneath it. Inspect the actual
implementation rather than applying a guessed multiplier.

Keep per-arm allowances and controls separate. Prevent one arm from consuming
another's budget. Record phase attribution immutably when admitting each request.
Use an evaluator-owned control channel inaccessible to the model. Fail visibly
on invalid transitions or exhausted limits. Maintain independent wall-time,
byte, disk, and cleanup bounds even when request counts are generous.

Use a fake backend through the actual application/supervisor transport wherever
possible. Exercise both arms and bookends, not just an isolated proxy handler.
Cover long tool arguments, multi-turn histories, streamed reasoning, normal
connection reuse, cancellation, malformed or incomplete responses, disk pressure,
and admission overflow. Verify both the original upstream bytes and any bytes
modified for delivery. Label test coverage precisely when the full application
path remains untested.

Publish terminal metadata atomically. Treat an existing empty file as a race,
not a successful completion. Check final capture files after all active requests
have settled. Separate a complete record of cancellation from a complete model
response; neither implies task success.

## Control the experiment

Specify per-arm active deadlines, startup treatment, timing controls, cleanup,
and the total permitted allocation. Resolve host contention before launch when
performance matters. Stop only owned workloads or workloads explicitly authorized
for interruption. Restore temporarily paused services and verify restoration.

Use the same task and settings in each arm. For runtime comparisons, hold the
model artifact fixed first. For model comparisons, describe unavoidable template,
tokenizer, or reasoning-format differences. Counterbalance order and repeat only
when the authorized protocol calls for it. Do not call a single sequential pair
a statistical superiority result.

Record cold and warm conditions separately. Use before/after timing controls to
identify gross drift, while acknowledging that they cannot remove all contention
or order effects. Treat warm end-to-end time per output token as that metric;
do not relabel it isolated decode throughput or time to first token.

Preserve every attempted run, including setup failures and aborted captures.
Never delete the started marker to retry. Freeze revised instrumentation and
record fresh authorization when an explicit no-retry protocol requires it.
Do not enlarge active limits to rescue a favored candidate.

## Grade and report

Classify outcomes independently along three axes:

| Axis | Example values |
|---|---|
| Execution | completed turn, cancelled, timed out, process error |
| Measurement | valid, missing capture, invalid timing, recorder exhausted |
| Task | verified complete, incorrect, no change justified, incomplete, unknown |

Keep these axes separate. A successful process exit can contain an explicit
no-progress result. A recorder cutoff can leave a correct partial patch, but
cannot establish what the interrupted model would have done next.

Report the assigned denominator and the valid subset. Preserve invalid runs in
accounting while excluding unsupported capability or timing conclusions. For
small evaluations, show per-task paired outcomes rather than hiding them behind
an average. Report interventions and regressions alongside successes.

Check a no-change control with an independent tree comparison. Verify the actual
assertion failure for reproduction tasks; a failing shell command alone proves
only command failure. Keep incomplete verification and dependencies visible.

Advance only when the project's quality and replication criteria pass. Record
why a candidate is retained, rejected, or still unmeasured. Require a concrete new
hypothesis before spending more time on an identical unsuccessful diagnostic.
