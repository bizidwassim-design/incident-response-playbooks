# Incident response tips and tricks

Field notes from running detection and response in a Microsoft Defender XDR and Active Directory environment.
Everything below is written in general terms: no organisation, host, account or person is named, and the
numbers are rounded. Use them as a checklist, not as a procedure to copy.

## 1. Automated isolation: arm it for workstations, never for servers

* Put a **second layer** behind native Tamper Protection: a custom detection rule that fires on *real*
  disable signals (command lines such as `DisableRealtimeMonitoring`, `sc stop WinDefend`, registry values set
  to `1`, `AntivirusDisabled` events, and antivirus **exclusions** added with `Add-MpPreference`). Map it to
  MITRE ATT&CK **T1562.001**. See [`detections/defender-tamper-custom-detection.kql`](../detections/defender-tamper-custom-detection.kql).
* Split it in **two rules**: one that auto-isolates (full isolation plus investigation package) and is limited
  to devices matching your **workstation naming convention**, and a twin rule for everything else that only
  **alerts**. Isolating a domain controller or a terminal server by reflex cuts dozens of people off; a server
  is a human decision.
* Keep an **exclusion list** written down before you arm anything: domain controllers, the identity sync
  server, the certificate authority, production databases, OT and HMI stations, backup appliances, time
  clocks, laboratory equipment, kiosks. Every device outside the naming convention gets the alert-only rule.
* Exclude the accounts and virtual machines used for **IR exercises and penetration tests**; they disable
  protections on purpose.

## 2. Tune before you trust

* `TamperingAttempt` events raised by `svchost -k GPSvcGroup` and `WmiPrvSE` at logon are benign and frequent
  (a dozen a day is normal). Never alert on them alone.
* Registry changes to antivirus exclusions are far too noisy when GPO or Intune manage them (millions of
  events a month). Detect the **command** instead (`Add-MpPreference`) and exclude the script path of your
  RMM agent, which is usually the only legitimate caller.
* A device that has just been isolated shows `ConnectionFailed` everywhere. It looks like sabotage; it is the
  isolation itself. Do not include it in the detection.
* Align the query window with the rule's look-back. A rule that runs hourly with a four-hour look-back needs
  `ago(4h)` in the query, or events can fall between two runs.
* Validate on **30 days of history** and require zero false positives before enabling any automatic action.

## 3. Check the suppression rules you inherited

Alert tuning rules outlive the tools they were written for. One "resolve alert: possible tampering with
protected processes" rule, created for an EDR that had since been removed, was silently closing Microsoft's
own tampering alert. Review every suppression and tuning rule when a product is decommissioned, and again
before you rely on an alert for a new response.

## 4. Test the whole chain, on a spare machine

* Trigger the rule from a **spare workstation** that nobody uses (online, no interactive logon for two weeks),
  with a dedicated test admin account that is **not** in the rule's exclusions.
* Never test on the analyst's own machine: a full isolation also cuts the Defender portal, Teams and Outlook
  for the person running the test.
* Expected within one rule cycle: the alert, the isolation, the investigation package, the notification
  emails. Record the observed delays.
* Test **release from isolation** before you need it, and keep remote-management access to the test device
  during the exercise.

## 5. Have the release procedure written before the first isolation

1. **Signal**: the "device isolated" notification and the high-severity incident.
2. **Ownership**: the on-call analyst, a deputy, a target response time in office hours, and the after-hours
   arrangement, all named in advance.
3. **Call the user**: the device has no network, so the phone is the only channel. Script the message: "Your
   computer was isolated automatically after a security alert. Do not turn it off; IT will call you back
   within *n* minutes."
4. **Analyse**: the signal, the detail and the actor columns of the alert, the investigation package, the
   device timeline. Check first whether it was a legitimate IT action through the RMM or a technician.
5. **Decide**: false positive or legitimate action, release with a comment and adjust the query; true positive,
   keep it isolated, open an incident, reset the user's account in the directory, full scan, rebuild if needed.
6. **Trace**: a comment in the incident and a work log on the ticket.

## 6. Everything starts in simulation

Hunting queries are read-only. Response scripts run in **simulation by default** and need an explicit
`-Execute` switch. Moving a response from simulation to live is a separate, human decision taken after
weeks without false positives. Writing this rule down at the top of every playbook keeps the pressure of an
incident from turning a test into an outage.

## 7. After a penetration test: one hunt and one response per threat

Turn each finding into a pair: an **investigation** query (KQL in advanced hunting, or PowerShell for
directory objects) and a **response** (a KQL rule for isolation or a PowerShell script in simulation mode).
A useful set:

