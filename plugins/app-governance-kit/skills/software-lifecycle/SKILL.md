---
name: software-lifecycle
description: Find installed software past or near end of life, with a CISA KEV needs-review flag, by running the offline software-lifecycle tool on a software inventory export on the person's own machine. Reports summary counts only, never names or item IDs. Use for a quarterly software lifecycle review or before an upgrade budget request.
---

# Software lifecycle check

You help a person check a software inventory for software past or near end of life. You do not do the check yourself. The standalone tool [software-lifecycle](https://github.com/evemcgivern/software-lifecycle) does it, offline, on the person's machine. You run `preflight`, then `check` in counts-only mode, and relay only the summary count lines. Never relay a line that lists item IDs, and never a name.

Real inventories are confidential. Never upload or paste the inventory anywhere, never open the inventory file, and never put its rows in a prompt, issue or commit. The same goes for the person's `--golden`, `--exceptions`, `--tracking`, and `--support-records` files and any earlier `--previous` report: they hold names and owners. Pass their paths to the tool; never open them.

## Read-only, and the one exception

The kit's skills are read-only: they never change a file, an account, or a record. This skill keeps that rule for everything that already exists. It makes two new things, and only in places the person names: a copy of the tool, and the tool's report folder. Tell the person this plainly before step 2, and ask before each one.

## Steps

1. Confirm the inventory export. Ask for the header row only, not any data rows. The file is a CSV with a header row and needs two columns: a name (accepted headings include name, software name, product, display name, application, title) and a version (version, software version, product version, display version, release, build). Optional columns: publisher, owner, an export end-of-life date, and **Parent** (also parent software, suite, or bundle), which names the suite or app a row belongs to. Headings are matched without regard to case, punctuation, or spacing; the full list is in the tool's README. Export dates must be ISO dates (`2026-01-15`). If a name or version heading does not match, the tool stops (exit code 3); `preflight` (step 5) names the columns it found and the ones it did not. Offer `--columns FILE` (see `templates/columns.example.json` in the tool) or `--profile flexera`, `servicenow-mbs`, or `rapid7`. Say that every profile is **Unverified:** no one has run them on a real export yet.
2. Get the tool at the pinned release, v0.7.0, commit `1ebc996e52b728507a4113aee6c67ea0e208a9e7`. Ask the person where to put it. Then:

   ```bash
   git clone https://github.com/evemcgivern/software-lifecycle.git FOLDER
   cd FOLDER
   git checkout --detach 1ebc996e52b728507a4113aee6c67ea0e208a9e7
   git rev-parse HEAD
   ```

   `git rev-parse HEAD` must print exactly `1ebc996e52b728507a4113aee6c67ea0e208a9e7`. If it does not, stop and say so. The commit is the pin, not the tag: a tag can be moved. If git is not available, the person can download the archive of that exact commit (`https://github.com/evemcgivern/software-lifecycle/archive/1ebc996e52b728507a4113aee6c67ea0e208a9e7.zip`); its top folder name carries the commit, and `VERSION` inside reads `0.7.0`. Say that an archive gives a weaker check than `git rev-parse HEAD`.
3. Check the prerequisites: `python3 --version` must be 3.9 or newer. The tool uses only the Python standard library, so there is nothing to install, and no network is needed to run it. `refresh_data.py` is the only file in the tool that uses the network; it builds data releases and is not needed for a check. Do not run it.
4. Check the bundled data, from the tool folder: `python3 software_lifecycle.py verify-data`. It should print "Data check passed". It checks the data files against their SHA-256 manifest. That catches a damaged data folder; it does not prove who made the files.
5. Run `preflight` on the export, from the tool folder: `python3 software_lifecycle.py preflight "INVENTORY.csv"`. It prints column titles and counts, never a cell, so you may relay it. It says which columns it found (including owner and the export end-of-life date), how many dates are not in `YYYY-MM-DD` form, and a "What to fix" list. If it lists a problem, tell the person what to fix in the export; do not open the file to fix it. A missing name or version column, or a file with no data rows, stops with exit code 3.
6. Ask the person to name the output folder. It must be new or empty: the tool writes into an existing folder and replaces any `report.*` files there, so refuse a folder that already holds files. It must also be outside the inventory's folder, outside the tool folder, and outside your working folder. Then run, from the tool folder, with every path in quotes:

   ```bash
   python3 software_lifecycle.py check "INVENTORY.csv" --counts-only --out "OUTPUT-FOLDER"
   ```

   `--counts-only` needs `--out`. Add `--as-of YYYY-MM-DD` to check as of a set date (the default is today) and `--lookahead-months N` to change the "ends soon" window (default 12). The person's own `--golden`, `--exceptions`, `--tracking`, and `--support-records` files and an earlier `--previous REPORT.json` (version 1 or 2 reports) are optional; see the tool's `docs/usage.md`. A support-records file lists support records the person holds, such as an extended-support contract, so they show beside the vendor's dates; it never changes a state or a list. Exit code 2 is a usage error, 3 is bad input, and 4 is a failed data check. In counts-only mode an error message leaves out file content; ask the person to rerun it themselves without `--counts-only` to see the detail.
7. The tool prints counts and item IDs. It still writes the full report (`report.md`, `report.json`, `report.csv`) into the output folder, and nothing technical stops you from reading it. Do not open the output folder or any file in it.
8. Relay only the summary lines, the ones that start with `checked_on`, `kev_current`, `items`, `states`, `classification`, `ambiguous_review`, `support_records` and `count_total`. Leave out every line that lists item IDs. The person looks up names and IDs themselves in `report.md` or `report.csv`. Ask which sections, if any, they want to share with you before you see any report content, and work only from what they paste.
9. Read the data dates from `manifest.json` in the folder passed to `--data`, if one was passed (the demo's test data has its own dates); otherwise from `data/manifest.json` in the tool folder. The manifest holds no inventory data. Read `release_id`, `kev_date`, `kev_catalog_version`, and `eol_date`. A KEV snapshot older than 3 days gets a warning, and older than 7 days the KEV overlay is reported as not current (`kev_current false`). An end-of-life snapshot older than 30 days gets a warning. If the data is stale, say so. **Decision needed:** whether to fetch a newer data release, verify it, and point `--data` at it, or accept the bundled snapshot.
10. Report, then hand the decisions back.

## What to report

- **Checked on** and **data currency**: the `checked_on` date (from `--as-of`, or today), `kev_current`, and the manifest dates from step 9.
- **Counts by state**: past end of life (`past_eol`), ends within the window (`ends_soon`), mainstream support ended (`mainstream_ended`), supported, and unmatched. Give items and rows; `rows` counts inventory rows, not installs.
- **Names to review**: the `ambiguous_review` count. These are rows the tool held back on purpose: the name looks like a product but there is not enough evidence, or the product's builds are shared by several support lines, so the tool keeps the product but gives no cycle, date or state (review code `shared_support_lines`, for example Internet Explorer 11). The reason per row is in the report, not in the count lines. They are counted as unmatched and are never reported as anything stronger.
- **Classification counts**: governable, component, bundle member, and unknown. `unknown` is a valid answer.
- **Bundle members**: report `classification.bundle_member` under that name. It is not the count of parts with a parent in the inventory. That count (`unmatched_breakdown.parts_with_parent`) and the count of parts whose parent needs attention (`inherited_attention`) are only in the full report; report them only if the person shares that section. A part's parent date is in `report.md` and `report.csv` under "Parent's date (inherited, not this item's own)", and in `report.json` as `inherited_lifecycle`. If the person shares any of it, label every such date as inherited from the parent. A part never counts as past end of life or ending soon through its parent.
- **Support records**: the `support_records` line gives `listed`, `ending_soon` and `not_matched`. Word them only as "a support record is listed in your file" or "not matched to a dated item in this inventory". They are the person's own records, shown beside the vendor's dates; the tool does not check that a record is current or paid. Say they are not a licence position and not audit preparation, and that a record never changes an item's state. Never relay record references, products or dates.
- **Golden-source warning**: if the person passed `--golden` and the tool printed a warning that a golden-source row was not applied (no cycle, see Names to review), relay the warning's count wording and tell the person to read Names to review in the report. Do not open the golden file.
- **Count total**: the `count_total` line, only when it is printed. It is the sum of the counts in the person's own count column, not a count of installs or machines.
- **The lists**: past end of life, ends soon, review urgently, dates disagree, unmatched, accepted risk, ownerless, golden overrides. Their counts and IDs are on lines that list item IDs, so do not relay those lines. Tell the person to read each list in `report.md` themselves. Report a list's count only where a summary line carries it.
- **Review urgently** (the person reads this list in the report): these items are past or near end of life and their vendor and product appear in CISA KEV. Use this line, exactly: "The vendor and product appear in CISA KEV. This does not mean your version is affected." KEV matches vendor and product, never version.
- **Unmatched**: no date is claimed for these. Unmatched does not mean safe. Software with no lifecycle policy, such as git, curl, and vim, is outside the data and stays unmatched.
- The open decisions, each as **Decision needed:**. For each past-end-of-life or ends-soon item, the asset owner chooses replace, upgrade, retire, or request risk acceptance. For each review-urgently item, a person checks the version against the KEV entries and sets the priority. The ITAM lead settles each dates-disagree item. The tool names roles; it never assigns people, and neither do you.

## Output

The data-currency line, the summary counts, the open decisions, then the findings block. The block is `[]`: item IDs are not relayed, so no finding carries an id. Never use a name, version, publisher, or owner as an id.

## Output rules

- Show the reasoning behind each conclusion.
- Mark every point where a person must decide with **Decision needed:** and stop short of deciding. A match is not a finding of risk; the person decides.
- Flag any figure you could not verify from the tool's output with **Unverified:**.
- For any claim about the tool's security, use only this line: "Runs locally with no network by default; not independently assessed." Do not call the tool, a release, or the data signed.
- Item IDs are a truncated hash of publisher, name, and version. Someone holding a guess can confirm it, so treat the IDs with the same care as the inventory. Never put one in your answer.
- Give no match rate or coverage percentage. On wrong matches, say: none found on the benchmark; unknown in general.
- Never call a KEV-matched item affected or exposed; use the KEV line above.
- Do not cite CISA BOD 22-01 as current: it is revoked and superseded by BOD 26-04. Do not state BOD 26-04 deadlines. The tool implements neither.
- Cite framework clauses by number from [`crosswalk.csv`](crosswalk.csv), for example XW-001 (inventory), XW-005 (discovery and reconciliation), XW-009 (lifecycle), and XW-024 (risk register). Paraphrase; never quote standards text.
- The kit gives methods and reasoning support. It is not a governance platform, a certification, or legal advice. Say so when a result could be mistaken for any of those.
- End your answer with a fenced block labeled `findings` containing a JSON list of `{"type": ..., "id": ...}` objects, as the task describes. Use `[]` when there are none.

## Demo

With no inventory of their own, the person can run the tool's synthetic demo from the tool folder at the pinned commit. It runs against synthetic data, so the output never changes with the date:

```bash
python3 software_lifecycle.py check examples/software-inventory.csv --data tests/fixtures/data --as-of 2026-10-24 --golden examples/golden-sources.csv --exceptions examples/exceptions.csv --tracking examples/tracking.csv --support-records examples/support-records.csv --counts-only --out "OUTPUT-FOLDER"
```

Every product, publisher, and owner in `examples/` is fictional. Run `preflight` on `examples/software-inventory.csv` before the check.

## Reference files

- `crosswalk.csv` in this skill's folder.
- The tool's optional counts-only server and unsigned Claude Desktop package: [docs/mcp-setup.md](https://github.com/evemcgivern/software-lifecycle/blob/main/docs/mcp-setup.md). The tool's docs say each was tested once on one Mac; anything beyond that is Unverified. This skill runs the command line, not the server.
- In the tool folder at the pinned commit: `README.md`, `docs/usage.md`, `docs/report-schema.md`, `docs/assistant-setup.md` (the steps for an assistant), `docs/sop.md` (the quarterly review and its roles), `docs/checklist.md`, `templates/`, and `examples/`.
