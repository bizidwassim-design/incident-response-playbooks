# Incident record — INC-YYYY-NNN

> One record per incident. Fill it in as you go, not afterwards. Everything time-stamped in **UTC** with the
> local time zone noted once. Keep it in a location the attacker cannot read.

## 1. Identification

| Field | Value |
|---|---|
| Incident ID | INC-2026-042 |
| Title | Short, factual ("Personal data exposed via misconfigured share") |
| Playbook(s) in use | `playbooks/data-breach-personal-data.md` |
| Incident manager | Name, phone (out-of-band) |
| Executive sponsor | Name |
| Opened (UTC) | 2026-03-04T09:15Z |
| **Awareness timestamp (UTC)** — starts regulatory clocks | 2026-03-04T09:15Z — evidence: SOC ticket #4821 |
| Severity (current) | S2 — set 2026-03-04T09:40Z by [IM]; previous: — |
| Status | Open / Contained / Recovered / Closed |
| Bridge / channel | Out-of-band channel name; dial-in |
| Need-to-know list | Names and roles — update whenever someone is added |

## 2. Summary (keep current, 5 lines maximum)

What happened, what is affected, what has been done, what is next, when the next update is due.

## 3. Impact

| Dimension | Assessment | Evidence |
|---|---|---|
| Systems | | |
| Data (categories, volume, residency) | | |
| Individuals affected (estimate → confirmed) | | |
| Business operations | | |
| Third parties / customers / suppliers | | |
| Regulatory clocks running | Regime — start — deadline — status | |

## 4. Roles assigned

| Role | Person | Contact (out-of-band) | Assigned (UTC) |
|---|---|---|---|
| Incident manager | | | |
| Legal | | | |
| Communications | | | |
| HR | | | |
| IT / SOC lead | | | |
| DPO | | | |
| Business owner | | | |

See `templates/roles-raci.csv` for who does what in each phase.

## 5. Decision log

| # | Decision (UTC) | Decision taken | Owner | Rationale | Alternatives rejected |
|---|---|---|---|---|---|
| D1 | | | | | |

## 6. Timeline

Maintained in `timeline.csv` (one row per event, decision or communication). Summarise the key milestones here:

| Milestone | UTC |
|---|---|
| First signal | |
| Awareness | |
| Containment achieved | |
| Regulator notified | |
| Individuals notified | |
| Recovered | |
| Closed | |

## 7. Evidence and chain of custody

| ID | Item | Source system | Collected by | Collected (UTC) | Storage location | SHA-256 | Custody transfers (to, when, why) |
|---|---|---|---|---|---|---|---|
| E1 | | | | | | | |

Rules: originals sealed, work on copies; one custodian per item; every hand-over logged; nothing deleted before the
retention period set by Legal.

## 8. Communications

Maintained in `communication-log.csv`. Approvals required: Legal for anything external, Executive sponsor for
regulator, press and customer messages.

## 9. Closure

| Field | Value |
|---|---|
| Closed (UTC) | |
| Closed by | |
| Post-incident review date | |
| Actions tracker reference | |
| Lessons added to playbook(s) | Yes / No — which |
