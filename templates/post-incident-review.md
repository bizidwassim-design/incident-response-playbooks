# Post-incident review — INC-YYYY-NNN

> Held within 30 days of closure, chaired by someone who was **not** the incident manager. Blameless: the review
> looks for the conditions that allowed the incident and slowed the response, not for the person who clicked.
> Two hours maximum; circulate the timeline 48 hours before.

## 1. Facts

| Field | Value |
|---|---|
| Incident ID / title | |
| Playbook(s) used | |
| Final severity | |
| Review date, chair, attendees | |
| Dates: first signal → awareness → contained → recovered → closed (UTC) | |
| Individuals / customers affected (final) | |
| Regulators notified (regime, date, deadline met Y/N) | |
| Cost estimate (hours, external services, lost revenue, remedies) | |

## 2. Timeline walk-through

Walk the `timeline.csv` from first signal to closure. For each phase ask:

| Phase | What went well | What slowed us down | Evidence |
|---|---|---|---|
| Detection → awareness | | | |
| Triage and severity | | | |
| Containment | | | |
| Investigation and scoping | | | |
| Notifications and communications | | | |
| Eradication and recovery | | | |

Key durations (fill in and compare with the playbook targets):

| Metric | Actual | Target | Gap |
|---|---|---|---|
| First signal → awareness | | | |
| Awareness → severity set | | | |
| Awareness → containment | | | |
| Awareness → regulator notification | | | |
| Awareness → individuals notified | | | |
| Awareness → recovered | | | |

## 3. Root cause and contributing factors

Separate the **technical cause** (what the attacker or error exploited) from the **organisational causes** (why it
was possible and why it was not caught sooner). Use "why?" five times, honestly.

| Type | Finding | Evidence |
|---|---|---|
| Technical root cause | | |
| Contributing factor 1 | | |
| Contributing factor 2 | | |
| Detection gap | | |
| Response gap | | |

## 4. Decisions review

For each decision in the decision log: was it the right call with the information available at the time? Would a
different default in the playbook have helped?

| Decision | Right call? | Comment | Playbook change? |
|---|---|---|---|
| D1 | | | |

## 5. What the playbook got wrong

Be specific. Missing roles, unrealistic target times, templates that did not fit, steps nobody understood.

## 6. Actions

Every action has one owner, one date and a way to verify it is done. Track them outside this document (ticketing /
risk register) and reference here.

| # | Action | Type (prevent / detect / respond / recover) | Owner | Due | Verification | Tracker ref |
|---|---|---|---|---|---|---|
| A1 | | | | | | |

## 7. Communication of the review

| Audience | What they receive | By |
|---|---|---|
| Executive / board | One-page summary: impact, cause, actions, residual risk | |
| Incident team | This document | |
| All staff | Lessons applicable to everyone (phishing, reporting, device handling) | |
| Regulator / customers | Where committed in notifications | |

## 8. Sign-off

| Role | Name | Date |
|---|---|---|
| Review chair | | |
| Incident manager | | |
| Executive sponsor | | |
