# Halden Logistics Demo Estate

Halden Logistics is a fictional logistics and transportation company created for testing and demonstration purposes. The demo estate contains nine generated data files representing a complete software and AI governance scenario with deliberately planted problems for tools to discover and correct.

**Generated files:**
- `apps.csv`: id, name, vendor, category, annual_cost_usd, users, data_sensitivity — 60 applications with confidential and internal sensitivity levels
- `licenses.csv`: id, app_id, entitlements, expiry, checked_on — licensing records (checked_on: 2026-09-01)
- `employees.csv`: id, status, termination_date — 80 employee records with active and terminated statuses
- `accounts.csv`: id, employee_id, app_id, role, last_login — 120 user accounts linking employees to applications
- `ai-systems.csv`: id, owner, description — 6 AI systems in use across the organization
- `maturity-answers.csv`: area, label, score — ITAM maturity assessment scores across 9 governance areas
- `controls.md`: 3 sample controls for mapping to external frameworks
- `council-draft.md`: A draft software governance council charter with intentional gaps

The `answer-key.json` file contains the authoritative list of planted problems (duplicates, expired licenses, orphaned accounts, high-risk AI systems, maturity gaps, control mappings, and charter flaws) organized by tool and problem type. This file is for grading tool outputs only and must never be given to a tool under test.
