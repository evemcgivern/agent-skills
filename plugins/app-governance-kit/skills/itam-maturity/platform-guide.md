# Platform guide: ITAM maturity check

For each of the nine process areas, the ServiceNow and Flexera One capability that supports it. Where no source names a capability for a platform in a given area, that is stated as a gap rather than guessed.

## Governance and policy

**ServiceNow.** Asset management policy lives in the same **Policy and Compliance Management** capability, inside ServiceNow's Integrated Risk Management (IRM) product, that the [crosswalk tool's platform guide](../crosswalk/platform-guide.md) describes: policies at the top, **Control Objectives** as the measurable targets, and **Controls** as the activities and evidence underneath them. There is no capability specific to SAM Pro, HAM Pro, or Enterprise Architecture (formerly Application Portfolio Management, APM) for holding the organization's own asset management policy document; it belongs in this shared IRM workspace.

**Flexera One.** No Flexera One feature exists for authoring or holding an organization's own asset management policy document; its capabilities (below) act on the estate the policy describes rather than storing the policy itself.

## Inventory and discovery

**ServiceNow.** SAM Pro gathers installation data automatically from integrations such as Discovery and normalizes what it finds through the **Content Library and Content Service**, then runs **Reconciliation** to compare discovered installs against records. HAM Pro's **Hardware Asset Manager Workspace** and **Asset Inventory Audit** capability do the equivalent for hardware, including barcode/QR scanning through the Agent Mobile app. **Enterprise Architecture (formerly Application Portfolio Management, APM)** builds its own application inventory from the **CMDB**, tracking the dependencies between applications and the technology they run on. Confirmed table names: **Business Application** (`cmdb_ci_business_app`), **Business Capability** (`cmdb_ci_business_capability`), and **Information Object** (`cmdb_ci_information_object`); Enterprise Architecture uses the Platform and Platform App fields on the Business Application table to link it to discovered application services (`cmdb_ci_service_discovered`), with `cmdb_ci_sdlc_component` and `cmdb_ci_appl` also referenced in that service-mapping context.

**Flexera One.** Flexera One's **asset discovery and inventory** capability builds a unified inventory across on-prem, cloud, SaaS, and containers, and normalizes what it finds against **Technopedia**, which Flexera states recognizes and normalizes titles at over 98%.

## Entitlement and license management

**ServiceNow.** SAM Pro's core license workflow is **Reconciliation | Remediation | Compliance**: matching entitlements to deployed installs, and surfacing over- or under-licensed positions. Its **Reclamation Rules and Removal Candidates** identify licenses to recover from unused installs.

**Flexera One.** Flexera One applies **Use Rights Analysis** against publisher-specific entitlement terms and uses **AI contract & entitlement ingestion** to read purchase orders, invoices, and contracts. It calculates an **Effective License Position (ELP)** to state the compliance position for top-tier vendors automatically.

## Lifecycle, request to retirement

