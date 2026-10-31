# Severity matrix — generic

> Every playbook carries its own matrix tuned to the incident type. This is the common scale behind them: use it
> when an incident does not fit a playbook, and to keep severities comparable across incidents and years.
> **Take the highest factor**, record who set the severity and when, and re-assess at every bridge call.

## Levels

| Level | Name | Meaning | Response posture |
|---|---|---|---|
| **S1** | Critical | Threat to safety, legal position, regulated data at scale, core operations or the organisation's ability to respond (identity, backups, EDR). | Crisis bridge now; executive sponsor and Legal in the room; external IR on standby; hourly updates; 24/7 staffing. |
| **S2** | High | Confirmed compromise or data exposure with customer, regulatory or significant financial impact, contained to part of the organisation. | Bridge within 1 h; Legal and Comms engaged; updates every 2–4 h; extended hours. |
| **S3** | Medium | Suspected or limited incident; impact confined to one team, system or a small data set; no regulatory clock confirmed. | Incident manager assigned; business hours; daily update. |
| **S4** | Low | Policy breach, near miss or single-host event with no data or operational impact. | Ticket-based; logged for trend analysis; reviewed quarterly. |

## Factors

| Factor | S4 Low | S3 Medium | S2 High | S1 Critical |
|---|---|---|---|---|
| **Data** | None, or public / internal non-sensitive | Confidential business data | Personal data; source code; contracts; pricing | Special-category personal data, credentials at scale, secrets, regulated data; cross-border |
| **Scale** | 1 user / host | One team or system | One site, business unit or platform | Enterprise-wide or control plane (identity, backup, EDR, network) |
| **Operations** | None | Slower work; workaround exists | Service degraded; customer-visible; SLA at risk | Operations stopped; safety impact; no workaround |
| **Regulatory / contractual** | None | Possible, low risk | One regime or contract with a clock | Multiple regimes; cross-border; sector regulator; contractual penalties |
| **Attacker** | Opportunistic, blocked | Commodity malware, contained | Hands-on-keyboard; persistence; privileged access | Control plane compromised; destructive intent; extortion |
| **Visibility** | Internal | Partners / a few customers | Many customers; social media | Press; regulator; legal claims |
| **Recoverability** | Trivial | Hours; in-house | Days; external help | Weeks; backups in doubt |

## Rules

1. Severity is set by the **incident manager** and recorded in the incident record with the time and the factor that drove it.
2. Over-call early, downgrade with evidence. Downgrades need a one-line justification.
3. Any running regulatory clock means **at least S2**.
4. Any incident touching identity, backups or EDR consoles is **S1** until proven otherwise.
5. Repeat incidents of the same type within 90 days go one level up.
