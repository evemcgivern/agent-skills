# LLM Engineer

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> In the Claude app and ChatGPT it designs the experiment but cannot inspect your local runtime.

Diagnoses language-model behavior across the model, its serving runtime, the prompt and context, and the application driving it. It separates task, harness, runtime, agent-policy and model-output failures, then turns the observed failure into one bounded, falsifiable experiment with controls and an explicit budget. Use when asked to "evaluate a local language model", "debug tool calling", "diagnose an agent that keeps exploring", "compare LLM runtimes", or "design an LLM experiment".

## What it looks like

The first thing the skill does with a failure is place it in one of five layers, because the fix for each is different. More than one layer can contribute, and the report keeps the proven cause apart from the plausible ones:

| Layer | What failed | Examples |
|---|---|---|
| Task or evidence | The job itself | Missing requirements, an invalid test oracle, stale source, a task that cannot be done offline |
| Harness | The measurement | Incomplete capture, wrong deadlines, grading errors, unequal comparison conditions |
| Runtime or protocol | The serving path | Model loading, chat-template mismatch, streaming framing, tool-call parsing, failed cancellation |
| Agent policy | The application's choices | Repeated exploration, assuming an unavailable tool, discarding evidence, finishing too early |
| Model output | The model | A wrong or thin answer when the harness, configuration and evidence are all sound |

Malformed JSON from a quantized model is not blamed on quantization until the template, parser, runtime and sampling settings have been ruled out.

The answer then comes back in the skill's own wording, which says exactly how far the evidence goes:

> "Offline regression passed" means the policy mechanics work with scripted responses. "Candidate had no patch at cutoff" means the run was interrupted. "Verified task completed" is used only when the task's independent criteria passed.

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder as `llm-engineer/`; keep every file in it together.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `references/runtime-diagnosis.md` — diagnosing loading, protocol, latency, memory and stopping failures.
- `references/evaluation-design.md` — freezing a claim, qualifying the harness, and grading results.
- `examples/experiment-packet.md` — an experiment template with a synthetic worked example.
- `VERSION` and `CHANGELOG.md` — package version history.
