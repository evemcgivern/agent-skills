# Clearly

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

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
