# Playbook — Lost or Stolen Device

| | |
|---|---|
| **Use when** | A laptop, phone, tablet, removable drive, hardware token or paper record containing company or personal data is lost, stolen, or left unattended somewhere it should not be. |
| **Default severity** | **S4 (Low)** for an encrypted, MDM-managed device wiped within the hour; **S3 (Medium)** if wipe cannot be confirmed; **S2 (High)** if unencrypted or holding personal / privileged data; **S1 (Critical)** for a privileged administrator's device or a device with cached production secrets. |
| **Incident manager** | IT Service Desk lead for S4/S3; Head of Security for S2/S1. |
| **Related SOC playbooks** | [credential-access](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/credential-access.md) · [cloud-account-compromise](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/cloud-account-compromise.md) |
| **Templates** | [incident-record](../templates/incident-record.md) · [timeline](../templates/timeline.csv) · [communication-log](../templates/communication-log.csv) · [post-incident-review](../templates/post-incident-review.md) |

> This is the most frequent incident most organisations have, and the one most likely to be under-reported because
> people are embarrassed. Make reporting painless and blame-free — the only wrong move is reporting late.
> The whole case turns on one question: **was the data on the device protected, and can we prove it?**

## 1. Scope and triggers

- User reports a loss via service desk, manager or the out-of-hours line.
- MDM reports a device offline for an unusual period, or a device checks in from an unexpected country.
- Police or a member of the public returns a device.
- A hardware MFA token or smart card is missing.
- Paper: printed customer lists, HR files, contracts left in a taxi, hotel or shared office.

**Not in scope**: a device that is found within the hour in the user's own home or desk — close as a near miss and
log it anyway (the pattern matters).

## 2. Severity matrix

| Factor | S4 Low | S3 Medium | S2 High | S1 Critical |
|---|---|---|---|---|
| Protection | Full-disk encryption **verified** in MDM, strong PIN, wiped | Encryption expected but not verifiable; wipe pending | No encryption, or weak/known PIN | Device had unlocked session, cached admin credentials or secrets |
| Data on device | Nothing beyond email cache | Internal documents | Personal data, customer data, source code | Special-category data, keys, privileged tooling |
| User's access level | Standard | Elevated in one system | Administrator | Domain / cloud / backup administrator |
| Circumstances | Lost, low-risk location | Lost, public place | Stolen opportunistically | Targeted theft (travel, executive, burglary with other items untouched) |
| Time to report | < 1 h | < 24 h | 1–7 days | > 7 days or discovered by a third party |

## 3. Roles

| Role | Responsibilities in this playbook |
|---|---|
| **Service desk** | First responder: account lock, MDM lock / wipe, device record, user support. |
| **Incident manager** | Severity, decisions, timeline for S2/S1. |
| **Identity / IT** | Session revocation, password and token resets, certificate revocation, conditional-access block. |
| **Security / SOC** | Monitor for use of the user's credentials and the device identity; check for sign-ins from the device after loss. |
| **DPO** | Personal-data assessment; notification clocks if data was not protected. |
| **HR** | Supports the user; policy follow-up only for repeated or negligent loss. |
| **Physical security / Facilities** | Building access card deactivation, CCTV, police liaison for on-site theft. |
| **Legal** | Police report, insurance claim, notification advice. |

## 4. Decision points

| # | Decision | Owner | Guidance |
|---|---|---|---|
| D1 | Lock or wipe? | SERVICE DESK | Lock immediately; wipe when the user confirms it is not simply misplaced, and always within 4 h for S2/S1. A wipe you cannot confirm is not a control — note "wipe pending" until the MDM reports success. |
| D2 | Was the data protected at rest? | IT + SECURITY | Only "yes" with evidence: MDM compliance record showing encryption status at last check-in, PIN policy, screen-lock timeout. Otherwise treat as unprotected. |
| D3 | Reset credentials and revoke sessions? | IDENTITY | Yes for every loss: password, refresh tokens, app passwords, certificates issued to the device, VPN profile, hardware token. Also any shared or service accounts the user knew. |
| D4 | Is personal data in scope? | DPO | If unprotected and personal data was on the device, follow [data-breach-personal-data](data-breach-personal-data.md). |
| D5 | Police report? | USER + LEGAL | Always for theft (insurance and regulator both expect a crime reference). |
| D6 | Can the device be trusted if recovered? | SECURITY | No — reimage before reuse; inspect for tampering if the theft was targeted. |

