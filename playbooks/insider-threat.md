# Playbook — Insider Threat

| | |
|---|---|
| **Use when** | A current or former employee, contractor or partner with legitimate access is suspected of misusing it: data theft, sabotage, fraud, unauthorised access, or policy violation with security impact. |
| **Default severity** | **S3 (Medium)** on suspicion; **S2 (High)** when privileged access, personal data or trade secrets are involved; **S1 (Critical)** for active sabotage or ongoing exfiltration by a privileged user. |
| **Incident manager** | Head of Security; HR and Legal are mandatory co-leads from the first hour. |
| **Related SOC playbooks** | [data-exfiltration](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/data-exfiltration.md) · [credential-access](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/credential-access.md) |
| **Templates** | [incident-record](../templates/incident-record.md) · [timeline](../templates/timeline.csv) · [communication-log](../templates/communication-log.csv) · [post-incident-review](../templates/post-incident-review.md) |

> Insider cases are **people cases first**. Evidence must be gathered lawfully, the person is presumed innocent until
> the facts say otherwise, and the circle of knowledge must stay tiny. Most "insider" alerts turn out to be a badly
> communicated business process — handle every case as if it will end up in front of a judge **and** as if the person
> did nothing wrong.

## 1. Scope and triggers

- DLP or SOC alert: bulk download, mass email forwarding, USB copy, personal cloud upload, source-code clone to an
  unusual location — especially within 30 days before or after a resignation or termination.
- Manager or colleague report (the most common source).
- Access anomalies: after-hours access to systems outside the person's role, privileged actions without a ticket.
- Sabotage indicators: deleted backups, disabled monitoring, logic bombs, unexplained outages after a disciplinary event.
- Fraud indicators from Finance (vendor master changes, payment detail changes) — coordinate with Finance.
- Former employee access still active and in use.

**Types** (record one in the incident record): *negligent* (policy breach without malice), *malicious* (intent),
*compromised* (the account, not the person — hand to the SOC credential-access playbook), *collusive* (with an
external party).

## 2. Severity matrix

| Factor | S4 Low | S3 Medium | S2 High | S1 Critical |
|---|---|---|---|---|
| Access level | Standard user | Elevated in one system | Administrator / developer with production access | Domain, cloud or backup administrator |
| Data at stake | Internal, non-sensitive | Confidential business data | Personal data, source code, pricing, M&A | Trade secrets, regulated data, safety systems |
| Activity | Policy breach, no exfil | Exfil suspected, person still employed | Exfil confirmed or sabotage attempted | Active sabotage or exfiltration right now |
| External party | None | Unknown | Competitor or new employer | Organised crime / state actor |

## 3. Roles

| Role | Responsibilities in this playbook |
|---|---|
| **Incident manager** | Runs the technical investigation, keeps the circle minimal, owns the timeline. |
| **HR** | Employment law, the person's record, interview process, suspension/termination mechanics, duty of care. |
| **Legal counsel** | Lawfulness of monitoring and evidence collection, privilege, injunctions, police referral, employment claims. |
| **Line manager** | Context on the role and behaviour — **only if not a suspect or a witness**. |
| **IT / SOC** | Evidence collection, access snapshot, access revocation when authorised. |
| **Comms** | Rarely external. Internal messaging if the case becomes visible. |
| **Physical security / facilities** | Badge logs, CCTV retention, escorting if required. |
| **Executive sponsor** | Approves covert monitoring (where lawful), suspension, police referral. |

Keep a **need-to-know list** in the incident record. Anyone added must be told the confidentiality expectations.

## 4. Decision points

| # | Decision | Owner | Guidance |
|---|---|---|---|
| D1 | Is monitoring of this person lawful and proportionate? | LEGAL + HR | Check the acceptable-use policy, works council / employee representation requirements, local law. Document the basis **before** looking at personal content. |
| D2 | Covert investigation or immediate access removal? | IM + HR + EXEC | Covert only while evidence is being secured and if no ongoing harm; remove access the moment harm is active. |
| D3 | Suspend, restrict or leave in place? | HR + EXEC | Suspension is neutral, not disciplinary; restrict rather than suspend when the evidence is thin. |
| D4 | Interview the person? When and who? | HR + LEGAL | Never the IM alone; HR leads, security presents facts. Offer representation where required. |
| D5 | Involve police / regulator? | LEGAL + EXEC | Theft of trade secrets, fraud above a threshold, personal data (see [data-breach-personal-data](data-breach-personal-data.md)). |
| D6 | Notify affected third parties (customers whose data was taken)? | LEGAL | Follow the personal-data playbook clocks if applicable. |
| D7 | Termination and recovery of data / devices | HR + LEGAL | Written undertaking, device return, confirmation of deletion, injunction if refused. |