| Threat | Investigation | Response |
|--------|---------------|----------|
| Reconnaissance and group enumeration | Who enumerates privileged groups over SAMR or LDAP | Watch list; a honeytoken if the noise allows |
| Kerberoasting | RC4 service-ticket requests for accounts with SPNs | Move service accounts to AES-only, then rotate their passwords |
| NTLM coercion and relay | Machine-account NTLM authentications to unexpected targets | SMB signing everywhere; alert on relay patterns |
| Resource-based constrained delegation | Accounts with a populated `msDS-AllowedToActOnBehalfOfOtherIdentity` | Clear the attribute **before** rotating the usurpable accounts |
| LSA secrets theft | Processes opening `lsass` with a PowerShell parent | LSA Protection (RunAsPPL) on servers with privileged logons |
| Over-scoped service accounts | Accounts authenticating on more than *n* hosts | Restrict scope; a monitoring account seen on a hundred hosts is the usual finding |
| Password spraying | One source, many accounts, short window; exclude cloud noise | Alert and block at the identity provider |
| Blast radius | Non-DC hosts where hundreds of distinct identities log on | Privileged access workstations, Credential Guard, tiering |
| Exposed test accounts | Accounts named like tests with a real logon history | Inventory, disable, force password change, one by one |

Refine the noisy ones with the real data: the first version of the LSA hunt returned 86 signals, the refined
version 7, and one of the 7 was worth an investigation.

## 8. Priority-zero hardening that closes whole classes of attack

* Admin accounts marked **not delegable** and in **Protected Users**: closes resource-based delegation abuse.
* **SMB signing** on every host that can be relayed: closes NTLM relay.
* **LSA Protection** on servers with privileged logons: raises the cost of credential dumping.
* Clear delegation attributes **before** rotating passwords, or the rotation does not help.

## 9. A lightweight SOAR without a SIEM

Notification and traceability can be built with the tools you already have: a workflow engine (Power
Automate or equivalent), the collaboration tool (Teams adaptive cards with approve and release buttons), the
ITSM for the work log, and email for escalation only.

* **Use case 1, traceability first**: every alert creates a ticket and the ticket number is written back as an
  incident comment. No action at all. Enable this one first.
* **Use case 2, notify on any isolation**: poll the endpoint API's machine actions. Polling catches every
  isolation, whether a rule, automatic attack disruption or an analyst did it.
* **Use case 3, human approval before isolating a server**: the workflow isolates only on a click.
* **Identity**: a dedicated app registration with the four permissions needed and nothing more (read alerts,
  read and write incidents, read machines, isolate machines); a certificate rather than a secret, stored in
  a key vault; Conditional Access on the app. Never reuse a broad app that exists for another purpose. The
  isolate permission can isolate the whole fleet; treat it as domain-admin grade.
* The custom detection rule's response action isolates natively; the app does not need the isolate permission
  for that path.

## 10. Phishing: remove, reset, re-register

* Confirm the email is malicious, then **purge it from every mailbox** with a compliance search and a hard
  delete; block the sender and the domain at the gateway; quarantine similar messages still in transit.
* Find who **interacted**: link clicks, attachment opens, sign-ins that follow. Reset those passwords, revoke
  sessions and **re-register MFA**; suspend the account while the investigation runs if the evidence is strong.
* Look for the attacker's next step: inbox rules, forwarding, consent grants, new devices, unusual sign-ins.
* Close the loop with SPF, DKIM and DMARC enforcement, phishing simulations and a one-click report button.

## 11. Post-phishing browser hygiene for the user

Give the user (or the technician helping them) a ten-minute checklist per browser:

1. Wait until IT confirms the **password has been reset**; the new password is needed to sign back in.
2. **Sign out** of the browser profile (and turn off sync in Chrome).
3. Clear, for **all time**: cookies and site data, cached files, saved passwords, autofill data.
4. Delete every saved password for the identity provider and the office suite; when in doubt, delete all.
5. Close the browser completely, wait a few seconds, reopen.
6. Sign in again with the new password and approve the MFA prompt; if asked to re-register authentication,
   that is expected.

Red flags that mean "call IT, click nothing": a password prompt on a page that is not the identity provider's
sign-in page, an MFA prompt the user did not trigger, an unusual pop-up, a password that "stops working"
repeatedly. And never forward the suspicious email to a colleague; delete it.

Track completion per user in a small table (profile signed out, cookies cleared, passwords removed,
re-signed in with MFA). It takes two minutes and proves the hygiene step was done.

## 12. The ten use cases every plan should cover

Phishing, ransomware, data breach or personal-data exposure, denial of service, malware, insider threat,
account compromise, privilege escalation, compromised third party, advanced persistent threat. Each one with
the same spine: identify, contain, eradicate, recover, learn. The playbooks in this repository follow it.
