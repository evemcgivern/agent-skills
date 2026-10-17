# Platform guide: Crosswalk

## ServiceNow

Mapped controls live in the **Policy and Compliance Management** capability inside ServiceNow's Integrated Risk Management (IRM) product. Its data model has three layers:

- **Policies** — the organizational commitments (what Halden's own policy documents say).
- **Control Objectives** — the measurable targets that sit between a policy and a control; this is where a crosswalk row's theme and summary belong, one control objective per row.
- **Controls** — the activities, tests, and evidence that prove a control objective is met.

Control objectives can be built top-down from **Authority Documents** (the external framework — ISO 27001, COBIT, or an internal equivalent) via **Citations** (the specific clause within that document), or bottom-up directly from a policy. Record the crosswalk row's id (`XW-NNN`) as a reference number on the control objective — for example in its short description or a custom reference field — so anyone opening the record in ServiceNow can trace it back to this kit's [`crosswalk.csv`](crosswalk.csv) and to the underlying COBIT/ISO clause captured there. Work in either the classic list views or the newer **Compliance Workspace**, which is the task-focused UI for compliance managers and analysts; both read and write the same underlying records.

This guide names the module, object, and workspace as ServiceNow documents them. It does not name internal table or field names, since those vary by release and are not needed to record a reference id.

## Flexera

Flexera One has no feature for mapping an arbitrary governance control to a custom framework like COBIT 2019, ISO/IEC 27001, ISO/IEC 42001, or ISO/IEC 19770-1. Its compliance capability, Compliance Standards Intelligence, runs automated technical checks against inventory for a fixed set of named regulatory standards (for example DORA, NYDFS, APRA, and FFIEC) — it is not a place to record this crosswalk's rows or clause references.

## Sources checked

- [Policy Lifecycle Management in IRM: Closing the gap on a single, governed policy workflow](https://www.servicenow.com/community/grc-articles/policy-lifecycle-management-in-irm-closing-the-gap-on-a-single/ta-p/3566226) — Policy and Compliance Management terminology: Policies, Control Objectives, Controls, Authority Documents, Citations, Compliance Workspace.
- [ServiceNow IRM Guide: Modules, TPRM, ESG & GRC](https://www.datalunix.com/post/servicenow-irm-guide-modules-tprm-esg-grc) — confirms Policy and Compliance Management as a named IRM module and how it links policies to control libraries and authoritative sources.
- [Introducing Flexera One Compliance Standards Intelligence](https://www.flexera.com/blog/it-visibility/introducing-flexera-one-compliance-standards-intelligence-compliance-without-the-complexity/) — confirms Flexera One's compliance feature is scoped to named regulatory frameworks (DORA, NYDFS, APRA, FFIEC) via automated checks, not custom framework mapping.
