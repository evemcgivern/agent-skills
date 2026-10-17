# Spec Workflow Drift

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: partial](https://img.shields.io/badge/Claude-partial-yellow)](../../../../README.md#compatibility) [![Codex / ChatGPT: partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-partial-yellow)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-full-brightgreen)](../../../../README.md#compatibility)
> Claude: Works in Claude Code; the Claude app has no access to your repo. Codex / ChatGPT: Works in Codex; ChatGPT has no access to your repo.

> **Requires the [spec-workflow MCP server](https://github.com/Pimzino/spec-workflow-mcp)** by Pimzino. Install and configure it first. This skill reads the `.spec-workflow/` directory that the server creates; it does not call the server's tools. This skill contains none of the server's code; the server is a separate project under its own license (GPL-3.0 at the time of writing).

Compares the specs in `.spec-workflow/` with the code. It maps which source files each spec covers, lists files no spec documents, flags specs with no recent implementation activity and critical files (auth, AI safety, licensing rules) that lack a spec, and writes a coverage report. Use on `/spec-workflow-drift` or when asked to "check spec drift", "show spec coverage", or "which files aren't in any spec".

## What it looks like

Example output, invented data. A full report starts with the totals, flags any security-relevant file that no spec covers, and ends with prioritized actions:

```markdown
# Spec-Workflow Drift Report

**Generated:** 2026-03-02T09:00:00Z
**Project:** <project>
**Total Specs:** 8 active
**Total Files:** 142
**Coverage:** 89% (126/142 files)
**Drift Files:** 16

🚨 CRITICAL DRIFT DETECTED

The following critical files are not documented in any spec:

- src/lib/rate-limit.ts (SECURITY: rate limiting)

## 🎯 Action Items

1. **Immediate:**
   - Document 1 critical file
2. **This Sprint:**
   - Create a utility spec for 4 infrastructure files
3. **Monitor:**
   - 1 aging spec (no activity in 41 days)
```

How a spec's age is judged, from the date of its last implementation log entry:

| Last logged activity | Status |
|---|---|
| 30 days or less | ACTIVE |
| 31 to 90 days | AGING |
| More than 90 days | STALE |

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder as `spec-workflow-drift/`; keep every file in it together.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
