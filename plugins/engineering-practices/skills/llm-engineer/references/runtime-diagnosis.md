# Runtime and behavior diagnosis

## Establish identity and ownership

Record the exact artifact location/revision and effective served identifier.
Check loaded models and queues using supported read-only interfaces. Distinguish
a requested model name, a loaded alias, and the underlying artifact. Verify
quantization, tokenizer, template and context separately when exposed.

Record the application, serving backend, wrapper/parser, and transport versions.
Inspect private configuration selectively; do not dump credentials or unrelated
host settings. Preserve model residency and other people's services unless
interruption is authorized. Do not accept licenses or download replacement
weights as an incidental diagnostic step.

## Reproduce a protocol failure

Capture the smallest representative exchange, including tool definitions,
request settings, raw streamed frames, returned tool arguments, and follow-up
tool results. Use synthetic nonsecret content for fixtures. Keep authentic
private traces local and outside candidate write access.

Check these boundaries in order:

1. Serialize the intended request and verify its actual model/settings.
2. Confirm the backend accepts the request and emits its advertised format.
3. Parse complete and fragmented frames, including terminal markers.
4. Assemble tool calls and reasoning separately from user-visible content.
5. Execute only supported tools through normal approval and isolation.
6. Return tool results with matching identifiers in the next model request.
7. Confirm terminal state and cancellation on both client and server.

Test normal HTTP connection reuse as well as connection closure. Check chunked
transfer boundaries and long bodies rather than assuming one socket read equals
one frame. Preserve original bytes if a recorder changes transport headers.
Avoid bypassing the application's real client solely to obtain a passing smoke
result.

Compare direct-backend success with application success only to localize a
boundary. Do not treat a direct API response as proof that agentic multi-turn
behavior works through the application.

## Diagnose latency and memory

Separate queue delay, model loading, prefix preparation, first response, generation,
tool execution, compaction, verification and cleanup. Report end-to-end task time
alongside component timings. Distinguish token counts reported by the backend
from estimates derived from characters or text prefixes.

Record context growth, cache state, memory pressure and concurrent work. Include
weights, KV cache and serving overhead in memory observations where measurable.
Do not infer throughput from parameter count or infer practical memory from the
artifact file size alone. Treat shared/unified-memory observations carefully;
process RSS and device allocation may overlap or omit important consumers.

For a quantization hypothesis, first rule out mismatched templates, context
settings, parser behavior and sampling. Compare the same workload with controlled
conditions. Label estimated memory and vendor-reported throughput explicitly.
Do not assume a larger or denser model is the better coding agent.

## Diagnose a reasoning or stopping failure

Inspect what evidence reached the model at each turn, especially after compaction.
Check whether the objective, constraints, investigated ranges, reproduction result,
changed files and next action remain accessible. Distinguish missing evidence
from evidence the model received but failed to use.

Track stages rather than only activity counts: localization, attempted validation,
reproduced defect, candidate change, independent verification, and handoff.
Allow legitimate backtracking and already-correct conclusions. Avoid promoting
source novelty or any nonzero exit into a validated milestone.

When a model keeps exploring, test a targeted next-action prompt or policy with a
scripted backend first. Verify that the tool guard actually admits the requested
reproduction. A policy that asks for a test while blocking its command is a
harness defect, even if its wording sounds reasonable.

Keep cancellation, denied access, unavailable dependencies and application
assertion failures distinct. Report the exact blocker rather than suggesting
unrelated model changes as a generic recovery. Do not ask for already-accessible
source unless a demonstrated access failure explains the request.

## Validate the fix at the right level

Use protocol fixtures for serialization and parsing, real temporary repository
tools for agent-policy tests, and an independently graded live task for model
behavior. Prove the regression fails without the change. Include no-change and
failure controls. Label an offline fixture result as an application guarantee,
not proof of improved local-model performance.
