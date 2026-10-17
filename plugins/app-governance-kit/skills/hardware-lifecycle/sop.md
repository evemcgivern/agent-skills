# Hardware lifecycle SOP

## Purpose

Give the organization evidence-backed visibility into which devices are overdue for replacement and which retired devices still hold an unconfirmed data wipe, so refresh spend is planned ahead of failure and no device leaves the estate without its data accounted for.

## Scope

Applies to every device in the hardware inventory in scope for asset management — laptops, desktops, mobile devices, and servers — across every business unit and location covered by the asset management policy.

## Roles

- **Hardware asset manager** — runs the lifecycle check, pulls the device inventory, and drafts the refresh and disposal-blocking summaries.
- **Device owners** — confirm their device's status and respond to refresh and wipe-confirmation requests.
- **IT operations** — executes replacements, upgrades, wipes, and certified destruction, and attaches the resulting evidence.
- **Budget owner** — checks the stated replacement cost range and confirms budget impact.
- **Procurement** — confirms vendor and warranty or contract terms before a replacement order is placed.

## Frequency

A full lifecycle check every quarter, plus an ad hoc check before any hardware budget request or before a disposal batch is closed out.

## Steps

1. Pull the inventory with device id, type, owner, and status for every device; list gaps as **Unverified:** [[XW-001]]
2. Chase missing owners, statuses, or dates before the check starts [[XW-001]]
3. Check every active device's refresh-due date against `checked_on` [[XW-001]] [[XW-010]]
4. Check every retired device's data-wipe confirmation [[XW-010]]
5. Group overdue-refresh devices by type and estimate the total replacement cost as a range [[XW-012]]
6. Check vendor and warranty or contract terms with procurement before any replacement, upgrade, or extension decision [[XW-013]]
7. Recommend replacement, upgrade, or extension for each overdue device, and route it to the asset owner for a decision [[XW-012]] [[XW-013]]
8. Recommend a wipe or certified-destruction method for each unwiped retired device, matched to its type [[XW-010]]
9. Hold disposal open for any retired device without wipe evidence attached [[XW-010]]
10. Have the budget owner check the cost estimate and vendor terms before a refresh order is placed [[XW-012]] [[XW-013]]
11. Record the decisions and approvers before the check is filed [[XW-001]] [[XW-010]]

## Evidence to retain

- The dated device inventory used, with gaps flagged.
- The overdue-refresh list, grouped by type, with the estimated replacement cost range.
- The unwiped-retired-device list and the wipe or certified-destruction method recommended for each.
- The wipe or destruction evidence attached once each disposal is actually closed out.
- The budget owner's confirmation of the cost estimate and procurement's confirmation of vendor terms.
- The decisions and approvers recorded for each replacement, upgrade, extension, and disposal.

## Related

- [Governance framework crosswalk](../crosswalk/) (`crosswalk`)
- [ITAM maturity check](../itam-maturity/) (`itam-maturity`)
- [Application rationalization](../rationalization/) (`rationalization`)
- [Access review pack](../access-review/) (`access-review`)
- [Stand up a governance program](../program-setup/) (`program-setup`)
