# Playbook — Web Application Compromise

| | |
|---|---|
| **Use when** | A public-facing web application, API or its hosting platform has been exploited: web shell, defacement, injected code (skimmer), database access through the application, abused admin interface, or a compromised CMS. |
| **Default severity** | **S2 (High)**; **S1 (Critical)** when the application processes payments, holds personal data at scale, or the attacker has reached the hosting account or the database. |
| **Incident manager** | Head of Security; Application owner and Platform lead co-lead. |
| **Related SOC playbooks** | [data-exfiltration](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/data-exfiltration.md) · [lateral-movement](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/lateral-movement.md) · [cloud-account-compromise](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/cloud-account-compromise.md) |
| **Templates** | [incident-record](../templates/incident-record.md) · [timeline](../templates/timeline.csv) · [communication-log](../templates/communication-log.csv) · [post-incident-review](../templates/post-incident-review.md) |

> The instinct is to "take the site down and fix it". Sometimes right, often wrong: you lose evidence, you tell the
> attacker you noticed, and you may not know yet what else they touched. Decide deliberately, and keep the business
> owner in the room — this is their revenue and their customers.

## 1. Scope and triggers

- WAF, EDR or file-integrity alert: new executable file in the web root, unexpected outbound connection from the web tier.
- Defacement or injected content reported by a customer, a scanner or search-engine safe-browsing warning.
- Payment card skimmer suspected (acquirer / card scheme notification, customer fraud pattern).
- Vulnerability disclosure or bug-bounty report with evidence of exploitation.
- Database anomalies: bulk reads from the application account, new admin users in the CMS.
- Cloud alert: web-tier role used for actions outside its normal pattern.

