# Playbook — Supply-Chain and Vendor Compromise

| | |
|---|---|
| **Use when** | A supplier, managed service provider, SaaS vendor, software dependency or build pipeline you rely on has been compromised, and the compromise can reach your data, your network or your customers. |
| **Default severity** | **S2 (High)** on notification; **S1 (Critical)** if the vendor holds privileged access to your environment (MSP, identity, EDR, backup, remote-support tooling) or the compromised component is deployed in production. |
| **Incident manager** | Head of Security; Procurement / Vendor Management co-leads. |
| **Related SOC playbooks** | [lateral-movement](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/lateral-movement.md) · [cloud-account-compromise](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/cloud-account-compromise.md) · [credential-access](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/credential-access.md) |
| **Templates** | [incident-record](../templates/incident-record.md) · [timeline](../templates/timeline.csv) · [communication-log](../templates/communication-log.csv) · [post-incident-review](../templates/post-incident-review.md) |

> You cannot investigate the vendor's network. What you **can** do: decide fast whether to cut the connection,
> find out what the vendor could reach, verify your own environment, and manage the obligations flowing to **your**
> customers. The hardest part is usually getting facts out of the vendor — plan for that.

## 1. Scope and triggers

- Vendor notifies you of a breach (email, portal notice, press release you saw first).
- Public disclosure: a widely used product (VPN appliance, file-transfer tool, library, CI action) is reported compromised or carries a critical zero-day being exploited.
- Your SOC sees suspicious activity from a vendor account, vendor IP range or vendor-managed system.
- A software update or package behaves unexpectedly (new outbound connections, unknown binaries).
- A customer of **yours** reports that your deliverable (code, document, update) is malicious.

**Three variants** — record which one applies, as the response differs:

| Variant | Example (fictional) | Your main exposure |
|---|---|---|
| **A. Service provider with access** | MSP "Contoso Managed IT" runs your help desk with domain admin | Their credentials and tooling reach your environment |
| **B. Data processor** | SaaS payroll "Fabrikam People" stores your HR data | Your data on their systems — personal-data clocks may run |
| **C. Software / component** | A library or vendor update in your product or pipeline | Malicious code running in your environment or shipped to your customers |

## 2. Severity matrix

| Factor | S4 Low | S3 Medium | S2 High | S1 Critical |
|---|---|---|---|---|
| Vendor access | None (data only, non-sensitive) | Standard user accounts | Admin to one platform | Admin to identity, EDR, backup, network or remote-support |
| Data held by vendor | Public / internal | Confidential | Personal data | Special-category or regulated data at scale |
| Component exposure (variant C) | Not deployed | Deployed in dev/test | Deployed in production | Shipped to your customers |
| Evidence of impact on you | None | Suspicious, unconfirmed | Confirmed access to your environment | Confirmed data loss or ongoing access |
| Vendor transparency | Full, timely | Partial | Slow / vague | Silent or disputing |

## 3. Roles

| Role | Responsibilities in this playbook |
|---|---|
| **Incident manager** | Owns timeline, vendor liaison cadence, decides on disconnection with the business owner. |
| **Vendor manager / Procurement** | Contract, SLAs, breach-notification clauses, right-to-audit, commercial leverage. |
| **Legal counsel** | Liability, obligations to your customers, regulator notification, evidence demands to the vendor. |
| **IT / SOC** | Vendor access inventory, isolation, hunting for the vendor's indicators in your environment. |
| **Business owner of the service** | Impact of disconnection, workarounds, alternative suppliers. |
| **Comms** | Customer messaging if your deliverables or data are affected; alignment with the vendor's public statements. |
| **Product / Engineering** (variant C) | SBOM lookup, dependency pinning, rebuild and re-release. |
| **Executive sponsor** | Disconnection decision for critical vendors, contractual escalation. |

## 4. Decision points

| # | Decision | Owner | Guidance |
|---|---|---|---|
| D1 | Disconnect the vendor now, restrict, or monitor? | IM + OWNER (+ EXEC for critical services) | Disconnect immediately when the vendor had privileged access and cannot confirm the scope. Restrict (rotate credentials, remove standing access, enable just-in-time) when impact is unconfirmed. |
| D2 | Rotate credentials and secrets shared with or known to the vendor? | IT | Yes, always — including API keys, service accounts, VPN certificates, shared mailboxes, and any secret in a vendor ticketing system. |
| D3 | Treat the vendor's indicators as present in our environment? | IM | Yes until a hunt over the full vendor-access window comes back clean. |
| D4 | Variant C: roll back, patch, or rebuild? | ENG | Roll back to a verified build, pin the dependency, rebuild from clean sources, re-sign, re-release. |
| D5 | Are our customers' data or deliverables affected? Do we notify them? | LEGAL + COMMS | Follow contracts and the [personal-data clocks](data-breach-personal-data.md) — the vendor's delay is not your defence. |
| D6 | Invoke contractual remedies (audit, indemnity, termination)? | PROCUREMENT + LEGAL | After containment; capture the facts for it now. |
| D7 | Continue with the vendor after the incident? | EXEC on IM recommendation | Based on their transparency, root cause and remediation evidence. |

