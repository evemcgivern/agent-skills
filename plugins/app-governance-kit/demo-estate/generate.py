"""Generate the Halden Logistics demo estate. Deterministic; standard library only."""
import csv
import datetime
import json
import sys
from pathlib import Path

CHECKED_ON = "2026-09-01"
CHECKED_ON_DATE = datetime.date(2026, 9, 1)

CATEGORIES = [
    ("ERP", "Northbeam"), ("Payroll", "Paylane"), ("HR information system", "Staffhub"),
    ("Recruiting", "Hirewell"), ("Learning management", "Coursefield"), ("Expense management", "Receiptly"),
    ("Procurement", "Buyline"), ("Contract management", "Clausebase"), ("CRM", "Relato"),
    ("Marketing automation", "Campaignly"), ("Customer support desk", "Helpwise"), ("Live chat", "Chattera"),
    ("Survey", "Pollform"), ("E-signature", "Signwell"), ("Document management", "Docuvault"),
    ("Intranet", "Hallway"), ("Video conferencing", "Meetrix"), ("Team chat", "Threadly"),
    ("Project management", "Taskmoor"), ("Diagramming", "Shapewise"), ("Password manager", "Keyfort"),
    ("Endpoint management", "Fleetdesk"), ("Antivirus", "Shieldline"), ("Backup", "Vaultline"),
    ("Monitoring", "Pulseboard"), ("IT service management", "Servicely"), ("Identity provider", "Gatekey"),
    ("Warehouse management", "Stackyard"), ("Transport management", "Routewise"), ("Fleet telematics", "Trackmile"),
    ("Route optimization", "Pathcraft"), ("Yard management", "Dockside"), ("Customs brokerage", "Borderline"),
    ("Freight audit", "Ratecheck"), ("EDI gateway", "Tradelink"), ("Carrier portal", "Loadboard"),
    ("Demand forecasting", "Foresight"), ("Business intelligence", "Chartwell"), ("Data warehouse", "Lakeshore"),
    ("ETL", "Pipewright"), ("Spreadsheet add-in", "Cellmate"), ("Accounts payable automation", "Payflow"),
    ("Treasury", "Cashmere"), ("Tax compliance", "Levywise"), ("Audit management", "Trailmark"),
    ("GRC", "Controlroom"), ("Policy management", "Rulebook"), ("Health and safety", "Safeyard"),
    ("Visitor management", "Frontdesk"), ("Facilities booking", "Roomly"), ("Invoice OCR", "Scanwright"),
    ("Chatbot", "Askbay"), ("Email security", "Mailguard"), ("Web analytics", "Clickpath"), ("Code repository", "Commitly"),
]
# Planted duplicates: slot -> (partner slot, alternate vendor)
DUPLICATES = {41: (8, "Tallysheet"), 52: (14, "Quickink"), 37: (22, "Linkup"), 58: (29, "Routesmith"), 46: (33, "Clearport")}
CONFIDENTIAL = {"Payroll", "HR information system", "Recruiting", "CRM", "Expense management", "Treasury",
                "Tax compliance", "Identity provider", "Customer support desk", "Accounts payable automation"}
EXPIRED = {"LIC-017": "2026-03-31", "LIC-044": "2025-12-31"}
TERMINATED = {"EMP-071": "2026-05-15", "EMP-072": "2026-07-02"}
ORPHANS = {"ACC-019": "EMP-071", "ACC-063": "EMP-072", "ACC-104": "EMP-099"}
AI_SYSTEMS = [
    ("AI-001", "Email security", "Classifies inbound email as spam or phishing and quarantines it."),
    ("AI-002", "Finance", "Reads supplier invoices and extracts totals, dates, and PO numbers for review."),
    ("AI-003", "Operations", "Suggests delivery routes to dispatchers, who approve each plan."),
    ("AI-004", "HR", "Ranks job applicants' CVs and shortlists candidates for interview."),
    ("AI-005", "Customer service", "Answers customer shipment-status questions in the website chat."),
    ("AI-006", "Planning", "Forecasts weekly warehouse volume from historic shipments."),
]
MATURITY = [
    ("governance", "Governance and policy", 3), ("inventory", "Inventory and discovery", 3),
    ("entitlement", "Entitlement and license management", 1), ("lifecycle", "Lifecycle, request to retirement", 2),
    ("vendor", "Vendor and contract management", 4), ("data-quality", "Data quality and reconciliation", 1),
    ("security", "Risk and security integration", 3), ("cost", "Cost and financial management", 4),
    ("reporting", "Reporting and improvement", 3),
]
CHARTER_FLAWS = ["decision-rights", "sponsor", "membership-size"]
DEVICE_TYPES = ["laptop", "desktop", "mobile", "server"]
DEVICE_REFRESH_CYCLE_MONTHS = {"laptop": 36, "desktop": 48, "mobile": 24, "server": 60}
DEVICE_VENDORS = {"laptop": ["Dell", "Lenovo"], "desktop": ["Dell", "HP"],
                   "mobile": ["Apple", "Samsung"], "server": ["Dell", "HPE"]}
