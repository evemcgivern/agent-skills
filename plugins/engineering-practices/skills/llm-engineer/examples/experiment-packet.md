# Experiment packet

- Objective and independent success criterion:
- Observed symptom and evidence path:
- Causal hypothesis:
- Disconfirming result:
- Baseline/candidate revision and artifact hashes:
- Exact task set, known-good/bad controls, no-change control:
- Model/runtime/template/config/tool-set identities:
- Requested versus verified-effective settings; unknowns:
- Offline harness qualification and missing coverage:
- Per-arm/control request accounting and admission limits:
- Active time, startup, cleanup, total allocation:
- Current authorization and retry policy:
- Host/load/cache conditions; ownership of affected services:
- Immutable raw artifacts and trusted grading inputs:
- Outcome categories, comparison method, invalidation conditions:
- Adoption threshold and required fresh confirmation:
- Result, limitations, next action, rollback:

## Worked diagnostic example (synthetic, no model result)

Symptom: repeated reads continue after localization, without a reproduction.
Hypothesis: a bounded validation transition can retain useful evidence while
prompting a discriminating check instead of another unrelated read.
Disconfirming result: novel reads indefinitely reset the transition, the guard
blocks the targeted test, or a denied command is labeled a reproduced defect.

Offline fixture: script legitimate reads followed by a test command against a
small known-broken repository. Repeat against its fixed version. Include a novel
read treadmill, a missing dependency, denied execution, and cancellation. Assert
that a nudge reaches the backend, the command is actually executed when permitted,
its assertion evidence survives compaction, and the fixed control stays unchanged.

Interpretation: passing fixtures establish policy mechanics only. Mark model
selection of the right reproduction as untested. Freeze a separately authorized
live diagnostic before making any model-effectiveness claim.
