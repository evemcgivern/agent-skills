# Application rationalization SOP

## Purpose

Give the organization an evidence-backed TIME (Tolerate, Invest, Migrate, Eliminate) decision for every application in the portfolio, so duplicate spend and expired licenses get found and acted on rather than carried forward another year.

## Scope

Applies to every application in the software inventory in scope for portfolio management, across every business unit and category covered by the asset management policy.

## Roles

- **Portfolio manager** — runs the rationalization, pulls the inventory, scores each app, and drafts the TIME table and savings summary.
- **App owners** — confirm their app's cost, users, and data held, and respond to duplicate and eliminate findings for their apps.
- **Finance partner** — checks the stated savings range and confirms budget impact.
- **Architecture** — reviews duplicate pairs and Migrate decisions for technical dependencies before they're approved.

## Frequency

A full rationalization every year, plus a lighter pass before each budget cycle. Re-run sooner after a merger or acquisition adds a new estate to reconcile.

## Steps

1. Pull the inventory with owner, category, cost, and user count for every app; list gaps as **Unverified:** [[XW-001]] [[XW-002]]
2. Chase missing owners or costs before scoring starts [[XW-026]]
3. Identify duplicate applications by category and function, reporting each pair once [[XW-011]]
4. Check licenses against the `checked_on` date for expiry and over-buying [[XW-007]] [[XW-008]]
5. Score each app for business value and technical fit, stating the scoring used [[XW-011]]
6. Assign Tolerate, Invest, Migrate, or Eliminate with reasons; for duplicate pairs, recommend which app to keep [[XW-011]]
7. State savings as a range, not a promise, and have the finance partner check it [[XW-012]]
8. Check vendor contract terms with architecture before any eliminate decision is acted on [[XW-013]]
9. Raise a retirement plan for each eliminate decision [[XW-009]] [[XW-010]]
10. Identify the data held by each retiring or migrating app and agree its disposition — archive, migrate, or delete, with a retention period — with the data owner [[XW-010]] [[XW-028]]
11. Record the decisions and approvers before the rationalization is filed [[XW-020]]

## Evidence to retain

- The dated inventory used, with gaps flagged.
- The duplicate pairs found and the keep/retire recommendation for each.
- The license check results, including expired and over-entitled licenses.
- The TIME table with the scoring and reasoning behind each decision.
- The data disposition agreed for each retiring or migrating app, and who agreed it.
- The finance partner's confirmation of the savings range and architecture's review of duplicate and Migrate decisions.

## Related

- [Governance framework crosswalk](../crosswalk/) (`crosswalk`)
- [ITAM maturity check](../itam-maturity/) (`itam-maturity`)
- [AI system intake and risk tiering](../ai-intake/) (`ai-intake`)
- [Access review pack](../access-review/) (`access-review`)
- [Stand up a governance program](../program-setup/) (`program-setup`)