## 5. Timeline template

| Phase | Target | Actions | Owner |
|---|---|---|---|
| **T0 — Notification** | 0 | Open incident record; record how and when you learned, and what the vendor says. Identify the variant. Name a single vendor liaison. | IM |
| **T+1 h** | 1 h | Inventory the vendor's access: accounts, VPN, API keys, agents installed, data shared, network paths. Decision D1. Credential rotation started (D2). | IT, IM |
| **T+4 h** | 4 h | Hunt for the vendor's indicators and vendor-account activity over the full access window. Contract review for breach-notification and SLA clauses. Written questions sent to the vendor (see regulator section for the list). | SOC, LEGAL |
| **T+24 h** | 24 h | Vendor fact call held and minuted. Variant C: SBOM searched, affected builds identified, rollback or pin completed. Decision D5 on customer notification. Insurer notified if impact confirmed. | IM, ENG, LEGAL |
| **T+72 h** | 72 h | Hunt concluded or extended with reasons. Customers / regulators notified where required. Vendor remediation evidence requested in writing. | IM, COMMS |
| **T+14 d** | 14 d | Vendor root-cause report received and reviewed. Access re-enabled under new conditions (JIT, MFA, logging) or kept off. | IM, PROCUREMENT |
| **T+30 d** | 30 d | Post-incident review including the vendor-risk programme. Contract amendments drafted. | IM, PROCUREMENT |

## 6. Communication templates

All templates are **fictional** examples for *Northwind Logistics* and its fictional supplier *Contoso Managed IT*.

### Internal

> **Subject:** Supplier security incident — Contoso Managed IT — action required
>
> Contoso, which provides our [service], has reported a security incident on their side. As a precaution we have
> suspended their access to our systems and rotated the credentials they used. You may notice [impact, e.g. slower
> help-desk response]. If you receive emails or calls claiming to be from Contoso asking for passwords, codes or
> remote access, do not act — report them to [SOC contact]. Incident manager: [name]. Next update: [time].

### Customers

> **Subject:** Information about a supplier security incident
>
> One of our suppliers, [vendor], has notified us of a security incident affecting their systems. We have suspended
> the supplier's access and reviewed our own environment. [Based on our review to date, your data/services were not
> affected. / The following information relating to you may have been affected: (categories).] We have [actions].
> We will update you by [date] or sooner if the situation changes. Contact: [address].

### Regulator

Where personal or regulated data is involved use the regulator section of
[data-breach-personal-data](data-breach-personal-data.md). In addition, document the **questions put to the vendor**
and their answers — regulators expect you to have asked:

1. What happened, when did it start, when did you become aware?
2. Which of our accounts, data sets, systems or deliverables were accessible or accessed?
3. What indicators (IPs, hashes, accounts, time windows) should we hunt for?
4. What has been contained and what remains at risk?
5. Which authorities have you notified?
6. When will the forensic report be available to us?

### Press holding statement

> Northwind Logistics is aware of a security incident reported by one of our suppliers. We have taken precautionary
> measures, including suspending the supplier's access to our systems, and are reviewing our environment with
> external specialists. At this time we have no evidence of impact to our customers. We will provide further
> information if that changes. Media contact: [name, address].

## 7. Evidence and chain of custody

- [ ] The vendor's notification(s) as received, with headers / portal screenshots and timestamps.
- [ ] Vendor access inventory at T+1 h (exported, hashed) and the rotation / revocation log.
- [ ] Hunt scope, queries, results and the analyst who ran them, over the full vendor-access window.
- [ ] Variant C: the affected artefact (package, update, binary) with hashes, the SBOM extract, build logs, signatures.
- [ ] Minutes of every vendor call, written Q&A, the vendor's root-cause report.
- [ ] Contract extracts relied upon (notification clause, right to audit, liability cap).
- [ ] Decision log D1–D7.

Chain of custody as in [templates/incident-record.md](../templates/incident-record.md). Keep vendor-supplied
artefacts separate from your own evidence and label their origin.

## 8. Post-incident review

Use [templates/post-incident-review.md](../templates/post-incident-review.md), and additionally:

1. Did we know this vendor's access and data footprint before the incident, or did we discover it during?
2. Was standing privileged access necessary? Can it become just-in-time with approval and session recording?
3. Did the contract give us the notification timeline, indicators and audit rights we needed? Amend the template.
4. Variant C: is there an SBOM for every product and pipeline? Are dependencies pinned and verified?
5. How did the vendor perform (speed, transparency, remediation)? Update the vendor risk rating.
6. Which single vendors are "too critical to lose"? Do we have an exit plan for them?
