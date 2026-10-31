# Playbook — Data Breach Involving Personal Data

| | |
|---|---|
| **Use when** | Personal data (customers, employees, candidates, partners' staff) has been, or may have been, accessed, disclosed, altered, lost or made unavailable without authorisation. |
| **Default severity** | **S2 (High)** on suspicion; **S1 (Critical)** once confirmed for special-category data, > 1 000 individuals, or any regulator clock running. |
| **Incident manager** | Head of Security or delegate; Data Protection Officer (DPO) co-leads. |
| **Related SOC playbooks** | [data-exfiltration](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/data-exfiltration.md) · [cloud-account-compromise](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/cloud-account-compromise.md) · [phishing-business-email-compromise](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/phishing-business-email-compromise.md) |
| **Templates** | [incident-record](../templates/incident-record.md) · [timeline](../templates/timeline.csv) · [communication-log](../templates/communication-log.csv) · [post-incident-review](../templates/post-incident-review.md) |

> The technical response (containing the attacker, closing the hole) is the SOC's job and is covered by the linked
> SOC playbooks. **This playbook is about the clocks, the decisions and the people**: who must be told, by when, and
> who decides. Start the timeline the moment anyone says "personal data".

## 1. Scope and triggers

Typical ways this incident starts:

- SOC confirms exfiltration from a system that holds personal data (HR, CRM, ticketing, e-commerce, payroll).
- A mailbox compromise where the mailbox contains customer or employee data.
- A misdirected email, a shared link set to "anyone", a database left open, a lost laptop without full-disk encryption
  (see [lost-or-stolen-device](lost-or-stolen-device.md)).
- A supplier reports a breach of data they process for you (see [supply-chain-vendor-compromise](supply-chain-vendor-compromise.md)).
- Ransomware with double extortion (encryption **and** theft).
- A data subject, journalist or researcher contacts you claiming to hold your data.

**Not in scope**: data that is public by design, fully anonymised data, or internal business data without personal
information (use the relevant technical playbook instead).

### Awareness and the clocks

"Awareness" starts regulatory timers. Use this working definition and record the timestamp in the incident record:

> *Awareness* = the moment someone with authority in the organisation has reasonable certainty that a security
> incident has compromised personal data. Not "suspicion", not "investigation complete".

| Regime (name only — check the current text with counsel) | Who to notify | Trigger | Clock to remember | Individuals |
|---|---|---|---|---|
| **EU / UK GDPR** | Supervisory authority of the lead establishment | Breach likely to result in a risk to individuals | **72 hours** from awareness (phased notification allowed) | Without undue delay if *high* risk |
| **Québec Loi 25** | Commission d'accès à l'information (CAI) | Incident presenting a *risk of serious injury* | **As soon as possible** — no fixed hours, document every delay | As soon as possible; keep an incident register |
| **Canada PIPEDA** | Office of the Privacy Commissioner (OPC) | *Real risk of significant harm* (RROSH) | **As soon as feasible** | As soon as feasible; records kept for 24 months |
| **Contractual** | Customers / controllers | Whatever the DPA says — often 24–48 h | Read the contract on day one | Usually the controller decides |
| **Sector / other** | Financial, health, telecom regulators; cyber-insurance | Policy-specific | Often 24 h for insurers | — |

Create one timeline row per clock the moment it starts ("GDPR 72 h clock started — awareness at 2026-03-04 09:15 UTC").

## 2. Severity matrix

| Factor | S4 Low | S3 Medium | S2 High | S1 Critical |
|---|---|---|---|---|
| Individuals affected | < 50 | 50–999 | 1 000–49 999 | ≥ 50 000 |
| Data categories | Business contact details only | Identity data (name, address, DOB) | Financial, credentials, government IDs | Special categories (health, biometrics, children), or ID documents |
| Exposure | Internal only, contained | Single external party, recoverable | Multiple external parties or unknown | Published / for sale / attacker confirmed |
| Regulatory | None | One regime, low risk | One regime, notification likely | Multiple regimes or cross-border |
| Reputational | None | Local | National press likely | Customer exits / contractual penalties |

Take the **highest** factor. S1 and S2 open a crisis bridge and bring in Legal, Comms and the executive sponsor within
the hour. The generic matrix lives in [templates/severity-matrix.md](../templates/severity-matrix.md).

## 3. Roles

| Role | Named in the incident record as | Responsibilities in this playbook |
|---|---|---|
| **Incident manager** | IM | Owns the timeline, chairs the bridge, calls the severity, holds decisions. |
| **DPO / Privacy lead** | DPO | Assesses risk to individuals, drafts regulator notifications, keeps the breach register. |
| **Legal counsel** | LEGAL | Privilege, contract obligations, regulator strategy, law-enforcement liaison. |
| **Communications** | COMMS | Internal notes, customer letters, press holding statement, social monitoring. |
| **HR** | HR | Employee data, employee communications, disciplinary process if insider involvement. |
| **IT / SOC lead** | IT | Technical facts: what, when, how many, is it still happening. |
| **Business owner of the data** | OWNER | Confirms the data set, impact to operations, customer relationships. |
| **Executive sponsor** | EXEC | Approves external communications, budget, go/no-go on notifications where discretionary. |

RACI for every step: [templates/roles-raci.csv](../templates/roles-raci.csv).

## 4. Decision points

Each decision gets a timeline row with the decision, the owner, the rationale and the alternatives rejected.

| # | Decision | Owner | Inputs | Default if undecided at deadline |
|---|---|---|---|---|
| D1 | Is personal data in scope? (sets the clocks) | DPO + IT | Data inventory, system owner statement | **Yes** — assume in scope |
| D2 | What is the risk to individuals: none / risk / high risk? | DPO + LEGAL | Data categories, exposure, likelihood of misuse, mitigations (encryption, revoked tokens) | **Risk** — notify regulator |
| D3 | Notify which regulators, in which order? | LEGAL | Lead establishment, residency of individuals, contracts | Lead authority first, within 72 h |
| D4 | Notify individuals? Now or after containment? | EXEC on DPO advice | High-risk assessment, risk of tipping off attacker, ability to give useful advice | Notify when the advice is actionable, never later than the regulator requires |
| D5 | Engage external forensics / breach coach? | IM + LEGAL | Scale, insurer requirements, privilege | Yes for S1/S2 |
| D6 | Offer credit monitoring / identity protection? | EXEC | Financial or ID data involved | Yes if financial or government IDs exposed |
| D7 | Law-enforcement report? | LEGAL | Criminal act, extortion, insurer requirement | Yes for S1 |

## 5. Timeline template

Copy into [templates/timeline.csv](../templates/timeline.csv). Target times are from **awareness** (T0).

| Phase | Target | Actions | Owner |
|---|---|---|---|
| **T0 — Awareness** | 0 | Open incident record. Record awareness timestamp with evidence. Classify severity. Start the clocks table. | IM, DPO |
| **T+1 h** | 1 h | Bridge opened. Legal and Comms briefed. Privilege established (counsel directs the investigation if practical). Contract obligations checked for the affected data set. | IM, LEGAL |
| **T+4 h** | 4 h | First scoping: systems, data categories, rough count, countries of residence. Containment status from SOC. First internal holding note sent. | IT, DPO, COMMS |
| **T+24 h** | 24 h | Insurer notified. Contractual customer notifications sent where the DPA requires 24 h. Regulator notification drafted. Decision D2 made (risk to individuals). | LEGAL, DPO |
| **T+48 h** | 48 h | Regulator notification approved by EXEC and LEGAL. Customer letter and FAQ drafted. Call-centre script ready. | DPO, COMMS |
| **T+72 h** | 72 h | **GDPR deadline.** Notification submitted (phased if facts are incomplete). Loi 25 / PIPEDA notifications submitted where triggered. | DPO |
| **T+7 d** | 7 d | Individuals notified (if D4 = yes). Website notice live. Breach register updated. Evidence pack frozen. | COMMS, DPO |
| **T+30 d** | 30 d | Follow-up regulator submission with final facts. Post-incident review held. Control improvements logged with owners and dates. | IM, DPO |

## 6. Communication templates

All templates below are **fictional** and written for the example company *Northwind Logistics*. Replace every
bracketed field, have Legal approve, and log each send in the [communication log](../templates/communication-log.csv).

### Internal

> **Subject:** Security incident — personal data — need-to-know
>
> Team, we are handling a security incident that may involve personal data held in [system]. The incident manager is
> [name] and the bridge is [channel]. Please do not discuss the incident outside this group, do not contact affected
> people or customers yourselves, and forward any external enquiry (press, customers, regulators) to [comms mailbox].
> Keep all related emails, chats and files — do not delete anything. Next update at [time].

### Customers

> **Subject:** Important information about your data at Northwind Logistics
>
> On [date] we identified a security incident affecting [description of system]. Our investigation shows that the
> following information relating to you may have been accessed: [categories]. It does **not** include [categories not
> affected, e.g. payment card numbers or passwords].
>
> What we have done: [containment in one sentence], [notified the relevant authorities], [engaged independent experts].
> What you can do: [specific, actionable advice — e.g. be alert to emails claiming to be from us, change a password if
> reused elsewhere, use the free monitoring service at (link)].
>
> We are sorry this happened. Questions: [dedicated address / phone], open [hours]. — [Executive name], [title]

### Regulator

Use the authority's own form where one exists. Have the following ready, with a note on which facts are still provisional:

1. Organisation identity, DPO contact details, lead establishment.
2. Nature of the breach: what happened, when, how it was discovered, awareness timestamp.
3. Categories and approximate number of individuals and records.
4. Likely consequences for individuals.
5. Measures taken or proposed (containment, mitigation, notification to individuals).
6. Cross-border elements; other regulators notified.
7. Whether this is a phased notification and when the next update will follow.

### Press holding statement

> Northwind Logistics is investigating a cyber security incident identified on [date]. We took immediate steps to
> secure our systems and are working with external specialists and the relevant authorities. Protecting the data of our
> customers and employees is our priority, and we will contact anyone affected directly. We will not be commenting
> further while the investigation is ongoing. Media contact: [name, address].

## 7. Evidence and chain of custody

Preserve before you fix. For personal-data breaches the evidence has to withstand a regulator or a court asking
"how do you know only 3 000 people were affected?".

- [ ] Awareness evidence: the alert, email or ticket that triggered awareness, with original timestamps.
- [ ] Access logs for the affected data store covering the full exposure window, exported read-only and hashed (SHA-256).
- [ ] The data set as it stood at the time (a copy or a record count query with its output), to support the numbers you report.
- [ ] Data map / inventory entry showing categories, residency and retention for the affected data.
- [ ] Containment actions with timestamps (token revocations, link disabling, password resets).
- [ ] Every notification sent, with recipients, time and sender — attach to the communication log.
- [ ] Contract extracts (DPA clauses) relied upon for notification decisions.
- [ ] Decision log for D1–D7 with rationale.

Chain of custody: one custodian per item, recorded in the incident record (who collected, when, where stored, hash).
Store in a restricted, retention-locked location. Nothing leaves the location without a log entry.

## 8. Post-incident review

Hold within 30 days, chaired by someone who was not the incident manager. Use
[templates/post-incident-review.md](../templates/post-incident-review.md) and answer specifically:

1. How long between the first signal and awareness? Could any control have shortened it?
2. Were the clocks met? If a deadline was missed or a notification phased, why?
3. Was the data inventory accurate? Did we know where the data lived, who owned it and which countries were involved?
4. Did the communication templates work? What did customers or the regulator ask that we had not anticipated?
5. Which technical control failures let it happen (link to the SOC review) — and which privacy controls (minimisation,
   retention, encryption, access reviews) would have reduced the impact?
6. Update the breach register, the data inventory, the DPA template and this playbook.
