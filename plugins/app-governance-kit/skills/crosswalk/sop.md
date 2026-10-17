# Crosswalk SOP

## Purpose

Give every control, requirement, or policy statement a traceable mapping to ISO/IEC 19770-1, COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001, so a control's origin and its gaps are visible without re-reading the standards.

## Scope

Applies to any new or changed control, policy statement, or audit finding that needs a framework citation, across application, AI, and access governance.

## Roles

- **Control owner** — drafts or changes the control and requests the mapping.
- **Governance lead** — maintains [`crosswalk.csv`](crosswalk.csv), resolves ambiguous matches, and approves new rows.
- **Reviewer** — a second person who checks the mapping and signs off with a date.

## Frequency

On every new or changed control. A full review of all mapped controls runs yearly, or sooner if a cited standard is revised.

## Steps

1. Restate the control owner's control in one plain sentence, splitting any bundled obligations into separate lines [[XW-003]]
2. Search [`crosswalk.csv`](crosswalk.csv) by theme and summary and record the single best-matching row, adding a second row only if it covers a framework the first misses [[XW-003]]
3. Record the clause number from that row for each of the four frameworks, or write "no direct equivalent" where none exists [[XW-003]]
4. List each gap by framework and note what that framework's auditor would ask for in its place [[XW-025]]
5. Where no existing row fits, propose a new theme and one-sentence summary and route it to the governance lead as a decision, rather than inventing a mapping [[XW-025]]
6. Have the reviewer check the completed mapping against the control and sign off with today's date before it is filed [[XW-020]]

## Evidence to retain

- The dated mapping table produced by the Output section (framework, clause, plain-language meaning, gaps).
- The reviewer's sign-off, including their name and the sign-off date.

## Related

- [ITAM maturity check](../itam-maturity/)
- [Application rationalization](../rationalization/)
- [AI system intake and risk tiering](../ai-intake/)
- [Access review pack](../access-review/)
- [Stand up a governance program](../program-setup/)
