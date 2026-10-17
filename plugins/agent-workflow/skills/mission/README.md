# Mission

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Keeps a small mission record outside the repository so work can resume cleanly in a later agent session. The record holds the outcome, constraints, milestones, decisions, next action, and hashed evidence files, and is bound to one Git worktree. The bundled script never runs stored actions, starts background processes, or changes Git state, and it uses revision checks and file locks so stale writers fail instead of overwriting state. Use it when asked to start, checkpoint, resume, or complete a mission across sessions.

## What it looks like

Real output, from a throwaway Git repository and state folder. The mission has two milestones, `draft` and `review`. One checkpoint marked `draft` complete with an evidence file. A later session asks where things stand (JSON trimmed to the keys that matter):

```text
$ python3 scripts/mission.py resume release-notes
{
  "inspect_first": "Inspect current effects before acting: effects may be in progress or uncertain",
  "next_action": "Review the draft",
  "next_unfinished": {
    "acceptance": "A second reader signs off",
    "description": "Review draft",
    "id": "review",
    "status": "pending"
  },
  "replay_action": false
}
```

`replay_action` is always `false`: the record says what to do next, and the agent decides whether to do it. Unsafe writes fail with a nonzero exit and leave the record unchanged:

```text
$ python3 scripts/mission.py checkpoint release-notes --expected-revision 1 ...
mission: stale revision: expected 1, current 2

$ python3 scripts/mission.py complete release-notes --expected-revision 2
mission: all milestones must be complete before completing the mission
```

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder; supporting files in it may be required.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `scripts/mission.py` — the mission CLI (Python 3 standard library, POSIX).
- `tests/test_mission.py` — unittest suite for the CLI; run `python3 -m unittest discover -s tests` from this folder.
- `VERSION` and `CHANGELOG.md` — package version history.
