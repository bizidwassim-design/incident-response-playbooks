# Playbook — Privileged Account Compromise

| | |
|---|---|
| **Use when** | An account with administrative rights — domain admin, cloud tenant / subscription owner, identity-provider admin, EDR or backup console admin, hypervisor or network admin, CI/CD or secrets-manager admin — is confirmed or strongly suspected to be under attacker control. |
| **Default severity** | **S1 (Critical)**. Downgrade to S2 only when the privilege is confined to a single non-critical system and the attacker's activity is fully scoped. |
| **Incident manager** | Head of Security. Identity lead and Infrastructure lead co-lead. |
| **Related SOC playbooks** | [credential-access](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/credential-access.md) · [cloud-account-compromise](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/cloud-account-compromise.md) · [lateral-movement](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/lateral-movement.md) · [ransomware](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/ransomware.md) |
| **Templates** | [incident-record](../templates/incident-record.md) · [timeline](../templates/timeline.csv) · [communication-log](../templates/communication-log.csv) · [post-incident-review](../templates/post-incident-review.md) |

> A compromised administrator means the attacker can read your incident channel, disable your EDR and delete your
> backups. The first decisions are about **where you communicate and who you trust**, not about which logs to pull.
> The technical steps (session revocation, credential rotation, hunting) are in the linked SOC playbooks; this one
> governs the crisis around them.

## 1. Scope and triggers

- SOC confirms attacker activity under an admin identity (impossible travel for a global admin, MFA method added,
  new app registration with broad consent, backup job changes, EDR exclusions created, group-policy changes).
- Privileged credentials found in a dump, a paste site, or a ransomware negotiation chat.
- A phishing or MFA-fatigue report from an administrator who approved a prompt.
- An MSP or vendor with admin access reports a compromise (see [supply-chain-vendor-compromise](supply-chain-vendor-compromise.md)).
- Discovery during another incident (web shell with cached domain credentials, ransomware precursor).

**Tiers** — record which tier is compromised; everything the tier controls is in scope:

| Tier | Examples | Blast radius |
|---|---|---|
| **0 — Identity and control plane** | Domain admin, identity-provider global admin, cloud tenant root/owner, PKI, backup console, EDR console, hypervisor | Everything |
| **1 — Platforms** | Server admin, database admin, network admin, CI/CD admin, secrets manager | All workloads on the platform |
| **2 — Applications** | SaaS admin, application admin | That application and its data |

## 2. Severity matrix

| Factor | S4 Low | S3 Medium | S2 High | S1 Critical |
|---|---|---|---|---|
| Tier | — | Tier 2 single application | Tier 1 | Tier 0 or any tier with evidence of use |
| Attacker activity | Credential exposed, no use | Logon only | Persistence created (new accounts, apps, keys, MFA methods) | Security controls altered, backups touched, data accessed, lateral movement |
| Dwell time | < 1 h | < 24 h | Days | Weeks or unknown |
| Containment confidence | Credential rotated, no sessions | Sessions revoked, persistence unknown | Persistence partially found | Control plane integrity cannot be trusted |

## 3. Roles

| Role | Responsibilities in this playbook |
|---|---|
| **Incident manager** | Out-of-band bridge, trusted-circle list, timeline, decisions. |
| **Identity lead** | Break-glass accounts, session and token revocation, MFA reset, app-consent review, rotation plan. |
| **Infrastructure / Platform lead** | Backup integrity, EDR and logging integrity, hypervisor and network control plane. |
| **SOC / Forensics** | Scoping the attacker's actions under the privileged identity, persistence hunt, timeline. |
| **Legal** | Privilege, insurer, law enforcement, regulator and contractual duties if data was accessed. |
| **Comms** | Internal messaging without alerting the attacker; external statements only if impact is confirmed. |
| **HR** | If the account owner is suspected of complicity; welfare of the administrator (they often feel responsible). |
| **Executive sponsor** | Approves disruptive containment (forcing all sessions out, taking identity services offline), spend on external IR. |

## 4. Decision points

| # | Decision | Owner | Guidance |
|---|---|---|---|
| D1 | Move the response to an **out-of-band** channel? | IM | Yes for Tier 0 and Tier 1 — separate messaging/collaboration tenant or phones; assume email and chat are read. |
| D2 | Who is in the trusted circle? | IM + EXEC | Minimum people needed; verify each by voice/in person; no shared mailboxes. |
| D3 | Contain fast (revoke everything now, visibly) or watch briefly to scope? | IM + EXEC | Contain now if backups, EDR or data are at risk — which for Tier 0 is always. Watching is only acceptable with evidence capture running and the attacker unable to reach backups and control planes. |
| D4 | Use break-glass accounts and rotate the compromised tier? | IDENTITY | Yes. Break-glass first, then rotate every credential in the tier, including the ones "nobody uses". Domain-level secrets (e.g. the Kerberos ticket-granting account) twice, with the required interval. |
| D5 | Trust the EDR, SIEM and backup consoles? | PLATFORM + SOC | Verify their admin audit logs for the dwell period before relying on them; validate backups from a separate copy. |
| D6 | Take identity services or the network offline? | EXEC on IM advice | Only when the attacker is actively destroying or you cannot evict them otherwise; prepare the business for it. |
| D7 | Engage external IR / forensics; notify insurer, law enforcement? | IM + LEGAL | Yes for Tier 0; insurer within their notice period; law enforcement for extortion or data theft. |
| D8 | Declare "evicted"? | IM + SOC | After full rotation, persistence hunt over the whole dwell period clean, and 72 h of clean monitoring. |

