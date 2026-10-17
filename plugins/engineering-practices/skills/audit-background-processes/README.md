# Audit Background Processes

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> The Claude app and ChatGPT cannot run it: they cannot see your computer's processes.

Inventories stray background processes that long agent sessions leave behind, such as watch loops, `tail -f` on finished logs, orphaned `sleep` calls, and detached runs, and cleans them up without killing anyone else's live work. The rule is to confirm ownership first and kill by PID, never by a broad `pkill -f` pattern. The bundled script reports suspected orphans with PID, parent, age and command, and kills nothing unless you pass `--kill` with specific PIDs that are still on its suspect list. Use it before any pattern-based kill, when a machine feels loaded, or when a run died for no clear reason.

## What it looks like

Real output from a report run on a test machine, after starting three throwaway processes and closing the shell that launched them. The other suspects on that machine were login helpers and app agents, which is why you read every line before passing a PID to `--kill`:

```text
=== interactive shells (never kill) ===
  959   958 02-00:17:06 -zsh
81810 81809    03:47:12 -zsh

=== live test and benchmark runs (killing one loses its in-flight work) ===
  none

=== suspected orphans: PID PPID AGE COMMAND ===
3383 1 00:03 sleep 3600
3385 1 00:03 bash -c while true; do sleep 30; done
3387 1 00:03 tail -f /dev/null
... (18 more lines, trimmed: login helpers and app agents)

Read each line before acting. To kill some of them: ~/.claude/skills/audit-background-processes/audit.sh --kill PID [PID...]
```

How to read a row:

| Signal | Safe to kill? |
|---|---|
| `ppid = 1` and it is a watch or `sleep` you started | Yes, by PID |
| `-zsh`, `-bash`, or `zsh -i` | Never, it is someone's terminal |
| A test or benchmark run, even with `ppid = 1` | Ask its owner first |
| You cannot tell whose it is | Ask first |

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder; supporting files in it may be required.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `audit.sh` — process inventory that only reports by default; `--kill PID...` sends SIGTERM to named PIDs that are still suspected orphans.
- `VERSION` and `CHANGELOG.md` — package version history.
