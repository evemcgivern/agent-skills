# Key work by crosswalk theme

Each of the 28 crosswalk themes below sets out what it means in practice, the concrete work it takes to run it, what evidence that work leaves behind, and which role usually carries it.

## XW-001 Application and software inventory

- **What it means:** Every application and software asset in use is recorded in one place and kept accurate as things change.
- **Key work:** Pull installed-software data from endpoint and cloud consoles; reconcile the pulls against the current inventory; add newly discovered assets and flag ones that no longer exist; run the `itam-maturity` tool to score how complete and current the inventory is.
- **Evidence it produces:** A dated inventory export and a maturity score with the gaps it found.
- **Usually owned by:** Asset owners, with the IT asset management team maintaining the record.

## XW-002 Asset ownership assigned

- **What it means:** Every application or software asset has one named role accountable for it, not a shared or absent owner.
- **Key work:** Match each inventory line to an owning team; chase down assets with no owner; confirm ownership at each inventory refresh; record the owner directly in the inventory record.
- **Evidence it produces:** An inventory with its owner field fully populated and a log of ownership changes over time.
- **Usually owned by:** Business unit leads, with the asset management team tracking completeness.

## XW-003 Asset management policy and scope

- **What it means:** A written policy sets out what counts as a managed asset and the rules for managing it.
- **Key work:** Draft the policy's scope and rules; circulate it for sign-off; publish it somewhere staff can find it; review it on a fixed schedule and update it when the estate changes; use the `program-setup` tool to draft the policy skeleton and route it through approval.
- **Evidence it produces:** An approved, dated policy document and its review history.
- **Usually owned by:** The governance sponsor, with the policy owner drafting and maintaining it.

## XW-004 Roles and responsibilities

- **What it means:** Each governance role is clearly assigned to a role, and that assignment is kept current.
- **Key work:** List every governance role the program needs; assign each to a named role or team; publish a responsibility matrix; review and update it when the organization changes; use the `program-setup` tool to generate the matrix from the program's structure.
- **Evidence it produces:** A current responsibility matrix and its revision history.
- **Usually owned by:** The governance sponsor, with each functional lead confirming their own assignments.

## XW-005 Discovery and reconciliation of installs

- **What it means:** What's actually installed is regularly checked against what the inventory says is installed, and the two are brought back into line.
- **Key work:** Run discovery scans across endpoints and cloud accounts; compare scan results to the inventory; investigate unexplained differences; update the inventory to match reality; log every reconciliation run.
- **Evidence it produces:** Discovery scan output, a reconciliation log, and a list of corrections made.
- **Usually owned by:** The IT asset management team, with application owners confirming disputed findings.

## XW-006 Entitlement records kept

- **What it means:** The organization keeps a record of every software license and entitlement it holds.
- **Key work:** Collect purchase orders, contracts, and vendor portals into one entitlement record; log quantity, terms, and renewal date for each; update the record whenever a license is bought, transferred, or retired; reconcile the record against vendor statements.
- **Evidence it produces:** An entitlement register showing what was bought, when, and under what terms.
- **Usually owned by:** The software asset management team, with procurement supplying purchase data.

## XW-007 License compliance position

- **What it means:** The organization knows whether it holds enough licenses for what's actually deployed, or too many.
- **Key work:** Compare deployed install counts to entitlement quantities per product; check available entitlement before approving a self-service install request; flag products that are over-deployed or under-deployed; quantify the compliance or cost exposure; report the position to the asset owner; use the `rationalization` tool to weigh whether to true up, reduce, or renegotiate.
- **Evidence it produces:** A compliance position report per product, with the resulting decision recorded.
- **Usually owned by:** The software asset management team, with the budget owner approving any true-up spend.

## XW-008 License renewal and expiry tracking

- **What it means:** Renewal and expiry dates for every license are tracked so nothing lapses or auto-renews unnoticed.
- **Key work:** Log the renewal or expiry date for every entitlement; set alerts ahead of each date; review actual usage before a renewal decision; document whether to renew, reduce, or cancel; notify the budget owner in time to act.
- **Evidence it produces:** A renewal calendar and a decision record for each renewal event.
- **Usually owned by:** The software asset management team, with the budget owner making the renew-or-cancel call.

## XW-009 Lifecycle, request to retirement

- **What it means:** Every application is managed through a defined path from the initial request to its eventual retirement.
- **Key work:** Route new application requests through an intake and approval step; track each application's current lifecycle stage; schedule periodic lifecycle reviews; flag applications overdue for a stage change; hand aging or low-value applications to the `rationalization` tool for a keep-or-retire decision.
- **Evidence it produces:** A lifecycle status log showing every application's stage and its history of stage changes.
- **Usually owned by:** The application owner, with the asset management team tracking lifecycle stage across the portfolio.

## XW-010 Retirement and decommissioning