## 5. Timeline template

| Phase | Target | Actions | Owner |
|---|---|---|---|
| **T0 — Confirmation** | 0 | Open incident record on the out-of-band channel (D1). Trusted circle named (D2). Evidence preservation ordered (identity logs, admin audit logs, EDR, backups). | IM |
| **T+30 min** | 30 min | Decision D3. Break-glass accounts verified. Compromised account disabled; all sessions and refresh tokens revoked; MFA methods reset. Backup repositories locked / immutable copy verified. | IDENTITY, PLATFORM |
| **T+2 h** | 2 h | Scope attacker actions under the identity: logons, changes, consents, new credentials, group memberships, mailbox rules, policies. Persistence hunt begins. External IR engaged if Tier 0 (D7). | SOC |
| **T+8 h** | 8 h | Tier-wide rotation plan executed (D4). EDR / SIEM / backup console integrity verified (D5). Internal note to staff about forced sign-outs. | IDENTITY, PLATFORM, COMMS |
| **T+24 h** | 24 h | Attacker objective assessed (ransomware staging, data theft, espionage). Data-access evidence reviewed with Legal — personal-data clocks if applicable. Insurer and law enforcement informed. | IM, LEGAL |
| **T+72 h** | 72 h | Persistence hunt complete over the dwell period. Monitoring clean. Decision D8 or extension with reasons. | SOC, IM |
| **T+14 d** | 14 d | Hardening: tiering enforced, standing admin removed, phishing-resistant MFA for admins, admin workstations. | IDENTITY |
| **T+30 d** | 30 d | Post-incident review. | IM |

## 6. Communication templates

All templates are **fictional** examples for *Northwind Logistics*. Send **nothing** on the suspected-compromised
platforms that reveals what you know.

### Internal

> **Subject:** Mandatory sign-out and password change — [date]
>
> As part of a security maintenance action, all staff will be signed out of [services] at [time] and must sign in
> again and register MFA. Administrators will receive separate instructions by phone from [name]. If you receive
> sign-in prompts or MFA requests you did not initiate, deny them and report to [contact]. Thank you for your
> patience — this is precautionary.

### Customers

Only if customer data or services were affected — then use the customer template in
[data-breach-personal-data](data-breach-personal-data.md) or [web-application-compromise](web-application-compromise.md).
Otherwise, do not communicate externally.

### Regulator

Where data was accessed, follow the regulator section of [data-breach-personal-data](data-breach-personal-data.md).
Expect additional questions on: how the privileged credential was obtained, whether MFA was enforced for admins, the
dwell time, what security controls the attacker altered, and backup integrity.

### Press holding statement

> Northwind Logistics identified unauthorised access to part of its IT environment on [date] and immediately
> initiated its incident response process with external specialists. We have contained the access and our services
> are operating normally. We are assessing whether any data was affected and will contact anyone concerned directly.
> Media contact: [name, address].

## 7. Evidence and chain of custody

- [ ] Identity-provider sign-in and audit logs for the account and the whole tier over the dwell period (exported from a separate, trusted admin session; hashed).
- [ ] Admin audit logs for EDR, SIEM, backup, hypervisor, network and cloud control planes over the same period.
- [ ] Snapshot of privileged group memberships, app registrations / consents, API keys, service principals, MFA methods — **before** and **after** rotation.
- [ ] Break-glass usage log; rotation log with timestamps and operators.
- [ ] Forensic images or EDR timelines for admin workstations and jump hosts.
- [ ] Backup integrity verification record.
- [ ] Out-of-band channel membership list and decision log D1–D8.

Chain of custody as in [templates/incident-record.md](../templates/incident-record.md). Store evidence outside the
compromised tenant / domain.

## 8. Post-incident review

Use [templates/post-incident-review.md](../templates/post-incident-review.md), and additionally:

1. How was the credential obtained — phishing, MFA fatigue, token theft, reuse, vendor, cached on a workstation?
2. Was the account's privilege standing or just-in-time? Did the account need it at all?
3. Was MFA phishing-resistant for this tier? Was the admin working from a dedicated, hardened workstation?
4. Did tiering hold — could the attacker reach backups, EDR or the identity provider from a lower tier?
5. How long did rotation take, and which credentials were forgotten the first time?
6. Was the out-of-band channel ready, or improvised? Update the crisis communication plan, the privileged-access
   model and this playbook.
