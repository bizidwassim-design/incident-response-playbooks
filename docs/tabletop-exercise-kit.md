# Tabletop exercise kit

Three ready-to-run scenarios, each 90–120 minutes, for the crisis-level team: incident manager, Legal, Comms, HR,
IT/SOC lead, DPO, a business owner and an executive sponsor. All companies, people and systems are **fictional**.

## How to run a tabletop

| Step | Who | Notes |
|---|---|---|
| 1. Pick the scenario and the playbook(s) it exercises | Facilitator | Rotate: one data/privacy, one availability/operations, one people/vendor per year. |
| 2. Brief the players a week ahead | Facilitator | Send the playbook and templates; do **not** send the injects. |
| 3. Set the rules | Facilitator | No wrong answers; play your real role; decisions are made, not deferred; use the real templates on screen. |
| 4. Run the injects at the stated time, record the decisions | Facilitator + scribe | Scribe fills `templates/timeline.csv` and the decision log live. |
| 5. Hot wash (20 min) | All | What surprised you, what was missing, what would have slowed you down for real. |
| 6. Report within a week | Facilitator | Use `templates/post-incident-review.md` — the review is the same whether the incident was real or not. |

Scoring is deliberately simple: for each inject, did the team (a) identify the decision, (b) make it, (c) record it,
(d) communicate it to the right people? Four points per inject.

**Facilitator tips**: keep time strictly; when the team stalls, ask "what does the playbook say?" rather than
giving the answer; put at least one inject that makes a previous decision wrong.

---

## Scenario 1 — "The Friday share" (data breach, personal data)

**Playbooks**: [data-breach-personal-data](../playbooks/data-breach-personal-data.md), with
[insider-threat](../playbooks/insider-threat.md) opening midway.

**Setting**: Northwind Logistics, 2 400 employees across Québec, France and the UK. HR data in a SaaS platform
("Fabrikam People") with a nightly export to an internal reporting share. It is Friday, 16:40 local time.

| Time | Inject | Expected decisions / actions |
|---|---|---|
| 0:00 | SOC analyst: "DLP flagged a 1.2 GB download from the HR reporting share by the service account `svc-reporting`, from a workstation in the Montréal office, 30 minutes ago." | Open incident record. Is personal data in scope? (yes — assume) Record awareness. Severity S2. Page DPO and Legal. |
| 0:10 | IT: "The share contains the full employee export: names, home addresses, dates of birth, bank details for payroll, for all three countries. Last export: last night." | Three regimes identified (GDPR via France/UK, Loi 25, PIPEDA). Clocks table created. Severity S1? (bank details, 2 400 people, three regimes — yes.) |
| 0:20 | Service desk: "The workstation belongs to a finance analyst who resigned last week; their last day is Tuesday." | Insider-threat playbook opened. HR engaged. Need-to-know list. Lawful basis for investigation documented before anyone looks at the analyst's mailbox. Do not contact the person. |
| 0:35 | Legal: "Our DPA with the UK customer whose staff we also manage requires notification within 24 hours of becoming aware. Does that apply?" | Contract check: do we process any customer personal data in this export? (Yes — 150 contractor records from Contoso.) Contractual clock: 24 h. Communication log entry planned. |
| 0:50 | SOC: "The file was copied to a USB device, then the device was removed. Endpoint logs show a personal cloud-storage client was also installed two days ago." | Decision: restrict access now vs covert. Preserve endpoint and cloud audit logs. Suspension decision with HR and Legal. Interview planning. |
| 1:05 | Comms: "A journalist has emailed asking whether Northwind has had 'an HR data leak'." | Press holding statement (reactive only). Who approves? Internal note to staff — what can be said without prejudicing the investigation? |
| 1:20 | DPO: "It is now Saturday 09:00. The GDPR 72-hour deadline falls on Monday 09:15. Facts are incomplete." | Phased notification decision. Who drafts, who approves on a weekend? Loi 25 "as soon as possible" — is Monday defensible? PIPEDA RROSH assessment. |
| 1:35 | Executive sponsor: "Do we tell the employees? All of them? Bank details — do we offer anything?" | Decision D4/D6: notify individuals, offer monitoring, payroll safeguards with Finance. Employee letter drafted from the template. |
| 1:50 | Hot wash | What did we not know (data inventory, contracts)? Was the awareness timestamp defensible? Who was missing from the room? |

---

## Scenario 2 — "Pay or we stay down" (DDoS with extortion, then a smokescreen)

**Playbooks**: [ddos](../playbooks/ddos.md), then [privileged-account-compromise](../playbooks/privileged-account-compromise.md).

**Setting**: Northwind's customer booking portal and API, hosted in the cloud behind a CDN with a basic plan. The
all-staff VPN terminates on the same edge firewall. Tuesday, 10:15, peak booking hours.

