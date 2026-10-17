# LLM Engineer

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Diagnoses language-model behavior across the model, its serving runtime, the prompt and context, and the application driving it. It separates task, harness, runtime, agent-policy and model-output failures, then turns the observed failure into one bounded, falsifiable experiment with controls and an explicit budget. Use when asked to "evaluate a local language model", "debug tool calling", "diagnose an agent that keeps exploring", "compare LLM runtimes", or "design an LLM experiment".

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder as `llm-engineer/`; keep every file in it together.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `references/runtime-diagnosis.md` — diagnosing loading, protocol, latency, memory and stopping failures.
- `references/evaluation-design.md` — freezing a claim, qualifying the harness, and grading results.
- `examples/experiment-packet.md` — an experiment template with a synthetic worked example.
- `VERSION` and `CHANGELOG.md` — package version history.