DEVICE_BASE_COST = {"laptop": 1200, "desktop": 900, "mobile": 600, "server": 6000}
# Planted problems: slots overdue for refresh (active, past their cycle) and
# retired slots with no confirmed data wipe (subset of DEVICE_RETIRED).
DEVICE_RETIRED = {5, 11, 18, 24, 29, 35, 42, 48, 53, 59}
DEVICE_OVERDUE = {8, 27, 45}
DEVICE_UNWIPED = {11, 42}
CHARTER_DRAFT = """# Halden Software Governance Council — draft charter

## Purpose
The council oversees software and applications at Halden Logistics.

## Members (voting)
CIO; CISO; heads of procurement, finance, legal, architecture, HR, operations, warehousing, transport, customer service, sales, marketing; and the service desk lead.

## Meetings
Monthly, 90 minutes. Standing agenda: new requests above threshold, exceptions, renewals due, and a review of measures. Outcomes are recorded in a register kept by the governance analyst. Urgent items are handled out of cycle by email vote within five working days.

## Scope
New software requests, renewals, retirements, and AI tools.

## Intake
Requests come through one software request form. The governance analyst triages requests weekly. Only items above a cost or risk threshold come to the council.

## Escalation
Disputes go to the Chief Operating Officer, who does not sit on the council and who breaks ties.

## Measures
Time from request to outcome, the share of software bought through the intake form, savings, and exceptions granted. Reviewed quarterly, starting from a baseline set in the first quarter.
"""
CONTROLS = [
    ("C1", "Maintain an accurate inventory of software and who owns each application.", "XW-001"),
    ("C2", "Review user access to applications on a schedule and remove access no longer needed.", "XW-016"),
    ("C3", "Assess each AI system for risk before it is deployed.", "XW-021"),
]


