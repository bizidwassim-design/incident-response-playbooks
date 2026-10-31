# Incident management process

This document describes how the playbooks in this repository fit together into one process, who runs it, and how
it connects to the analyst-level work in
[soc-detection-playbooks](https://github.com/bizidwassim-design/soc-detection-playbooks). It follows the lifecycle
phases named in **NIST SP 800-61** (Preparation; Detection and Analysis; Containment, Eradication and Recovery;
Post-Incident Activity) — referenced by name only; read the publication itself for the detail.

## 1. Two levels, one timeline

| Level | Who | Question they answer | Where it lives |
|---|---|---|---|
| **Analyst / SOC** | SOC analysts, incident responders | *What is the attacker doing and how do we stop it?* | [soc-detection-playbooks](https://github.com/bizidwassim-design/soc-detection-playbooks) — triage, containment, investigation, eradication, evidence |
| **Incident manager / crisis** | Incident manager, Legal, Comms, HR, DPO, business owners, executive sponsor | *What does the organisation do, decide and say, and by when?* | This repository — severity, roles, decisions, clocks, communications, chain of custody, review |

Both levels write to the **same timeline** (`templates/timeline.csv`). The SOC lead sits on the crisis bridge; the
incident manager does not run queries.

## 2. The lifecycle as used here

### Preparation

- Playbooks adopted, adapted to your tools and legal regimes, and reviewed yearly.
- Roles named with deputies; out-of-band contact details tested quarterly.
- Templates (`templates/`) stored where the attacker cannot read them, with offline copies.
- Tabletop exercises run at least twice a year ([tabletop-exercise-kit.md](tabletop-exercise-kit.md)).
- Contracts (insurer, external IR, scrubbing provider, breach coach) signed before the incident.
- Data inventory current enough to answer "which personal data lives where" in an hour.

### Detection and analysis

1. **Signal** arrives (SOC alert, report, vendor notice, regulator letter).
2. **Triage** by the SOC or service desk using the SOC playbooks. If the triage answers "yes" to any of the questions
   below, open an incident record and page the incident manager:
   - Personal, regulated or customer data may be affected?
   - A privileged account, backup, EDR or identity platform is involved?
   - Customers, press or a regulator may notice?
   - More than one team is needed to respond?
   - An AI system, a vendor, a physical site or a device loss is involved?
3. **Incident manager** opens the record (`templates/incident-record.md`), records the **awareness timestamp**,
   selects the playbook(s), sets the severity (`templates/severity-matrix.md`) and names the roles
   (`templates/roles-raci.csv`).
4. **Bridge** opened for S1/S2, out-of-band if a privileged account may be compromised.

### Containment, eradication and recovery

- Technical actions follow the SOC playbooks; the incident manager owns the **decision points** listed in each
  crisis playbook and logs every decision with rationale.
- Legal, DPO and Comms work in parallel from the first hour: clocks, obligations, messages.
- Evidence is preserved before remediation and tracked with chain of custody.
- "Contained", "recovered" and "closed" are declared explicitly by the incident manager against the criteria in the
  playbook, never implied.

### Post-incident activity

- Review within 30 days (`templates/post-incident-review.md`), chaired by someone outside the response.
- Actions tracked to closure in the risk register or ticketing system.
- Playbooks, templates and the severity matrix updated; the change noted in `CHANGELOG.md` if you fork this repository.

## 3. Choosing the playbook

| Situation | Start with | Also open |
|---|---|---|
| Personal data exposed by any means | [data-breach-personal-data](../playbooks/data-breach-personal-data.md) | the technical playbook for the cause |
| Employee or contractor misuse | [insider-threat](../playbooks/insider-threat.md) | data-breach if personal data taken |
| Supplier, MSP, SaaS or software dependency compromised | [supply-chain-vendor-compromise](../playbooks/supply-chain-vendor-compromise.md) | privileged-account-compromise if they had admin access |
| Service unavailable due to attack traffic | [ddos](../playbooks/ddos.md) | — (run the SOC smokescreen checks) |
| Laptop, phone, token or paper lost or stolen | [lost-or-stolen-device](../playbooks/lost-or-stolen-device.md) | data-breach if unprotected personal data |
| Website, API or CMS exploited | [web-application-compromise](../playbooks/web-application-compromise.md) | data-breach; privileged-account-compromise if hosting account taken |
| Chatbot / agent / model misbehaviour | [ai-system-incident](../playbooks/ai-system-incident.md) | data-breach; supply-chain if a vendor model |
| Admin / cloud / identity account under attacker control | [privileged-account-compromise](../playbooks/privileged-account-compromise.md) | malware-outbreak or data-breach as impact shows |
| Malware on many hosts or spreading | [malware-outbreak](../playbooks/malware-outbreak.md) | privileged-account-compromise if admins touched |
| Unauthorised physical entry, rogue device, on-site theft | [physical-security-breach](../playbooks/physical-security-breach.md) | lost-or-stolen-device; data-breach |

Several playbooks open at once is normal. One incident record, one timeline, one incident manager.

## 4. Severity and escalation summary

| Severity | Incident manager | Bridge | Legal / Comms | Executive sponsor | Update cadence |
|---|---|---|---|---|---|
| S1 Critical | Head of Security | Immediately, 24/7 | Within 1 h | Within 1 h, on the bridge | Hourly |
| S2 High | Head of Security or deputy | Within 1 h | Within 2 h | Informed within 2 h | Every 2–4 h |
| S3 Medium | Security manager | If needed | On request | Weekly summary | Daily |
| S4 Low | Service desk / SOC | No | No | Quarterly trend | On closure |

## 5. Records to keep

| Record | Template | Retention (suggested — confirm with Legal) |
|---|---|---|
| Incident record | `templates/incident-record.md` | 5 years, or longer if litigation |
| Timeline | `templates/timeline.csv` | With the incident record |
| Communication log and every message sent | `templates/communication-log.csv` | With the incident record |
| Evidence and chain-of-custody register | section 7 of the incident record | Until Legal releases |
| Breach register (personal data, all incidents including non-notified) | your privacy programme | Per applicable law (e.g. PIPEDA 24 months minimum) |
| Post-incident review and actions | `templates/post-incident-review.md` | 3 years |

## 6. Validation

`scripts/check_playbooks.py` verifies that every playbook has the common structure (metadata table, eight numbered
sections, the four communication templates, links that resolve) and that the CSV templates have the expected
columns. CI runs it on every push and pull request.
