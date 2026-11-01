# Incident response plan: the ten use cases

An incident response plan is a set of use cases, one per type of incident, each with a playbook that says what
to do and in which order. This is the short form I keep at the front of the plan: ten use cases, the trigger,
and the sequence of actions. The full crisis-level playbooks in [`playbooks/`](../playbooks/) expand the ones
that put the organisation in front of a regulator or a customer.

Every use case follows the same spine: **identify, contain, eradicate, recover, learn.**

## 1. Phishing attack

**Trigger:** a user reports a suspicious email, or a security tool flags one; the risk is a click on a link or an attachment.

1. Confirm the email is malicious (headers, sender, content, links, attachments).
2. Find out who received it and who interacted with it (clicked, opened, replied).
3. Purge it from every mailbox; block the sender and the domain at the gateway; quarantine similar messages.
4. Reset credentials, revoke sessions and re-register MFA for the users who interacted; suspend the account if the evidence is strong.
5. Look for the attacker's next step: inbox rules, forwarding, consent grants, new devices, unusual sign-ins.
6. Tell the affected users what happened and what was done; feed the case into awareness training.
7. Close the loop: SPF, DKIM and DMARC enforcement, filtering rules, a one-click report button.

## 2. Ransomware infection

**Trigger:** files or systems are encrypted and a ransom note appears.

1. Isolate the affected systems immediately to stop the spread.
2. Identify the variant and the entry point.
3. Notify the authorities and meet the legal obligations.
4. Restore from clean backups after checking their integrity.
5. Investigate how the ransomware got in; patch the weakness it used.
6. Train users on what let it in.

## 3. Data breach or personal-data exposure

**Trigger:** unauthorised access to sensitive or personal data.

1. Confirm the breach from logs and alerts.
2. Scope it: which data, how many people, which systems.
3. Bring in Legal and Compliance for the regulatory clocks.
4. Contain: isolate the systems or accounts involved.
5. Forensic analysis of the attack path.
6. Notify the affected individuals with guidance.
7. Strengthen controls: access, encryption, monitoring.

## 4. Denial of service

**Trigger:** services disrupted by a flood of traffic.

1. Characterise the attack: volumetric, protocol or application layer.
2. Engage the ISP or cloud provider for mitigation.
3. Rate-limit and filter at the edge.
4. Use a DDoS protection service.
5. Monitor during and after the attack.
6. Record lessons learned; add redundancy.

## 5. Malware infection

**Trigger:** malware detected on one or more systems.

1. Isolate the infected systems.
2. Identify the malware type.
3. Remove or quarantine it with the endpoint protection.
4. Patch what let it in.
5. Full scan; look for lateral movement on other systems.
6. Rebuild the compromised systems if needed.
7. Educate users.

## 6. Insider threat

**Trigger:** a trusted person exposes data or harms systems, deliberately or not.

1. Monitor the behaviour with the tools you have (DLP, user analytics).
2. Investigate the person's actions.
3. Restrict their access to sensitive systems and data.
4. Involve HR and Legal.
5. Collect evidence and logs properly.
6. Take the appropriate action.
7. Tighten access control and activity monitoring.

## 7. Unauthorised access or account compromise

**Trigger:** someone is using an account or an administrative system without authorisation.

1. Disable or lock the compromised accounts.
2. Force password resets; make sure MFA is in place.
3. Find out how the account was compromised (phishing, brute force, reuse).
4. Review the systems the account touched.
5. Remove backdoors and unauthorised changes.
6. Strengthen account policies.

## 8. Privilege escalation

**Trigger:** an attacker or a user gains elevated privileges.

1. Identify the cause: vulnerability or misconfiguration.
2. Disable the compromised accounts immediately.
3. Roll back the unauthorised changes.
4. Patch the system or application.
5. Review permissions and access rights across the board.
6. Improve logging and monitoring to catch the next attempt.

## 9. Compromised third-party service

**Trigger:** a vendor or service provider is breached and your organisation is affected.

1. Get the details from the provider.
2. Analyse which data and services the provider holds for you.
3. Disable or limit the connections to the service if needed.
4. Put compensating controls in place: more monitoring, less access.
5. Check the contractual obligations; notify the stakeholders.
6. Watch your own systems for signs of compromise.

## 10. Advanced persistent threat

**Trigger:** a persistent, targeted intrusion over a long period.

1. Gather indicators of compromise from threat intelligence and monitoring.
2. Analyse network traffic for lateral movement.
3. Isolate the affected systems or network segments.
4. Bring in specialised threat-hunting or response capacity.
5. Patch, and remove backdoors and persistence mechanisms.
6. Raise the baseline: Zero Trust architecture, tiering, hardening.
7. Keep monitoring for the long term.

## The general steps, for every incident

1. **Identification**: detect through monitoring, alerts or reports.
2. **Containment**: isolate quickly to limit the damage.
3. **Eradication**: remove the threat from the systems and the network.
4. **Recovery**: restore systems and data; verify before going back online.
5. **Lessons learned**: a post-incident review that changes something.

See [tips-and-tricks.md](tips-and-tricks.md) for what running these in practice taught me.
