# Playbook — Distributed Denial of Service (DDoS)

| | |
|---|---|
| **Use when** | A public-facing service (website, API, VPN, DNS, email gateway) is degraded or unavailable because of deliberately generated traffic, or you have received a DDoS extortion threat. |
| **Default severity** | **S3 (Medium)** for a non-critical site; **S2 (High)** when customer-facing revenue or operations are hit; **S1 (Critical)** when safety, regulated services or the VPN used by all staff are down for more than one hour. |
| **Incident manager** | Head of Infrastructure or Security; Network lead co-leads. |
| **Related SOC playbooks** | None directly — DDoS is rarely an intrusion. Watch for it being used as a **smokescreen**: run [credential-access](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/credential-access.md) and [data-exfiltration](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/data-exfiltration.md) checks in parallel. |
| **Templates** | [incident-record](../templates/incident-record.md) · [timeline](../templates/timeline.csv) · [communication-log](../templates/communication-log.csv) · [post-incident-review](../templates/post-incident-review.md) |

> A DDoS is an **availability** incident with a **communication** problem. Customers notice before you do, and
> the business wants a restore time you cannot promise. Decide early what you will say, keep saying it on a schedule,
> and do not negotiate with extortionists.

## 1. Scope and triggers

- Monitoring: latency, error rate or saturation alarms on edge devices, load balancers, CDN or WAF.
- Upstream provider / CDN alert of volumetric attack.
- Customer complaints or social-media reports that the site is down.
- Extortion email ("pay X or we take you down") — with or without a demonstration attack.
- Unexplained outage where capacity is the obvious symptom (bandwidth, connection tables, CPU on the edge).

**Classify the attack** once you have data: *volumetric* (bandwidth), *protocol / state exhaustion* (SYN, UDP,
connection tables on firewalls and VPN), *application layer* (expensive requests, login endpoints, search). The
mitigation differs — volumetric needs upstream scrubbing; application layer needs rate limiting and caching rules.

## 2. Severity matrix

| Factor | S4 Low | S3 Medium | S2 High | S1 Critical |
|---|---|---|---|---|
| Service affected | Marketing site, no transactions | Internal tools, partner portal | Customer transactions, API, email flow | Safety-related, regulated service, all-staff VPN |
| Duration / recurrence | < 30 min, once | < 2 h | > 2 h or repeated same day | > 8 h or multi-day campaign |
| Mitigation status | Auto-mitigated | Mitigated with manual rules | Partial — degraded | Not mitigated; upstream saturated |
| Extortion | None | Threat without attack | Threat with demonstration | Attack ongoing with ransom demand |
| Collateral | None | Shared infrastructure affected | Other tenants / partners affected | Smokescreen for intrusion suspected |

## 3. Roles

| Role | Responsibilities in this playbook |
|---|---|
| **Incident manager** | Timeline, severity, decision owner, bridge cadence. |
| **Network / Infrastructure lead** | Attack characterisation, mitigation with ISP / CDN / scrubbing provider, capacity actions. |
| **Application owner** | Which endpoints are hit, what can be cached, degraded or turned off. |
| **SOC** | Parallel hunt for intrusion; monitor the extortion mailbox; log preservation. |
| **Comms** | Status page, customer messaging, social monitoring, press holding statement. |
| **Legal** | Extortion handling, law-enforcement report, contractual SLA implications. |
| **Customer service** | Scripts, call volumes, escalations. |
| **Executive sponsor** | Approves any spend (emergency scrubbing contract), any statement, the no-payment position. |

## 4. Decision points

| # | Decision | Owner | Guidance |
|---|---|---|---|
| D1 | Engage the upstream scrubbing / CDN provider now? | NETWORK + IM | Yes as soon as volumetric or protocol attack is confirmed; most contracts allow emergency onboarding within hours — know yours before the day. |
| D2 | Geo-block, rate-limit or challenge (CAPTCHA) traffic? | APP OWNER + NETWORK | Start with rate limits per endpoint and challenges on login/search; geo-blocking only with business owner approval and an exception path for travelling staff. |
| D3 | Turn off non-essential features or whole services to protect the core? | APP OWNER + EXEC | Degrade gracefully: static pages, read-only mode, queueing. Pre-agree the order of sacrifice. |
| D4 | Public statement: status page only, or proactive customer email? | COMMS + IM | Status page within 30 min of customer-visible impact; email if the outage exceeds the SLA or affects transactions. |
| D5 | Respond to extortion? | LEGAL + EXEC | Do not reply, do not pay. Preserve the message. Report to law enforcement. |
| D6 | Invoke business continuity (alternate site, manual processes)? | IM + BUSINESS | When restore time estimate exceeds the maximum tolerable downtime in the BIA. |
| D7 | Stand down? | IM | When traffic is back to baseline for 2 h **and** the intrusion hunt is clean. Keep mitigations for 7 days. |