**ServiceNow.** HAM Pro automates the hardware lifecycle with Flow Designer flows covering the **Hardware Asset Order flow** (procurement through deployment), **Asset Onboarding and Offboarding flows**, and six asset task types — Deploy, Swap, Retire, Refresh, Loaner, and Leased Return — ending in **Hardware Disposal flows** with certificate tracking. **Enterprise Architecture (formerly Application Portfolio Management, APM)** runs **Application Portfolio Rationalization** through classify, measure, analyze, and plan phases to decide whether an application is migrated, sustained, or divested (Enterprise Architecture's own four-way decision, stored as **Planned Disposition** on the Business Application: invest, sustain, migrate, or retire). On the technology side, Enterprise Architecture separately names **Technology Lifecycle Management (TLM)**, which tracks technology life-cycle risks and exceptions, and the **Technology Reference Model**, which manages the software-product and hardware catalog and standards — both shown on Gantt-chart timelines, and together the named coverage for hardware/software standards lifecycle beyond HAM Pro's physical-asset lifecycle.

**Flexera One.** Flexera One's **Hardware Lifecycle Management** tracks hardware from request to disposal, with **Lifecycle Automation** integrating vendors, procurement, and disposal systems, and **Lifecycle Alerts** for events such as end of life, warranty expiry, or lease termination. Flexera One also names a **Software Lifecycle Management (SLM)** capability, covering software from acquisition to retirement and centered on identifying end-of-life (EOL) and end-of-support (EOS) applications using Technopedia data — the software-side counterpart to Hardware Lifecycle Management.

## Vendor and contract management

**ServiceNow.** **Vendor Risk Management (VRM)**, part of the GRC portfolio, covers vendor relationships through named functional areas: **Vendor Portfolio**, **Vendor Tiering**, **Assessment Management**, **Vendor Portal**, and **Issues and Remediation**.

**Flexera One.** Flexera One's **AI contract & entitlement ingestion** extracts vendor contract data automatically from invoices and purchase orders. No standalone, branded vendor-risk-management capability exists; Flexera's vendor-management page frames that outcome as emerging from IT Asset Management and SaaS Management rather than a distinct feature. Flexera does name a separate **SBOM Management** capability (software bill-of-materials tracking of third-party code and producers) as its nearest named vendor/supply-chain risk feature, distinct from vendor relationship or tiering management.

## Data quality and reconciliation

**ServiceNow.** Both SAM Pro and HAM Pro normalize records through the shared **Content Library and Content Service**, and SAM Pro's reconciliation step is where mismatches between discovered and recorded data surface for correction.

**Flexera One.** Flexera One's **Technopedia** enrichment is the named data-quality capability: Flexera states it standardizes software titles and versions and adds details such as end-of-life and end-of-support dates, with over 98% recognition and normalization rates.

## Risk and security integration

**ServiceNow.** ServiceNow's public documentation does not name a dedicated integration product linking SAM Pro, HAM Pro, or Enterprise Architecture to Vulnerability Response, IRM, or Security Incident Response for general application security. All of these capabilities read the same CMDB, and ServiceNow's own Enterprise Architecture documentation describes Technology Risk Management as an EA-internal capability that surfaces lifecycle-driven security and regulatory risk from EA's own portfolio data, rather than a link to a separate security product. The one confirmed named cross-capability link is **AI Control Tower**, which attaches AI risk and ownership data to a Business Application via table `sn_apm_ws_ba_product_model_map`, but it is scoped to AI assets specifically and requires its own license — so it does not close the gap for enforcing access control policy on new applications generally.

**Flexera One.** No Flexera One capability exists for enforcing or checking an access control policy against new applications; its confirmed capabilities are scoped to inventory, licensing, and cost rather than access security.

## Cost and financial management

**ServiceNow.** **Cloud Cost Management** is a named ServiceNow capability offered alongside SAM, with a **Cloud Cost Simulator** available to SAM Enterprise customers for modeling the cost of moving workloads to the cloud.

**Flexera One.** Flexera One's **renewal & true-up optimization** right-sizes renewals from usage and entitlement data, and its **automated license reclamation** identifies unused software to cut spend.

## Reporting and improvement

**ServiceNow.** HAM Pro's **Hardware Asset Manager Workspace** includes configurable KPI tiles for assets due for refresh, unassigned assets, and expiring contracts. Enterprise Architecture's (formerly APM's) **Assessment Dashboard** visualizes application indicators — cost, quality, technical risk, investment, user satisfaction, and business value — for portfolio decisions.

**Flexera One.** Flexera One's **always-on audit readiness** is the named capability for maintaining a defensible, reportable license position on an ongoing basis rather than only at audit time.

## Sources checked

- [Policy Lifecycle Management in IRM: Closing the gap on a single, governed policy workflow](https://www.servicenow.com/community/grc-articles/policy-lifecycle-management-in-irm-closing-the-gap-on-a-single/ta-p/3566226) — Policies, Control Objectives, Controls terminology (also used by the crosswalk platform guide).
- [Software Asset Management Professional (SAM Pro) — ServiceNow Community](https://www.servicenow.com/community/developer-blog/software-asset-management-professional-sam-pro/ba-p/3025704) — Content Library and Content Service, Reconciliation | Remediation | Compliance, Reclamation Rules and Removal Candidates.
- [Core Asset Management vs HAM Pro — ServiceNow Community](https://www.servicenow.com/community/ham-blog/core-asset-management-vs-ham-pro-what-you-actually-get-and-when/ba-p/3518013) — Hardware Asset Manager Workspace, Asset Onboarding and Offboarding flows, Hardware Asset Order flow, asset task types, Hardware Disposal flows, Asset Inventory Audit.
- [Application Portfolio Management on ServiceNow — ServiceNow Community](https://www.servicenow.com/community/enterprise-architecture-articles/application-portfolio-management-on-servicenow/ta-p/2297172) — CMDB-based application inventory, Application Portfolio Rationalization phases, Assessment Dashboard and indicators.
- [ServiceNow Vendor Risk Management notes and videos — ServiceNow Community](https://www.servicenow.com/community/grc-blog/servicenow-vendor-risk-management-notes-and-videos/ba-p/2274288) — Vendor Portfolio, Vendor Tiering, Assessment Management, Vendor Portal, Issues and Remediation.
- [Cloud Cost Management Path to Value — ServiceNow Community](https://www.servicenow.com/community/cloud-cost-management-articles/cloud-cost-management-path-to-value/ta-p/3060830) — Cloud Cost Management, Cloud Cost Simulator availability for SAM Enterprise.
- [Reporting & Dashboards: SAM — ServiceNow Community](https://www.servicenow.com/community/sam-forum/reporting-amp-dashboards-sam/td-p/3241900) — checked for a named SAM dashboard; confirms only reconciliation grouping/consumption rules, no named dashboard, so none is claimed above.
- [IT Asset Management (ITAM) Software — Flexera](https://www.flexera.com/products/flexera-one/it-asset-management) — asset discovery and inventory, Use Rights Analysis, AI contract & entitlement ingestion, renewal & true-up optimization, automated license reclamation, Technopedia.
- [Software Asset Management (SAM) Tools — Flexera](https://www.flexera.com/solutions/software-usage-costs/software-asset-management) — Effective License Position (ELP), always-on audit readiness, Technopedia recognition/normalization rate.
- [IT Hardware Asset Management Solutions — Flexera](https://www.flexera.com/solutions/it-asset-lifecycle/hardware-asset-management) — Hardware Lifecycle Management, Lifecycle Automation, Lifecycle Alerts.
- [Enterprise Architecture (formerly Application Portfolio Management) — Start your EA Journey Toolkit — ServiceNow Community](https://www.servicenow.com/community/enterprise-architecture-articles/enterprise-architecture-formerly-application-portfolio/ta-p/2382292) — the Xanadu rename.
- [Enterprise Architecture (formerly Application Portfolio Management) and CSDM tables — ServiceNow Docs, Xanadu](https://www.servicenow.com/docs/r/xanadu/application-portfolio-management/enterprise-architecture/apm-use-case.html) — `cmdb_ci_business_app`, `cmdb_ci_business_capability`, `cmdb_ci_information_object`, `cmdb_ci_service_discovered`, `cmdb_ci_sdlc_component`, `cmdb_ci_appl`.
- [Technology Risk and Portfolio Governance with ServiceNow — ServiceNow Community](https://www.servicenow.com/community/enterprise-architecture-articles/technology-risk-and-portfolio-governance-with-servicenow/ta-p/3532840) — Technology Risk Management as an EA-internal capability.
- [Unpacking Common Questions on Application Vulnerability Response — ServiceNow Community](https://www.servicenow.com/community/secops-articles/unpacking-common-questions-on-application-vulnerability-response/ta-p/3251929) — confirms AVR and Enterprise Architecture share the CMDB but names no direct integration.
- [ServiceNow Vulnerability Response and Application Rationalization — Cadena guide](https://cadena.co/resources/guides/servicenow-vulnerability-response) — a conceptual (not a named technical) workflow linking SAM data to remediation decisions.
- [Software Lifecycle Management — Flexera](https://www.flexera.com/solutions/it-asset-lifecycle/software-lifecycle-management) — the named SLM capability, EOL/EOS identification via Technopedia.
- [Vendor Management — Flexera](https://www.flexera.com/solutions/software-renewals-audits/vendor-management) — confirms no standalone vendor-risk-management capability; outcome is framed as emerging from IT Asset Management and SaaS Management.
- [Flexera Launches SBOM Management Functionality in Flexera One IT Visibility — Flexera press release](https://www.flexera.com/about-us/press-center/flexera-launches-sbom-management-functionality-in-flexera-one-it-visibility) — the named SBOM Management capability.

Pages that do not return readable content to an automated fetch: ServiceNow's own product pages (`servicenow.com/products/...`, `servicenow.com/uk/products/...`, both 403) and Flexera's documentation site (`docs.flexera.com/...`, also 403). Everything above comes from a page that loaded.
