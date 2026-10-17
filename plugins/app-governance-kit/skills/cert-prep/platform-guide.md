# Platform guide: Certification study coach

This tool has no platform integration. It runs in a chat with the Halden demo files attached, and keeps its log in a spreadsheet you control. Nothing here names a vendor module or field, so there is nothing to confirm against a vendor source.

## Where to run it

- **Claude and Codex:** install the skill from the Tools page, then ask for a study session by certification name.
- **Microsoft Copilot:** use the agent instructions and knowledge files from the Copilot download, or paste the chat prompt.
- Attach only files from `demo-estate/`. Do not attach real company data to a study session.

## Where to keep the log

Open `template.csv` in any spreadsheet and add one row per drill. Keep it with your other study notes. The columns are: date, certification, task, data used, rating, gap topic, why it matters, next drill, crosswalk row, and practicum exercise.

## What the tool does not do

- It does not hold or reproduce any certification body's exam questions or course material.
- It does not predict a result. A good run of drills shows you practiced the tasks, not that you will pass.
- It does not know a certification's current exam format. The facts in the field guide were fetched on 2026-09-25; check the certification body's page before booking.

## Sources

- [Certifications field guide](../../field-guide/certifications.md): the six certifications, their tasks, and the sources for their exam formats.
- Certification bodies, as listed in the field guide: IAITAM (CAMP, CSAM, CHAMP), IAPP (AIGP), PeopleCert (ITIL 4 Foundation), Institute of Asset Management (IAM Certificate).