## 5. Timeline template

| Phase | Target | Actions | Owner |
|---|---|---|---|
| **T0 — Detection** | 0 | Open the incident record; confirm it is an attack, not a failure or a legitimate spike. Capture flow samples and edge metrics. | NETWORK, IM |
| **T+15 min** | 15 min | Characterise (volumetric / protocol / application), targets, source profile. Decision D1. Bridge opened. | NETWORK |
| **T+30 min** | 30 min | Status page updated. Customer-service script issued. Scrubbing / CDN mitigations active. Decision D2. | COMMS, NETWORK |
| **T+1 h** | 1 h | Decision D3 if still degraded. SOC confirms no parallel intrusion (auth anomalies, new admin sessions, outbound transfers). Legal briefed if extortion. | APP OWNER, SOC |
| **T+2 h** | 2 h | Hourly update cadence set. Decision D6 if restore estimate exceeds tolerance. Insurer notified for S1/S2. | IM, COMMS |
| **Restore + 2 h** | — | Decision D7 stand down; mitigations kept; monitoring raised for 7 days. Customer closure note sent. | IM, COMMS |
| **T+14 d** | 14 d | Post-incident review; capacity and contract actions assigned. | IM |

## 6. Communication templates

All templates are **fictional** examples for *Northwind Logistics*.

### Internal

> **Subject:** Service disruption — [service] — DDoS in progress
>
> [Service] is being targeted by a denial-of-service attack. The network team is working with our providers to
> filter the traffic. Expect [impact]. Customer-facing staff: please use the approved script at [link] and do not
> speculate about the cause. Do not post about this on social media. Updates every hour on [channel].

### Customers

> **Subject:** Service disruption affecting [service]
>
> Since [time, timezone] some customers have been unable to [action] due to a high volume of malicious traffic
> directed at our systems. There is no indication that customer data has been affected. Our teams and our network
> providers are actively filtering the traffic and service is [partially restored / expected to be restored by]. We
> will post updates at [status page URL]. We apologise for the disruption.

### Regulator

DDoS alone rarely triggers data-protection notification, but may trigger **operational-resilience or sector**
reporting (financial, telecom, critical infrastructure). Prepare: start time, services affected, duration, customer
impact, mitigation steps, whether an extortion demand was received, and whether law enforcement was informed.

### Press holding statement

> Northwind Logistics experienced a disruption to [service] on [date] caused by a denial-of-service attack. Our
> teams, working with our network providers, restored service at [time]. We have no indication that any customer
> data was accessed. We have reported the matter to the relevant authorities. Media contact: [name, address].

## 7. Evidence and chain of custody

- [ ] Flow / packet samples and edge metrics (bandwidth, packets per second, connections) across the attack, exported with timestamps.
- [ ] CDN / WAF / scrubbing-provider reports and the mitigation rules applied, with who applied them and when.
- [ ] Application logs for targeted endpoints (sampled if huge).
- [ ] Extortion messages with full headers; any payment addresses — never interact with them.
- [ ] Status-page history and every customer message sent.
- [ ] SOC's parallel-intrusion hunt: scope, queries, result.
- [ ] Decision log D1–D7 including spend approvals.

Chain of custody as in [templates/incident-record.md](../templates/incident-record.md). Keep provider-supplied data
labelled by origin.

## 8. Post-incident review

Use [templates/post-incident-review.md](../templates/post-incident-review.md), and additionally:

1. Time from first customer impact to status-page update — target 30 minutes. Why longer?
2. Did the upstream mitigation contract work as expected (onboarding time, capacity, cost)?
3. Which application endpoints were the weak point? Can they be cached, rate-limited or redesigned?
4. Was the "order of sacrifice" pre-agreed, or decided under pressure?
5. Was there any sign the DDoS masked another attack?
6. Update capacity planning, the BIA maximum tolerable downtime, provider contracts and this playbook.