def _write(path: Path, header: list[str], rows: list[list]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def generate(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    key = []
    base = iter(CATEGORIES)
    slots = {}
    for i in range(1, 61):
        if i not in DUPLICATES:
            slots[i] = next(base)
    for i, (partner, vendor) in DUPLICATES.items():
        slots[i] = (slots[partner][0], vendor)
        key.append({"tool": "rationalization", "type": "duplicate_app",
                    "id": "+".join(sorted((f"APP-{partner:03d}", f"APP-{i:03d}")))})
    apps = [[f"APP-{i:03d}", f"{slots[i][1]} {slots[i][0]}", slots[i][1], slots[i][0],
             round(5000 + (i * 7919) % 90000, -2), 20 + (i * 37) % 900,
             "confidential" if slots[i][0] in CONFIDENTIAL else "internal"] for i in range(1, 61)]
    _write(out / "apps.csv", ["id", "name", "vendor", "category", "annual_cost_usd", "users", "data_sensitivity"], apps)

    licenses = []
    for i in range(1, 61):
        lid = f"LIC-{i:03d}"
        licenses.append([lid, f"APP-{i:03d}", 25 + (i * 13) % 500, EXPIRED.get(lid, "2027-06-30"), CHECKED_ON])
    key += [{"tool": "rationalization", "type": "expired_license", "id": lid} for lid in EXPIRED]
    _write(out / "licenses.csv", ["id", "app_id", "entitlements", "expiry", "checked_on"], licenses)

    employees = [[f"EMP-{i:03d}", "terminated" if f"EMP-{i:03d}" in TERMINATED else "active",
                  TERMINATED.get(f"EMP-{i:03d}", "")] for i in range(1, 81)]
    _write(out / "employees.csv", ["id", "status", "termination_date"], employees)

    accounts = []
    for i in range(1, 121):
        aid = f"ACC-{i:03d}"
        emp = ORPHANS.get(aid, f"EMP-{(i - 1) % 70 + 1:03d}")
        accounts.append([aid, emp, f"APP-{(i - 1) % 60 + 1:03d}", "admin" if i % 17 == 0 else "user",
                         f"2026-08-{(i % 28) + 1:02d}"])
    key += [{"tool": "access-review", "type": "orphaned_account", "id": aid} for aid in ORPHANS]
    _write(out / "accounts.csv", ["id", "employee_id", "app_id", "role", "last_login"], accounts)

    _write(out / "ai-systems.csv", ["id", "owner", "description"], [list(a) for a in AI_SYSTEMS])
    key.append({"tool": "ai-intake", "type": "high_risk_ai", "id": "AI-004"})

    _write(out / "maturity-answers.csv", ["area", "label", "score"], [list(m) for m in MATURITY])
    lowest = sorted(MATURITY, key=lambda m: m[2])[:3]
    key += [{"tool": "itam-maturity", "type": "maturity_gap", "id": m[0]} for m in lowest]

    (out / "controls.md").write_text(
        "# Controls to map\n\n" + "".join(f"- **{c}**: {text}\n" for c, text, _ in CONTROLS), encoding="utf-8")
    key += [{"tool": "crosswalk", "type": "crosswalk_match", "id": f"{c}:{xw}"} for c, _, xw in CONTROLS]

    (out / "council-draft.md").write_text(CHARTER_DRAFT, encoding="utf-8")
    key += [{"tool": "program-setup", "type": "charter_gap", "id": f} for f in CHARTER_FLAWS]

    devices = []
    for i in range(1, 61):
        dtype = DEVICE_TYPES[(i - 1) % 4]
        cycle = DEVICE_REFRESH_CYCLE_MONTHS[dtype]
        vendor = DEVICE_VENDORS[dtype][(i // 4) % len(DEVICE_VENDORS[dtype])]
        owner = f"EMP-{((i * 13) % 80) + 1:03d}"
        cost = DEVICE_BASE_COST[dtype] + (i * 173) % DEVICE_BASE_COST[dtype]
        retired = i in DEVICE_RETIRED
        status = "retired" if retired else "active"
        if i in DEVICE_OVERDUE:
            months_since_deploy = cycle + 6
        elif retired:
            months_since_deploy = 24 + (i * 7) % 40
        else:
            months_since_deploy = 3 + (i * 11) % (cycle - 6)
        deploy_date = CHECKED_ON_DATE - datetime.timedelta(days=months_since_deploy * 30)
        if retired:
            refresh_due_date = ""
            retire_months_ago = months_since_deploy - 18
            retirement_date = (CHECKED_ON_DATE - datetime.timedelta(days=retire_months_ago * 30)).isoformat()
            data_wipe_confirmed = "no" if i in DEVICE_UNWIPED else "yes"
        else:
            refresh_due_date = (deploy_date + datetime.timedelta(days=cycle * 30)).isoformat()
            retirement_date = ""
            data_wipe_confirmed = ""
        devices.append([f"DEV-{i:03d}", dtype, vendor, owner, deploy_date.isoformat(), refresh_due_date,
                         status, retirement_date, data_wipe_confirmed, cost, CHECKED_ON])
    _write(out / "devices.csv", ["device_id", "type", "vendor", "owner", "deploy_date", "refresh_due_date",
                                  "status", "retirement_date", "data_wipe_confirmed", "cost_usd", "checked_on"],
           devices)
    key += [{"tool": "hardware-lifecycle", "type": "overdue_refresh", "id": f"DEV-{i:03d}"}
            for i in sorted(DEVICE_OVERDUE)]
    key += [{"tool": "hardware-lifecycle", "type": "unwiped_retired_device", "id": f"DEV-{i:03d}"}
            for i in sorted(DEVICE_UNWIPED)]

    key.sort(key=lambda k: (k["tool"], k["type"], k["id"]))
    (out / "answer-key.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    generate(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent)
