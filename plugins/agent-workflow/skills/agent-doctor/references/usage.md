# Skill usage and archiving

Use this when the owner wants to keep skills fresh: find skills that are
rarely or never called, then offer to update, keep, or archive each one.
Nothing changes without the owner's explicit yes.

## Run the report

From this skill's folder:

```bash
python3 scripts/agent_doctor.py --usage --days 90 --min-uses 3
python3 scripts/agent_doctor.py --usage --format json
python3 scripts/agent_doctor.py --usage --exclude my-keeper --exclude other-keeper
```

| Option | Default | Meaning |
| --- | --- | --- |
| `--days N` | 90 | Window to count calls in (1-3650). |
| `--min-uses K` | 3 | Fewer calls than this is `RARELY USED`. |
| `--format text\|markdown\|json` | markdown | `text` prints the same Markdown table. |
| `--claude-logs DIR` | `~/.claude/projects` | Claude Code session logs. |
| `--codex-logs DIR` | `~/.codex/sessions` | Codex session logs. |
| `--exclude NAME` | none | Skill the owner always keeps; repeatable. |
| `--project DIR` | current folder | Adds the project's `.claude`, `.agents`, `.codex` skills. |
| `--home DIR` | your home | Alternate home, for fixtures. |

Skills listed one per line in `~/.agent-doctor-ignore` or
`<project>/.agent-doctor-ignore` (`#` starts a comment) are left out of the
table and named as "excluded by the owner".

Installed skills come from the same discovery as the wiring scan
(`~/.claude/skills`, `~/.agents/skills`, `~/.codex/skills`, the project
folders) plus the skills of plugins listed in
`~/.claude/plugins/installed_plugins.json`. Plugin skills show as
`plugin:skill`.

## What counts as a call

- **Claude Code.** An assistant `tool_use` named `Skill` with `input.skill`,
  and a `<command-name>/name</command-name>` slash command in a user
  message. A `plugin:skill` call also credits the bare `skill` name. Tool
  definitions, request replays, tool results and assistant text are not
  counted, and a call copied into a resumed session counts once.
- **Codex, best effort.** A tool call whose arguments mention
  `skills/<name>/SKILL.md` (the agent reading the skill), and `$name` in a
  user message. Injected `AGENTS.md` text and harness notices are skipped.
  This is a heuristic: a skill can be used without either sign, and reading
  a skill to edit it also counts.

Lines are prefiltered by substring before JSON parsing, malformed lines are
skipped and counted, and files not modified inside the window are skipped
by modification time. An entry without a timestamp uses its file's
modification time.

## Verdicts

Most concerning first:

| Verdict | Rule |
| --- | --- |
| `NO CALLS FOUND` | No calls found in the logs during the window. |
| `RARELY USED` | Fewer than `--min-uses` calls. |
| `UNKNOWN-WINDOW` | Few or no calls, but the logs reach back less than `--days`: "logs only reach back D days". |
| `NEW` | Installed less than `--days` ago. Never flagged. |
| `ACTIVE` | At least `--min-uses` calls. |

Install time is the lock file's `installedAt`, the plugin registry's
`installedAt`, or else the oldest of the skill folder's creation time and
its folder and `SKILL.md` modification times.

The log window is the shortest reach of the log families present (Claude
Code, Codex), measured from the oldest file modification time or entry
timestamp seen. Say "no calls found in the logs", never "unused".

**Log retention caveat.** Claude Code deletes old transcripts after
`cleanupPeriodDays` (30 days by default), and logs from another machine,
the web, or the mobile app are not on this disk. A short or partial log
history makes skills look idle. Check the reported reach before trusting
`NO CALLS FOUND`.

## Freshness signals

All offline. Listed as `advisory` notes under the table:

- Days since `SKILL.md` changed (table column).
- Lock file entries in `~/.agents/.skill-lock.json`: "installed from
  `<source>`, last updated N days ago: check upstream".
- Broken relative links and missing referenced files.
- Mentions of skills that are not installed (``the `x` skill``,
  ``skill `x` ``, `` `$x` ``).
- Another installed skill with the same name but different content.

Do not guess about content staleness beyond these signals.

## Privacy

The usage mode reads session logs read-only and keeps only skill names,
timestamps and counts. It never prints conversation text, conversation file
paths, or project names. Output names installed skills only.

## Required agent workflow

1. Run `--usage` and show the owner the table, the log reach, and the
   totals.
2. For each `NO CALLS FOUND` or `RARELY USED` skill, ask the owner to choose
   **update**, **keep**, or **archive**. Do not decide for them.
   - **update**: point to the source from the lock file, or run the owner's
     installer only if they ask.
   - **keep**: offer to add the name to `.agent-doctor-ignore`.
   - **archive**: run `plan` first, show its output, and get an explicit
     yes for that skill. Then run `archive --yes`.
3. Never archive in the same turn as the question. Each skill needs its own
   explicit yes.
4. Tell the owner how to restore (the command is in the plan and in the
   archive record).

## Archive and restore

`scripts/skill_archive.py` is the only part of this skill that writes.

```bash
python3 scripts/skill_archive.py plan old-skill other-skill
python3 scripts/skill_archive.py archive old-skill --yes
python3 scripts/skill_archive.py restore old-skill --from ~/.agents/skills-archive/2026-10-17
```

- `archive` moves every installed copy of the skill (from the home and
  project skill folders) to `<archive-root>/<YYYY-MM-DD>/<name>`. Extra
  copies go to `<name>~2`, `<name>~3`. It writes
  `<archive-root>/<YYYY-MM-DD>/<name>.restore.txt` with the exact restore
  command. Default archive root: `~/.agents/skills-archive`
  (`--archive-root` to change it).
- A symlinked skill moves as the symlink itself, never the target's
  contents. A symlink whose target is outside the skill roots is refused
  unless `--follow-symlinks`.
- Refused: no `--yes`; names with path separators, `..`, or other
  non-plain characters; plugin skills (`plugin:skill`, or a name only a
  plugin ships, or a symlink into the plugin folder). Uninstall or disable
  the plugin instead.
- Moves use rename only, so nothing is copied and deleted. An archive root
  on another disk fails with exit 4 and nothing moves.
- `restore` moves the copies back and keeps the record. It refuses if the
  original location is occupied or the record points outside the skill
  roots.

| Exit code | Meaning |
| --- | --- |
| 0 | Success, or a plan was printed. |
| 1 | Refused (see above), or the destination already exists. |
| 2 | Bad command line. |
| 3 | Skill or archive record not found. |
| 4 | A move failed; nothing for that skill moved. |
