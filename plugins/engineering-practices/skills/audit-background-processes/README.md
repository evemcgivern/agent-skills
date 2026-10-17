# Audit Background Processes

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Inventories stray background processes that long agent sessions leave behind, such as watch loops, `tail -f` on finished logs, orphaned `sleep` calls, and detached runs, and cleans them up without killing anyone else's live work. The rule is to confirm ownership first and kill by PID, never by a broad `pkill -f` pattern. The bundled script reports suspected orphans with PID, parent, age and command, and kills nothing unless you pass `--kill` with specific PIDs that are still on its suspect list. Use it before any pattern-based kill, when a machine feels loaded, or when a run died for no clear reason.

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder; supporting files in it may be required.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `audit.sh` — process inventory that only reports by default; `--kill PID...` sends SIGTERM to named PIDs that are still suspected orphans.
- `VERSION` and `CHANGELOG.md` — package version history.