- **What it means:** When an application is retired, it is formally shut down and its data and access are removed, not just left running unused.
- **Key work:** Confirm no remaining dependents before shutdown; export or archive the data the business must keep; revoke all access and integrations; decommission the infrastructure; record the retirement date and the disposition of the data.
- **Evidence it produces:** A signed-off decommissioning checklist and a data-disposition record.
- **Usually owned by:** The application owner, with IT operations executing the technical shutdown.

## XW-011 Portfolio value optimization (rationalization)

- **What it means:** The application portfolio is periodically reviewed to decide what to keep, merge, or retire.
- **Key work:** Score each application on cost, usage, risk, and overlap with other tools; group applications that serve the same need; recommend consolidate, retain, or retire for each; get sign-off on the recommendations; use the `rationalization` tool to run the scoring and produce the recommendation set.
- **Evidence it produces:** A scored portfolio review and a signed-off list of consolidate, retain, or retire decisions.
- **Usually owned by:** The application portfolio owner, with business unit leads confirming usage.

## XW-012 Cost and budget tracking

- **What it means:** What the organization spends on software is tracked against budget and attributed to the right owner.
- **Key work:** Pull software spend from finance and vendor invoices; map each cost line to an owning application and budget; compare actual spend to budget monthly; flag overspend or unattributed cost; report variances to the budget owner.
- **Evidence it produces:** A cost-to-budget report per application, with variances explained.
- **Usually owned by:** The budget owner, with finance supplying the underlying spend data.

## XW-013 Vendor and contract management

- **What it means:** Vendor relationships and their contract terms are actively managed, including the risk a given supplier introduces.
- **Key work:** Maintain a contract record per vendor with key terms and renewal dates; assess each vendor's risk at onboarding and on a set cycle; track vendor performance against the contract; escalate breaches or risk changes to the owner; renegotiate or exit underperforming contracts.
- **Evidence it produces:** A vendor register with risk ratings and a log of contract reviews.
- **Usually owned by:** Procurement, with the application owner assessing operational risk.

## XW-014 Access control policy

- **What it means:** A written policy sets the rules for how access to systems is granted, changed, and removed.
- **Key work:** Draft the access rules covering request, approval, and removal; align them with the segregation-of-duties rules; get the policy approved; publish and train staff on it; review it on a fixed schedule.
- **Evidence it produces:** An approved access control policy and its review history.
- **Usually owned by:** The governance sponsor, with the identity and access team maintaining it.

## XW-015 Access provisioning

- **What it means:** New or changed access to a system is granted only through an approved, traceable process.
- **Key work:** Capture the access request and its business justification; route it to the owner for approval; provision only what was approved; log the request, approval, and grant together; use the `access-review` tool to confirm the grant matches policy before it's applied.
- **Evidence it produces:** A provisioning ticket per grant, linking the request, approval, and the access actually given.
- **Usually owned by:** The application owner approving, with the identity and access team provisioning.

## XW-016 Periodic access review

- **What it means:** People's access to each application is checked on a set schedule, and anything no longer needed is removed.
- **Key work:** Pull account exports; match them to HR records; send privileged roles to owners for re-approval; remove orphaned and dormant access; record every decision; use the `access-review` tool to generate the review packet and track completion.
- **Evidence it produces:** A dated review log, owner sign-offs, and removal tickets.
- **Usually owned by:** Application owners, with the identity and access team running the cycle.

## XW-017 Leaver access removal

- **What it means:** A person's access is removed promptly when they leave the organization or change roles.
- **Key work:** Trigger an access-removal request the moment a leaver or role change is confirmed; disable accounts across every connected system; confirm no access was missed; log the removal timestamp against the trigger date; escalate any removal that missed its deadline.
- **Evidence it produces:** A leaver checklist with removal timestamps measured against the trigger date.
- **Usually owned by:** HR triggering the event, with the identity and access team executing removal.

## XW-018 Privileged access

- **What it means:** Accounts with elevated or administrative rights are held to tighter controls than ordinary user accounts.
- **Key work:** Maintain a separate inventory of privileged accounts; require a stronger approval step before granting privileged rights; review privileged access more often than standard access; use time-limited or just-in-time elevation where the platform supports it; log every privileged session; run the `access-review` tool against the privileged-account list on its shorter cycle.
- **Evidence it produces:** A privileged-account inventory, elevation logs, and shortened-cycle review records.
- **Usually owned by:** The identity and access team, with system owners approving each privileged grant.

## XW-019 Segregation of duties

- **What it means:** Conflicting duties are split between roles so no single role can both request and approve the same action.
- **Key work:** Map which duties conflict for each critical process; check role assignments against that conflict map; flag anyone holding both sides of a conflicting pair; compensate with a manual check where a conflict can't be avoided; document every exception with its compensating control.
- **Evidence it produces:** A conflict map, a list of violations found, and signed-off exceptions with their compensating controls.
- **Usually owned by:** The process owner, with the identity and access team checking role assignments.