## 5. Timeline template

| Phase | Target | Actions | Owner |
|---|---|---|---|
| **T0 — Report** | 0 | Service desk opens ticket and incident record: device ID, user, last seen, circumstances, what was on it. Remote **lock** sent. | SERVICE DESK |
| **T+15 min** | 15 min | Sessions revoked, password reset, MFA re-registered, certificates / VPN profile revoked. Device marked lost in MDM; location requested where lawful. | IDENTITY |
| **T+1 h** | 1 h | Decision D1 (wipe) and D2 (protection evidence). Severity set. SOC check for sign-ins or device activity after the loss time. | SERVICE DESK, SECURITY |
| **T+4 h** | 4 h | Wipe confirmed or escalated. D3 completed, including shared accounts. D4 assessment if S2/S1. Building access card deactivated. | IT, DPO |
| **T+24 h** | 24 h | Police report filed (theft). Replacement device issued. Data inventory for the device finalised (email cache, synced folders, local files). | USER, SERVICE DESK |
| **T+72 h** | 72 h | Personal-data clocks met if triggered. Insurance claim submitted. | DPO, LEGAL |
| **T+14 d** | 14 d | Post-incident review for S2/S1; for S4/S3 a quarterly trend review of all device losses. | IM |

## 6. Communication templates

All templates are **fictional** examples for *Northwind Logistics*.

### Internal

> **Subject:** Lost device reported — actions completed
>
> [Name]'s [device] was reported [lost/stolen] on [date]. The device has been remotely locked and [wiped at (time) /
> a wipe is pending]. Their credentials and sessions have been reset. [Name], please complete the device data
> questionnaire at [link] so we can confirm what was stored locally, and file a police report if it was stolen
> (reference needed for insurance). No further action is needed from other staff. Reminder to all: report device loss
> immediately to [contact], 24/7 — there is no penalty for reporting.

### Customers

Only needed when D4 confirms unprotected personal data. Use the customer template in
[data-breach-personal-data](data-breach-personal-data.md), and state clearly whether the device was encrypted and
whether there is any evidence the data was accessed.

### Regulator

Needed only when D4 triggers notification. The regulator will ask specifically: encryption status and how you verified
it, lock/wipe timing and confirmation, PIN and screen-lock policy, whether the device was recovered, what data was
stored locally and how you know. Have the MDM compliance record and the wipe confirmation ready.

### Press holding statement

> A Northwind Logistics device was reported [lost/stolen] on [date]. The device was encrypted and has been remotely
> disabled, and we have no evidence that any information on it has been accessed. We have reported the matter to the
> police and [where applicable] to the relevant authorities. Media contact: [name, address].

## 7. Evidence and chain of custody

- [ ] User's report with time of loss, time of discovery, circumstances, and the local-data questionnaire.
- [ ] MDM records: last check-in, compliance (encryption, PIN), lock and wipe commands with timestamps and results.
- [ ] Identity actions: session revocation, password reset, token re-registration, certificate revocation — with timestamps.
- [ ] Sign-in and device logs for the account and device ID from the loss time onward.
- [ ] Police report reference; insurance claim reference.
- [ ] If recovered: photographs, tamper check, reimage record.
- [ ] Decision log D1–D6.

Chain of custody as in [templates/incident-record.md](../templates/incident-record.md). A recovered device is
evidence until Security releases it.

## 8. Post-incident review

Use [templates/post-incident-review.md](../templates/post-incident-review.md), and additionally:

1. Could we **prove** encryption from MDM data alone? If not, which devices in the fleet have the same gap?
2. How long between loss and report, and between report and lock? What slowed each?
3. Was there data on the device that should not have been (local copies, exports, unsynced folders)?
4. Did the user have admin rights or cached secrets they did not need?
5. Trend: losses per quarter, by device type and location. Are there hotspots (travel, specific sites)?
6. Update MDM policy, travel guidance, the reporting process and this playbook.
