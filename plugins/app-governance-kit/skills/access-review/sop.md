# Access review SOP

## Purpose

Give the organization evidence that access to each in-scope application is still needed, that leavers and orphaned accounts are removed, and that privileged and conflicting roles have been re-approved by the people accountable for them.

## Scope

Applies to every application in scope for access governance, including all systems holding confidential or restricted data and every system with privileged or administrative roles.

## Roles

- **Review coordinator** — sets the review scope, pulls the account export and HR list, runs the matching and exceptions analysis, and files the evidence pack.
- **Application owners** — re-approve privileged roles for their application, decide each exception, and confirm removals are carried out.
- **HR** — supplies the current employee status and leave-date list the review is matched against.
- **IAM team** — provisions and removes access on the owners' decisions and confirms each removal in the system of record.
- **Internal audit** — samples completed reviews and their evidence packs to confirm the process was followed.

## Frequency

Quarterly for privileged accounts and other in-scope systems holding confidential or restricted data. Yearly for all other applications.

## Steps

1. Set the review scope: applications, period, and export date [[XW-016]]
2. Obtain the account export and the HR list from the systems of record [[XW-016]]
3. Order applications by data sensitivity, most sensitive first [[XW-028]]
4. Match every account to a person [[XW-015]]
5. Flag orphaned and leaver accounts for removal [[XW-017]]
6. Send privileged roles to owners for re-approval [[XW-018]]
7. Flag accounts with no login in 90 days before the export date as dormant [[XW-016]]
8. Check role conflicts against segregation-of-duties rules [[XW-019]]
9. Collect owners' decisions and confirm actions are completed [[XW-016]]
10. File the evidence pack and auditor memo [[XW-020]]

## Evidence to retain

- The dated account export and HR list used, with any missing columns flagged.
- The exceptions list: account, issue, recommended action, and the owner's decision.
- The privileged-role re-approvals, by owner and date.
- The evidence summary and auditor memo, including the clauses satisfied.
- Confirmation from the IAM team that each agreed removal was carried out.

## Related

- [**Governance framework crosswalk**](../crosswalk/) (`crosswalk`) — supplies the framework rows this review's exceptions and evidence map to.
- [**ITAM maturity check**](../itam-maturity/) (`itam-maturity`) — its security area score draws on how consistently this review runs.
- [**Application rationalization**](../rationalization/) (`rationalization`) — takes over an application once this review flags it as a retirement or migration candidate for its data disposition.
- [**AI system intake and risk tiering**](../ai-intake/) (`ai-intake`) — this review covers who can use or administer an AI system once intake has approved it.
- [**Stand up a governance program**](../program-setup/) (`program-setup`) — stands up the sponsor and owner roles this review reports its exceptions to.
