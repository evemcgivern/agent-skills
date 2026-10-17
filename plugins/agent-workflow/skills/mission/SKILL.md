---
name: mission
description: "Persist a small, worktree-bound mission record across agent sessions: outcome, constraints, milestones, decisions, next action, and hashed evidence files. Use when asked to \"start a mission\", \"record where we are\", \"resume the mission\", \"checkpoint progress\", or \"mark the mission complete\". For continuity only, not task execution, delegation, or a background daemon."
---

# Mission continuity

Use this skill when work needs durable continuity across sessions. It records a bounded mission outside the repository and reports its next unfinished step. It never executes a stored action, replays a command, starts a background process, delegates work, or changes Git state.

Resolve the script from the location of this loaded `SKILL.md`: its sibling `scripts/mission.py`. Do not derive the path from `$0`, assume a Claude-only environment variable, or run a task string through a shell. The script emits JSON on stdout and concise errors on stderr.

Use native goal tools only when the user explicitly asks to create or manage a goal. This skill must not automatically create or replace one. Use your usual delegation approach for handing off work, and an acceptance-evidence skill such as `prove-it` from the [stylusnexus agent-plugins marketplace](https://github.com/stylusnexus/agent-plugins), if installed, for proving outcomes; mission owns continuity only.

## Create

Run from the intended Git worktree. `create` takes one outcome, zero or more constraints, one or more milestones, and a next action. A milestone is `id|description|acceptance`; IDs use lowercase letters, digits, and hyphens.

```sh
python3 <this-skill-directory>/scripts/mission.py create release-notes \
  --outcome "Publish accurate release notes" \
  --constraint "Do not change source files" \
  --milestone "draft|Draft notes|Notes name every user-facing change" \
  --next-action "Draft the release notes"
```

State defaults to `~/.local/state/agent-missions`. Use `--state-dir <external-directory>` for isolated tests or an explicitly chosen state location. The record is bound to the canonical Git worktree root and common Git directory, and stores only initial/current local HEAD provenance. A normal HEAD advance is a warning, not a blocker.

## Inspect and continue

`show <mission-id>` returns the record and provenance. `resume <mission-id>` returns the next unfinished milestone, recorded next action, and relevant changes. It always returns `replay_action: false`. For `in_progress` or `blocked` missions, inspect the work's actual effects before taking action; blocked records require a reason.

Use `checkpoint` to record a new status (`pending`, `in_progress`, or `blocked`), decisions, next action, milestone status, and optional evidence artifacts. Every mutation needs the revision returned by the prior response, so concurrent or stale writers fail safely instead of overwriting state.

```sh
python3 <this-skill-directory>/scripts/mission.py checkpoint release-notes \
  --expected-revision 1 --status in_progress \
  --milestone-status draft=complete \
  --evidence draft=/tmp/release-notes-draft.txt \
  --decision "Use customer language" \
  --next-action "Review the draft"
```

Each completed milestone needs at least one `--evidence milestone-id=/explicit/output-file` in the checkpoint that marks it complete. Evidence is an explicitly named existing non-symlink file outside the repository. The script stores its canonical path, SHA-256 hash, and local file identity with that milestone; completion rejects a changed, symlinked, or repository-resolving artifact. Re-registering the exact same artifact is idempotent, while re-registering a changed path is rejected. It does not scan directories or store Git remotes or secrets. A blocked milestone also needs `--milestone-blocked-reason milestone-id=reason`.

## Complete

Mark a mission complete only after every milestone is `complete` and all its
registered evidence files still match their recorded identities and hashes.
Optional `--evidence milestone-id=/file` adds another artifact to an existing
milestone; it cannot replace changed evidence.

```sh
python3 <this-skill-directory>/scripts/mission.py complete release-notes \
  --expected-revision 2
```

Recorded evidence shows that a file existed unchanged at completion. It is not independent proof that the stated outcome is true. Completed records are immutable; create a distinct mission for explicit new scope.

## Failure handling

The CLI uses nonblocking POSIX advisory locks and atomic replacement. Lock contention, stale revisions, a mismatched worktree, unsafe state symlinks, missing or changed evidence, and corrupted JSON return a nonzero error without overwriting state. POSIX `fcntl` locks are released by the operating system when a crashed process exits; use a POSIX host for this CLI.
