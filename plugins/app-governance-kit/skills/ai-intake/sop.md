# AI system intake SOP

## Purpose

Give every AI system a documented risk tier and a recorded set of controls before it goes into use, so risk is identified and owned at intake rather than discovered after the fact. Legal content last reviewed: 2026-09.

## Scope

Applies to any AI system a team proposes to introduce, build, buy, or extend to a new use — including a new use of a system already on the inventory.

## Roles

- **Requesting team** — describes the use case, the data it uses, and whether a person reviews each output.
- **AI governance lead** — runs the intake, assigns the tier, and maintains the AI inventory.
- **Legal** — reviews any prohibited-practice concern and any high-risk tiering before approval.
- **Security** — reviews the supplier and data-handling controls for the system.
- **Data protection** — confirms personal-data use and provenance, and any data-subject impact.

## Frequency

Every new system at proposal; every material change of use; a full re-review every year.

## Steps

1. Restate the use case: purpose, affected people, decisions made or supported, and whether a person reviews each output [[XW-021]]
2. Record the data used, whether it includes personal data, and its provenance [[XW-028]]
3. Check prohibited practices first; if one might apply, stop and escalate to legal before anything else [[XW-021]]
4. Check the high-risk areas (employment, essential services, education, law enforcement, critical infrastructure) and tier accordingly [[XW-021]]
5. Otherwise tier as limited-risk or minimal-risk [[XW-021]]
6. List the required controls for the tier, mapped through the crosswalk and the NIST AI RMF functions [[XW-024]]
7. Identify the supplier and model provider and assess them [[XW-023]]
8. Add the system to the AI inventory using [`template.md`](template.md) [[XW-022]]
9. Enter any identified risk in the risk register with an owner [[XW-024]]
10. Record the approval decision and the approver, with legal review for any high-risk or prohibited result [[XW-020]]
11. Set a re-review date, and re-run intake on any change of use [[XW-021]]

## Evidence to retain

- The restated use case, including data used, personal data, and provenance.
- The risk tier assigned and the reasoning behind it.
- The list of required controls for that tier.
- The supplier and model-provider assessment.
- The AI inventory record.
- The approval decision, the approver, and any legal review carried out.
- The re-review date set.

## Related

- [Governance framework crosswalk](../crosswalk/) (`crosswalk`) — supplies the framework rows this intake's controls and tier map to.
- [ITAM maturity check](../itam-maturity/) (`itam-maturity`) — its inventory and lifecycle questions extend to AI systems entering the estate through this intake.
- [Application rationalization](../rationalization/) (`rationalization`) — takes over an AI system once it's on the inventory, to decide whether it's still worth keeping.
- [Access review pack](../access-review/) (`access-review`) — reviews who can use or administer an AI system once this intake has approved it.
- [Stand up a governance program](../program-setup/) (`program-setup`) — stands up the sponsor and AI governance lead role this intake reports its decisions to.
