# Clearly

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)
> In the Claude app and ChatGPT the writing rules work; the --explain video needs a local install, so it uses a diagram or page. On a computer, it asks before installing `manim` and `ffmpeg`.

Plain, short, scannable writing for tired readers, with comma-delimited lists and an optional `--explain` mode that picks a diagram, page, or short video.

## Credits

Adapted from ASD-STE100 (controlled technical English), Strunk's *The Elements of Style*, and the [i-have-adhd](https://github.com/ayghri/i-have-adhd) plugin (MIT, Ayoub Ghriss). See [THIRD-PARTY.md](../../../../THIRD-PARTY.md).

## What it looks like

The same status update before and after the skill. Example output, invented data.

**Before**

```text
Just wanted to give a quick update: basically, the deployment that was being
worked on yesterday has been delayed in order to allow the team to look into
some issues that were identified with the database migration (#6411, #279),
and it should hopefully be ready in a bit, assuming everything goes well.
```

**After**

```text
The deployment is delayed. The database migration failed two checks: 6411, 279.

1. Fix the migration script.
2. Run the two checks again.
3. Deploy when both checks pass. Expected: Thursday.

Next: open 6411 and read the failed check (2 minutes).
```

The answer comes first, each sentence holds one idea, filler is gone, issue numbers sit on one comma line without `#`, "in a bit" becomes a day, and the update ends with one short next action.

## Install

See the [repository README](../../../../README.md#install).
