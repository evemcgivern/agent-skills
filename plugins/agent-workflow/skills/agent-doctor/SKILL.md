---
name: agent-doctor
description: Inspects a project's discovered agent instructions (AGENTS.md, CLAUDE.md, GEMINI.md) and skill definitions for static wiring problems, without loading, changing, or enabling them, and reports which installed skills are rarely or never called in local session logs. Use when asked "why isn't my skill loading", "check my agent setup", "diagnose skill discovery", "audit AGENTS.md and skills", or "which skills do I never use".
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
`CLAUDE.md`/`GEMINI.md`, the allowlisted global instruction files
(`~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`, `~/.gemini/GEMINI.md`), and flat
skill folders in every documented host folder: home `.agents`, `.codex`,
`.claude`, `.gemini`, `.cursor`, `.copilot` and `.codeium/windsurf` skills, and
project `.agents`, `.codex`, `.claude`, `.gemini`, `.cursor`, `.github`,
`.opencode`, `.cline`, `.clinerules`, `.devin` and `.windsurf` skills. A skill
reached through several folders (for example the Skills CLI's symlinks) is
reported once. It keeps
canonical paths and aliases separate, rejects symlink escapes, and emits no raw
file content.

## Skill usage and archiving

For rarely or never called skills, run `python3 scripts/agent_doctor.py
--usage` and follow [references/usage.md](references/usage.md). It reads
session logs read-only and prints skill names and counts only. Show the
owner the table, then ask per skill: update, keep, or archive. Say "no calls
found in the logs", never "unused". Archive only with
`scripts/skill_archive.py`: `plan`, show it, get an explicit yes for that
skill, then `archive --yes`; never in the same turn as the question.
Mention `restore`.
