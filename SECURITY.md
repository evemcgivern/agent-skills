# Security

These skills are instructions plus a few shell and Python scripts that agents run on your machine. Read a skill before you install it, and run its scripts only on code you trust.

## Supported versions

Only the latest `main` is supported. Fixes land there and ship in the next release; older releases do not get backported fixes.

## Scope

In scope:

- The shipped shell and Python scripts under `plugins/` and `scripts/`.
- Skill instructions (`SKILL.md` and the files they point to), including anything that could lead an agent to run a harmful command, leak data, or follow instructions planted in content it reads.
- The install guidance in the READMEs and `scripts/install.sh`.

Out of scope: third-party tools a skill tells you to install or run (report those to their maintainers), and the agents themselves.

## Reporting a problem

Report a vulnerability or a harmful instruction through GitHub's private vulnerability reporting: **Security → Report a vulnerability** on this repository. Please do not open a public issue for it.

Include the skill name, the file and line, and what an agent could be tricked into doing. Expect a reply within a week.