| Time | Inject | Expected decisions / actions |
|---|---|---|
| 0:00 | Monitoring: "Portal latency 20 s, API error rate 60 %. Edge firewall at 95 % connection table. CDN reports a volumetric attack of 40 Gbit/s." | Open incident record. Characterise: volumetric + state exhaustion. Severity S2 (revenue) — S1 if the VPN drops. Engage CDN/scrubbing emergency upgrade (D1). Status page within 30 min. |
| 0:15 | Customer service: "Phones are overloaded, customers say the site is down. Can we tell them when it will be back?" | Script issued: no promise of time, status-page URL. Comms owns the cadence. |
| 0:25 | Executive: email received — "Northwind, we can keep this up for days. 5 BTC and it stops. You have 6 hours." | D5: no reply, no payment; preserve the email; Legal and law enforcement. Who else in the company got it? Instruct staff not to respond. |
| 0:40 | Network: "The VPN is down. All home workers are offline, including the SOC night shift which works remotely." | Severity S1. Decision D3: move the VPN to a separate address / provider? Business-continuity invocation (D6)? How does the SOC operate without VPN — is there an out-of-band path? |
| 0:55 | CDN provider: "Emergency scrubbing is active, traffic dropped to 2 Gbit/s. Application-layer requests to `/api/login` still at 50× normal." | Rate limiting and challenge on login (D2). Which legitimate integrations will break? Business owner decides. |
| 1:10 | SOC (via phone): "During the attack, a global administrator account signed in from a new country and registered a new MFA method. We only saw it now because the SIEM was flooded." | Smokescreen confirmed. Open privileged-account-compromise: out-of-band channel (D1), trusted circle (D2), contain now (D3). Break-glass accounts. Backup and EDR console integrity. |
| 1:25 | Comms: "A trade publication has posted that Northwind is 'under cyber attack and negotiating a ransom'." | Press holding statement updated: attack yes, ransom negotiation no. Customer email now justified? Do we mention the admin account? (No — not until scoped.) |
| 1:40 | Network: "Traffic back to baseline for 30 minutes." | Stand-down criteria (D7): 2 h clean **and** intrusion hunt clean — not yet. Keep mitigations 7 days. Post-incident review scheduled. |
| 1:55 | Hot wash | Did the SOC have an out-of-band way to work? Was the scrubbing contract known before the day? Did anyone nearly reply to the extortionist? |

---

## Scenario 3 — "The helpful assistant" (AI system incident with a vendor twist)

**Playbooks**: [ai-system-incident](../playbooks/ai-system-incident.md), then
[supply-chain-vendor-compromise](../playbooks/supply-chain-vendor-compromise.md).

**Setting**: "NorthBot", a customer-service assistant built on a vendor-hosted model, with retrieval over the
knowledge base and a tool that can issue shipping refunds up to a limit. Internal pilot of an agent that reads
supplier emails and updates purchase orders. Wednesday, 14:00.

| Time | Inject | Expected decisions / actions |
|---|---|---|
| 0:00 | Social media: a screenshot shows NorthBot quoting another customer's name, address and tracking history when asked "what did you tell the last person?". 3 000 shares in an hour. | Open incident record; variant B (data leakage). Preserve the conversation and retrieval logs. Decision D1: disable or degrade (remove retrieval). Comms acknowledges publicly within the hour. |
| 0:15 | AI owner: "The retrieval index was rebuilt last night and accidentally included the live ticketing export instead of the anonymised one." | Root cause candidate. Scope: how many conversations since the rebuild touched the ticketing data? Personal-data playbook clocks start — awareness timestamp now. |
| 0:30 | Finance: "Refund volume through NorthBot tripled in the last two days. Several refunds went to the same three accounts." | Variant D (unsafe action) suspected: prompt injection via chat to trigger refunds? Disable the refund tool; revoke its credentials (D2). Fraud team engaged. Preserve tool-call logs. |
| 0:45 | Procurement: "The purchase-order agent approved a 'change of bank details' request from supplier Contoso Freight this morning. Contoso says they sent no such email." | Injection through supplier email into the agent. Treat as BEC + AI incident. Stop payment with the bank. Who else could have been targeted? Disable the agent. |
| 1:00 | Vendor (model provider): "We are investigating reports that a plugin in our marketplace, which your tenant has enabled, is exfiltrating conversation data." | Supply-chain playbook opened. Inventory the vendor's access and the plugin's permissions. Written questions to the vendor. Does this change the data-breach scope? |
| 1:15 | Legal: "The customer in the screenshot has contacted us through a lawyer. A regulator has also seen the post and asked for a call tomorrow." | Regulator preparation from the AI-specific list. Affected-individuals list method. Remedy for the customer. |
| 1:30 | Executive: "Can we switch NorthBot back on for the weekend sale? We lose a lot without it." | Re-enable criteria (D7): root cause fixed, regression test including this case, monitoring, sign-off in the AI register. Text-only mode as a compromise? Who signs? |
| 1:45 | Hot wash | Was the AI risk assessment realistic? Did anyone own the retrieval pipeline? Were tool permissions least-privilege? Did Comms have an AI-specific template? |

---

## Inject bank (for your own scenarios)

Mix and match; each should force a decision from the playbook rather than a technical action.

- A key person is unavailable (incident manager on a plane, DPO on leave, only deputy is new).
- The insurer insists on their own forensics firm, which cannot start for 48 hours.
- The attacker reads the incident channel and posts a screenshot.
- The regulator's portal is down on the deadline day.
- A customer's own incident team wants to join your bridge.
- The backup you planned to restore from turns out to be 11 days old.
- Someone on the team tweets support for colleagues, revealing the incident.
- The CEO wants to announce "no data was taken" before scoping is done.
- Law enforcement asks you to keep the attacker's access open to observe.
- The post-incident review discovers the same root cause as an incident 14 months ago.