## 5. Timeline template

| Phase | Target | Actions | Owner |
|---|---|---|---|
| **T0 — Report** | 0 | Open the incident record with the *need-to-know list*. Classify type and severity. Do **not** contact the person. | IM |
| **T+2 h** | 2 h | HR and Legal briefed. Lawful basis for investigation documented (D1). Preservation request to IT: freeze mailbox, endpoint, cloud audit logs, badge logs, CCTV. | IM, LEGAL, HR |
| **T+8 h** | 8 h | Access snapshot: every system, group, token, shared drive the person can reach. Initial activity timeline for the last 90 days. Decision D2. | IT |
| **T+24 h** | 24 h | Evidence reviewed by IM + Legal. Decision D3 (suspend/restrict). If restricting: revoke remote access and tokens, keep the account enabled for forensic continuity where practical. | IM, HR |
| **T+3 d** | 3 d | Interview prepared (D4): facts, questions, documents. Interview held with HR lead and note-taker. | HR, LEGAL |
| **T+5 d** | 5 d | Outcome: no case / policy breach / misconduct / criminal. Decisions D5–D7. Third-party notifications if required. | EXEC, LEGAL |
| **T+30 d** | 30 d | Access fully removed or restored. Data recovery confirmed. Post-incident review focused on **control gaps**, not the individual. | IM, HR |

## 6. Communication templates

All templates are **fictional** examples for *Northwind Logistics*. Insider cases usually need only the internal and,
rarely, customer templates. Legal approves every message.

### Internal

> **Subject:** Confidential — access review in progress
>
> [Name], as part of a confidential review we have temporarily restricted some system access for [team/person].
> This is a precaution and not a conclusion. Please do not discuss this with colleagues or the person concerned, and
> route any questions to HR at [contact]. Thank you for your discretion.

### Customers

> **Subject:** Notice regarding your information held by Northwind Logistics
>
> We are writing to inform you that an individual with authorised access to our systems is believed to have copied
> information without permission on or around [date]. The information may include [categories]. We have removed the
> individual's access, secured the affected systems, and [referred the matter to the authorities / obtained legal
> undertakings for the return and deletion of the data]. We recommend [specific advice]. Contact: [address].

### Regulator

Only where personal data or regulated data is involved — use the regulator section of
[data-breach-personal-data](data-breach-personal-data.md). Add: the insider's role and access level (not their
identity unless required), the lawful basis for the investigation, and the status of any legal action.

### Press holding statement

> Northwind Logistics is aware of an internal matter involving the handling of company information and has taken
> appropriate action, including engaging external advisers. We do not comment on individual employment matters.
> Our systems and customer services are operating normally. Media contact: [name, address].

## 7. Evidence and chain of custody

The evidence will be challenged — by the person's lawyer, a tribunal or a regulator. Collect it as if every item
will be cross-examined.

- [ ] Lawful-basis memo (policy references, who approved, date) **before** any content review.
- [ ] Preservation: litigation hold on mailbox and cloud drive; endpoint image or EDR timeline export; VPN, proxy,
      DLP, cloud audit and badge logs for the window; CCTV retention extended.
- [ ] Access snapshot at T+8 h (exported, hashed).
- [ ] The specific artefacts: files copied, emails forwarded, commands run — each with source, timestamp, hash and collector.
- [ ] Interview notes signed by the note-taker; the person's statement if given.
- [ ] Device return receipts and deletion confirmations.
- [ ] Decision log D1–D7 with the people in the room.

Custodian rules: two-person collection for anything that may go to court; working copies only, originals sealed;
custody log in the incident record with every hand-over.

## 8. Post-incident review

Review the **system**, not the person. Use [templates/post-incident-review.md](../templates/post-incident-review.md) and cover:

1. Why did the person have the access they used? Was it still needed? When was it last reviewed?
2. How long did the activity go on before detection, and which signal finally caught it?
3. Did the leaver / mover process fire? Were there gaps between HR events and access changes?
4. Was DLP tuned for the data that actually matters (customer lists, pricing, code)?
5. Was the investigation lawful, proportionate and fair? Any process the person could reasonably complain about?
6. Which controls to add: joiner-mover-leaver automation, privileged access reviews, DLP rules, exit interviews,
   pre-departure access tightening.
