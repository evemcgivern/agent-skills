# Spec Workflow Drift

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

> **Requires the [spec-workflow MCP server](https://github.com/Pimzino/spec-workflow-mcp)** by Pimzino. Install and configure it first. This skill reads the `.spec-workflow/` directory that the server creates; it does not call the server's tools. This skill contains none of the server's code; the server is a separate project under its own license (GPL-3.0 at the time of writing).

Compares the specs in `.spec-workflow/` with the code. It maps which source files each spec covers, lists files no spec documents, flags specs with no recent implementation activity and critical files (auth, AI safety, licensing rules) that lack a spec, and writes a coverage report. Use on `/spec-workflow-drift` or when asked to "check spec drift", "show spec coverage", or "which files aren't in any spec".

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder as `spec-workflow-drift/`; keep every file in it together.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