## XW-020 Evidence retention for audit

- **What it means:** Records of governance activity are kept long enough, and in a form complete enough, to hand to an auditor on request.
- **Key work:** Define what evidence each control produces and how long to keep it; store evidence somewhere it can be retrieved on demand; check retention against the policy period on a set schedule; purge evidence only after its retention period ends; test retrieval before an audit, not during one.
- **Evidence it produces:** A retention schedule and a successful test retrieval of sample evidence.
- **Usually owned by:** The governance program owner, with each control owner supplying their own evidence.

## XW-021 AI system risk and impact assessment before deployment

- **What it means:** An AI system's likely risk and impact are assessed before it goes into production, not after.
- **Key work:** Capture the AI system's intended use and data inputs at intake; score its risk against a fixed set of criteria; require a higher-level sign-off for higher-risk systems; document mitigations for risks found; block deployment until the assessment is signed off; use the `ai-intake` tool to capture the request and produce the risk score.
- **Evidence it produces:** A completed risk assessment and its sign-off, tied to the deployment record.
- **Usually owned by:** The AI system owner, with the AI governance reviewer approving the assessment.

## XW-022 AI system inventory

- **What it means:** Every AI system in use is recorded alongside the general software inventory, not tracked separately or missed.
- **Key work:** Add each AI system to the inventory at intake; record its purpose, model, and data sources; flag AI systems discovered outside the intake process; reconcile the AI inventory against the software inventory on the same schedule; use the `ai-intake` tool to feed new entries into the inventory automatically.
- **Evidence it produces:** An AI system inventory cross-referenced to the software asset inventory.
- **Usually owned by:** The AI governance reviewer, with the asset management team maintaining the combined record.

## XW-023 AI supplier and third-party oversight

- **What it means:** The vendor-oversight process is extended to cover AI suppliers and the third parties they in turn rely on.
- **Key work:** Ask AI suppliers to disclose their own subprocessors and model sources; assess AI-specific risks such as training-data provenance and model updates; add AI-specific clauses to supplier contracts; review AI suppliers on the same cycle as other high-risk vendors; escalate any undisclosed subprocessor.
- **Evidence it produces:** An AI supplier risk record with subprocessor disclosures attached.
- **Usually owned by:** Procurement, with the AI governance reviewer assessing AI-specific risk.

## XW-024 Risk register and treatment

- **What it means:** Identified risks are logged in one register and tracked until they are treated, not just noted and forgotten.
- **Key work:** Log each identified risk with its likelihood, impact, and owner; assign a treatment plan and target date; track treatment progress against that date; escalate overdue or worsening risks; close the risk only once the treatment is verified.
- **Evidence it produces:** A risk register with current status and a closure record for each treated risk.
- **Usually owned by:** The risk owner named on each entry, with the governance program tracking the register overall.

## XW-025 Performance review and improvement

- **What it means:** How well the governance process is working is reviewed on a set cycle, and what the review finds gets acted on.
- **Key work:** Define a small set of metrics for each control area; pull the metrics on a fixed schedule; compare them against target and against the last review; agree improvement actions for anything off target; track those actions to completion.
- **Evidence it produces:** A dated performance review with metrics, findings, and tracked improvement actions.
- **Usually owned by:** The governance program owner, with each control owner supplying their own metrics.

## XW-026 Data quality of asset records

- **What it means:** The information held in asset records is accurate and complete enough that people can make decisions from it without double-checking.
- **Key work:** Define what "complete" means for each required field; spot-check a sample of records against source systems; flag and correct records that fail the check; track a data-quality score over time; feed quality findings back into the `itam-maturity` tool's scoring.
- **Evidence it produces:** A data-quality score and a log of corrections made.
- **Usually owned by:** The asset management team, with application owners correcting their own records.

## XW-027 Governance body, sponsor, and decision rights

- **What it means:** A named group owns governance decisions, a sponsor is accountable for the program, and it's clear who can decide what.
- **Key work:** Form the governance body and name its members; assign an accountable sponsor; write down which decisions the body makes versus which it delegates; schedule regular meetings with recorded decisions; review membership and decision rights on a fixed cycle; use the `program-setup` tool to stand up the body's charter and meeting cadence.
- **Evidence it produces:** A governance charter, meeting minutes, and a decision-rights log.
- **Usually owned by:** The governance sponsor, with the governance body making collective decisions.

## XW-028 Data classification and handling

- **What it means:** Data is labeled by how sensitive it is, and handled according to that label.
- **Key work:** Define the classification levels and what each requires; classify data at creation or intake; apply the matching handling controls, such as encryption or access limits; audit a sample of data against its assigned classification; reclassify data when its sensitivity changes.
- **Evidence it produces:** A classification scheme, labeled data samples, and an audit record of handling checks.
- **Usually owned by:** The data owner, with the data governance team maintaining the classification scheme.
