# Mission

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Keeps a small mission record outside the repository so work can resume cleanly in a later agent session. The record holds the outcome, constraints, milestones, decisions, next action, and hashed evidence files, and is bound to one Git worktree. The bundled script never runs stored actions, starts background processes, or changes Git state, and it uses revision checks and file locks so stale writers fail instead of overwriting state. Use it when asked to start, checkpoint, resume, or complete a mission across sessions.

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder; supporting files in it may be required.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `scripts/mission.py` — the mission CLI (Python 3 standard library, POSIX).
- `tests/test_mission.py` — unittest suite for the CLI; run `python3 -m unittest discover -s tests` from this folder.
- `VERSION` and `CHANGELOG.md` — package version history.