**Variants**: *content / defacement* (reputation), *web shell / RCE* (foothold on the server), *application-level
data access* (SQL injection, broken access control — data breach without server compromise), *client-side injection*
(skimmer — your customers' browsers are the victim), *platform / hosting account* (cloud or CMS admin compromised).

## 2. Severity matrix

| Factor | S4 Low | S3 Medium | S2 High | S1 Critical |
|---|---|---|---|---|
| Application | Brochure site | Partner portal, internal API | Customer accounts, orders | Payments, health, regulated data, authentication for other systems |
| Attacker position | Attempt blocked | Code execution attempted, unconfirmed | Web shell confirmed or data accessed | Database dumped, hosting account or credentials taken, skimmer live |
| Data exposure | None | Internal configuration | Personal data | Card data, credentials at scale |
| Visibility | None | Internal only | Customers notice / search-engine flag | Press / card schemes / regulator involved |
| Persistence | None | Single artefact removed | Multiple artefacts, scheduled tasks | Rebuild required; CI/CD or source possibly tainted |

## 3. Roles

| Role | Responsibilities in this playbook |
|---|---|
| **Incident manager** | Timeline, severity, decision owner, bridge. |
| **Application owner** | Business impact, go/no-go on taking the application offline, customer-facing functions. |
| **Platform / DevOps lead** | Hosting, images, rebuild, secrets rotation, infrastructure logs. |
| **Development lead** | Root cause in code, hotfix, dependency review, source-integrity check. |
| **SOC / Forensics** | Evidence capture, scoping, hunting for lateral movement from the web tier. |
| **DPO / Legal** | Personal-data and card-data obligations, PCI reporting to the acquirer, law enforcement. |
| **Comms** | Customer notices, status page, press; search-engine and browser-warning clean-up requests. |
| **Executive sponsor** | Offline decision for revenue-critical applications, external statements. |

## 4. Decision points

| # | Decision | Owner | Guidance |
|---|---|---|---|
| D1 | Take the application offline, put it in maintenance mode, or keep it running under observation? | APP OWNER + IM (+ EXEC if revenue-critical) | Offline immediately if a skimmer is live, payments are affected, or data is actively leaving. Maintenance page with the back end isolated is the usual middle ground. Observation only with forensics capturing and the attacker contained at the edge. |
| D2 | Capture evidence before remediation? | SOC | Yes: snapshot / image the instances and database **before** rebuilding. Minutes, not hours. |
| D3 | Rotate secrets? Which? | PLATFORM | Everything reachable from the web tier: database credentials, API keys, cloud roles' keys, session-signing keys (invalidates all sessions — decide with the business), CMS admin passwords, deploy keys. |
| D4 | Patch in place or rebuild from a known-good image and source? | PLATFORM + DEV | Rebuild for any confirmed code execution. Verify the source repository and CI pipeline were not touched. |
| D5 | Force password reset / logout for users? | APP OWNER + DPO | Yes if credentials or sessions could have been captured; communicate the reason honestly. |
| D6 | Card-data involvement — notify acquirer / card schemes? | LEGAL | Yes, immediately, if cardholder data may have been exposed; a PCI forensic investigation may be mandated. |
| D7 | Personal-data notification? | DPO | Follow [data-breach-personal-data](data-breach-personal-data.md). |

## 5. Timeline template

| Phase | Target | Actions | Owner |
|---|---|---|---|
| **T0 — Detection** | 0 | Open the incident record. Identify the variant. Edge containment (block attacker IPs / paths at WAF) without touching the server. Decision D2 — start evidence capture. | IM, SOC |
| **T+30 min** | 30 min | Decision D1. Snapshots taken. Bridge opened with application owner, platform and dev leads. | IM, PLATFORM |
| **T+2 h** | 2 h | Scope: when did the first malicious request arrive (web logs), what did the attacker do (shell commands, DB queries), what did they take (outbound transfers, DB read volumes). Decision D3 — rotation starts. | SOC, DEV |
| **T+6 h** | 6 h | Root cause identified (vulnerable component, injection point, weak admin credential). Hotfix tested. Decision D4. | DEV, PLATFORM |
| **T+12 h** | 12 h | Clean rebuild deployed with the fix, new secrets, hardened configuration. Monitoring tuned for recurrence. Decision D5/D6/D7. | PLATFORM, DPO |
| **T+24 h** | 24 h | Customer and regulator notifications if required. Search-engine / browser-warning removal requested. Insurer notified. | COMMS, LEGAL |
| **T+72 h** | 72 h | Hunt for lateral movement from the web tier complete. Personal-data clocks met. | SOC, DPO |
| **T+30 d** | 30 d | Post-incident review; AppSec backlog items assigned. | IM, DEV |

## 6. Communication templates

All templates are **fictional** examples for *Northwind Logistics*.

### Internal

> **Subject:** Security incident — [application] — restricted availability
>
> We have identified unauthorised activity affecting [application] and have placed it in maintenance mode while we
> investigate and rebuild. [Teams affected] should use [workaround]. Please do not discuss the cause externally and
> forward customer or press questions to [contact]. Incident manager: [name]. Next update: [time].

### Customers

> **Subject:** Security update regarding your Northwind Logistics account
>
> On [date] we identified unauthorised access to [application]. We immediately took the service offline, removed
> the cause and rebuilt the affected systems. Our investigation shows that [what was and was not affected]. As a
> precaution we have [logged out all users / reset passwords]. When you next log in you will be asked to [action].
> If you used your Northwind password elsewhere, please change it there too. [Card-data paragraph if applicable.]
> We are sorry for the concern this causes. Contact: [address].

### Regulator

Where personal data is involved follow [data-breach-personal-data](data-breach-personal-data.md). Technical facts
regulators ask for in web compromises: vulnerability exploited and how long it existed, first and last malicious
request timestamps, what the attacker could read or write, logging coverage (and gaps), whether the data was
encrypted at the application or database layer, and the evidence for your count of affected individuals.

### Press holding statement

> Northwind Logistics identified unauthorised access to [application] on [date]. The service was taken offline
> immediately, the issue was resolved and the service restored at [time]. We are contacting affected customers
> directly and have informed the relevant authorities. We will not comment further while our investigation is
> ongoing. Media contact: [name, address].

## 7. Evidence and chain of custody

- [ ] Snapshots / images of web, application and database tiers **before** remediation, with hashes and custodian.
- [ ] Web server, WAF, load-balancer and CDN logs for the full window (and 30 days before the first malicious request).
- [ ] The malicious artefacts (web shell, injected script, modified templates) preserved as files with hashes.
- [ ] Database audit / query logs; row counts of accessed tables to support the affected-individuals figure.
- [ ] Cloud / hosting account audit trail (role usage, key creation, instance changes).
- [ ] Source-control and CI/CD integrity check results (commit history, pipeline runs, deploy keys).
- [ ] Secrets-rotation log with timestamps.
- [ ] Decision log D1–D7, including the offline decision and who approved.

Chain of custody as in [templates/incident-record.md](../templates/incident-record.md). Keep the compromised
images isolated and never boot them on the production network.

## 8. Post-incident review

Use [templates/post-incident-review.md](../templates/post-incident-review.md), and additionally:

1. Was the vulnerability known (patch available, scanner finding, pentest item) before exploitation? Why was it open?
2. Dwell time: first malicious request to detection. Which log would have caught it earlier?
3. Could the web tier reach more than it needed (database rights, cloud role permissions, network paths)?
4. Were the secrets the attacker could reach stored and scoped correctly?
5. Did we have a clean, reproducible build to rebuild from? How long did the rebuild take?
6. Add the findings to the AppSec programme: SAST/DAST coverage, dependency management, WAF rules, admin-interface
   exposure, logging coverage; update this playbook.
