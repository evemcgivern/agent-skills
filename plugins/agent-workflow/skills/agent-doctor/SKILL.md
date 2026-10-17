---
name: agent-doctor
description: Inspects a project's discovered agent instructions (AGENTS.md, CLAUDE.md) and skill definitions for static wiring problems, without loading, changing, or enabling them. Use when asked "why isn't my skill loading", "check my agent setup", "diagnose skill discovery", or "audit AGENTS.md and skills".
---

# Agent Doctor

Use this skill to ground diagnosis of agent instructions and skill discovery in
the files actually present. It reports sources as **discovered**, never as
runtime loaded or configured available.

Run the deterministic scan first, then reason only from the report and the
files it names. The scan is read-only and never fixes files, loads skills,
requests permissions, or reads general home, environment, credential, or auth
files.

From this skill's installed directory, run:

```bash
python3 scripts/agent_doctor.py --project <path-to-project> --format markdown
```

Use `--home /fixture/home` for fixture or alternate global discovery. Add an
explicit `--skill-root /path/to/skills` only for additional allowed skill
roots. `--model <name>` takes the model you are running (any literal name,
such as `Claude`, `claude-opus-5-5` or `GPT-5`), compares it to literal "You
are <model>" identity claims in normal skill prose, ignoring case, hyphens
versus spaces or dots, and a leading `claude-`, and reports mismatches as
advisories only. Omit
it to skip that check. Select
`--format json` for machine-readable output. Use `--max-files` and
`--max-bytes`, and `--max-directories` to tighten the bounded scan for a
focused diagnosis.

The scan bounds depth, directories, files, and bytes; it skips dependency, VCS, cache, and
worktree directories. It recognizes ancestor and nested `AGENTS.md`/
`CLAUDE.md`, the allowlisted global instruction files, and flat skill folders
under the project and home `.agents`, `.codex`, and `.claude` folders. It keeps
canonical paths and aliases separate, rejects symlink escapes, and emits no raw
file content.
