# Platform guide: Application governance router

This skill has no platform integration. It routes between the kit's other skills and keeps a routing log in a spreadsheet you control. Nothing here names a vendor module or field, so there is nothing to confirm against a vendor source.

## Where to run it

- **Claude Code:** install the skills from the Tools page. Optionally save the app governance agent to `~/.claude/agents`; it loads this skill.
- **Codex:** install the skills, then describe the task, or type `$app-governance`.
- **Microsoft Copilot:** use the agent instructions and knowledge files from the Copilot download. A Copilot agent cannot call other agents, so the router names the right tool and you open that tool's agent yourself.

## Where to keep the log

Open `template.csv` in any spreadsheet and add one row per request.

## What it does not do

- It does not run tools it cannot reach. If a chosen skill is not installed, it says which one to install.
- It does not merge results from several skills into one verdict. Each skill's output stands on its own.
