# Playbook — AI System Incident

| | |
|---|---|
| **Use when** | An AI system you operate or embed (chatbot, copilot, document-processing model, decision-support or scoring model, agent with tool access) causes or is suspected of causing harm: prompt injection, data leakage through outputs, harmful or defamatory output, unsafe autonomous actions, or model drift producing wrong decisions. |
| **Default severity** | **S3 (Medium)**; **S2 (High)** when personal data left the system, an agent executed an unintended action, or the output reached customers or the public; **S1 (Critical)** for decisions affecting safety, legal rights, credit or employment, or an agent acting on production systems. |
| **Incident manager** | Head of Security; AI system owner and AI governance lead co-lead. |
| **Related SOC playbooks** | [data-exfiltration](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/data-exfiltration.md) (data leaving via model outputs or tool calls) · [cloud-account-compromise](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/cloud-account-compromise.md) (abused API keys / agent identities) |
| **Templates** | [incident-record](../templates/incident-record.md) · [timeline](../templates/timeline.csv) · [communication-log](../templates/communication-log.csv) · [post-incident-review](../templates/post-incident-review.md) |

> AI incidents mix classic security (a key was abused), privacy (data in a prompt log), safety (a wrong answer at
> scale) and reputation (a screenshot on social media). The response is the same discipline: contain the system,
> preserve the prompts and outputs, work out who was affected, and decide who to tell. The novelty is that
> "turn it off" may be the safest and cheapest first move — the system is rarely life-critical, but its mistakes scale.

## 1. Scope and triggers

| Variant | What it looks like | Typical trigger |
|---|---|---|
| **A. Prompt injection / jailbreak** | Instructions hidden in a document, web page, email or ticket make the model ignore its rules, reveal its system prompt, exfiltrate context, or call tools it should not. | Red-team finding, user report, tool-call anomaly, outbound request from the agent to an unknown host |
| **B. Data leakage through outputs** | The model reveals another customer's data, internal documents, secrets from the retrieval index, or personal data from training/fine-tuning. | User screenshot, DLP on model output, review of conversation logs |
| **C. Harmful or unlawful output** | Defamatory, discriminatory, dangerous or legally problematic text or images delivered to a user or published. | Complaint, press, social media, content-moderation alert |
| **D. Unsafe autonomous action** | An agent with tool access deletes, sends, pays, changes configuration, or loops at cost. | Cloud bill alert, change-management anomaly, user complaint |
| **E. Model drift / wrong decisions** | A scoring or classification model silently degrades (data drift, upstream change) and produces systematically wrong outcomes. | Monitoring drift alarm, business KPI anomaly, appeal pattern |
| **F. Supply chain** | Compromised model weights, poisoned dataset, malicious plugin/tool, vendor model incident. | Vendor notice — combine with [supply-chain-vendor-compromise](supply-chain-vendor-compromise.md) |

## 2. Severity matrix

| Factor | S4 Low | S3 Medium | S2 High | S1 Critical |
|---|---|---|---|---|
| Who was affected | Internal testers | Internal users | Customers / public | Individuals' rights, safety, credit, employment, health |
| Data involved | None | Internal, non-sensitive | Personal data or confidential business data | Special-category data, secrets, cross-tenant leakage |
| Actions taken by the system | None (text only) | Reversible internal action | Irreversible or external action (email sent, payment, deletion) | Action on production or safety-related systems |
| Scale | Single conversation | < 100 interactions | Hundreds to thousands | Systematic — all users / all decisions over a period |
| Visibility | Internal | Customer complaint | Social media / press | Regulator or legal claim |

## 3. Roles

| Role | Responsibilities in this playbook |
|---|---|
| **Incident manager** | Timeline, severity, decision owner, bridge. |
| **AI system owner** | Knows the architecture (model, prompts, retrieval sources, tools, guardrails), can disable or roll back, owns the fix. |
| **AI governance lead / Risk** | Impact on individuals, fairness and rights assessment, AI management system records (ISO/IEC 42001-style register), regulator view. |
| **Security / SOC** | Abused credentials, tool-call forensics, data-flow analysis, hunting for injection payloads in the sources. |
| **DPO / Legal** | Personal data in prompts, logs and outputs; defamation or liability for outputs; notification duties; vendor contracts. |
| **Comms** | Public response to screenshots and press; customer notices; tone. |
| **HR** | If outputs affected employees (recruiting, performance) or an employee misused the system. |
| **Executive sponsor** | Switch-off decision for revenue-critical systems; external statements; decision review for variant E. |

## 4. Decision points

| # | Decision | Owner | Guidance |
|---|---|---|---|
| D1 | Disable the system, degrade it (remove tools / retrieval / external access), or keep running with monitoring? | AI OWNER + IM (+ EXEC if customer-facing revenue) | Disable immediately for variants D and S1 cases. Degrade (text-only, no tools, no retrieval) for A/B while investigating. |
| D2 | Revoke the system's credentials and tool permissions? | SECURITY | Yes for A, D, F: API keys, service identities, tool tokens, connectors. Re-issue with least privilege. |
| D3 | Which conversations / decisions are affected? | AI OWNER + SOC | Search logs for the payload, the leaked content, or the drift period. Preserve the full prompt/output records first. |
| D4 | Were individuals affected in a way that requires notification or remedy? | GOVERNANCE + DPO + LEGAL | Personal data leaked → [data-breach-personal-data](data-breach-personal-data.md). Wrong decisions → remediate (re-run, human review, reversal) and inform. |
| D5 | Roll back model / prompt / retrieval index to a known-good version? | AI OWNER | Yes when the cause is a change; keep the bad version for evidence. |
| D6 | Public response to a viral output? | COMMS + EXEC | Acknowledge quickly, do not blame the user, say what you changed. |
| D7 | Re-enable criteria | IM + GOVERNANCE | Root cause fixed, guardrail test suite passes including the incident case, monitoring in place, sign-off recorded in the AI register. |

## 5. Timeline template

| Phase | Target | Actions | Owner |
|---|---|---|---|
| **T0 — Detection** | 0 | Open the incident record; classify the variant. Preserve prompt, context, retrieved documents, tool calls and outputs for the triggering interaction(s). | IM, AI OWNER |
| **T+30 min** | 30 min | Decision D1 (disable / degrade). D2 if credentials or tools are implicated. Bridge opened. | AI OWNER, SECURITY |
| **T+4 h** | 4 h | Scope (D3): which interactions, users, decisions, time window. Identify the injection source or leak path or drift start. Legal and DPO briefed if personal data or harmful content is involved. | SOC, AI OWNER |
| **T+24 h** | 24 h | Root cause confirmed. Decision D5 roll-back. Affected users / decisions list produced. D4 assessment. Customer notice drafted if needed. | AI OWNER, GOVERNANCE |
| **T+72 h** | 72 h | Fix implemented and tested against the incident case plus the regression suite. Personal-data clocks met. Remedy for wrong decisions started (human review queue). | AI OWNER, DPO |
| **T+7 d** | 7 d | D7 re-enable with sign-off. Monitoring (drift, injection patterns, tool-call anomalies) in place. AI register updated. | IM, GOVERNANCE |
| **T+30 d** | 30 d | Post-incident review including the AI risk assessment and the guardrail design. | IM |

## 6. Communication templates

All templates are **fictional** examples for *Northwind Logistics* and its fictional assistant "NorthBot".

### Internal

> **Subject:** NorthBot temporarily limited — security review
>
> We have temporarily [disabled / limited] NorthBot after identifying [an issue with how it handled certain
> inputs]. Until further notice, do not paste customer data or confidential documents into any AI tool, and treat
> any unusual NorthBot output from [date range] as unreliable — check it against the source system. If you noticed
> odd behaviour, please tell [contact] with the conversation link. We expect to restore service by [date].

### Customers

> **Subject:** An update about our AI assistant
>
> Between [dates], our AI assistant may have [provided incorrect information about / displayed information that
> was not intended for you]. We have paused the assistant, corrected the issue and reviewed the affected
> conversations. [If your information was shown to another user, we are contacting you separately.] [If a decision
> about your account was affected, it has been reviewed by a member of our team and (outcome).] We are sorry for
> any confusion. Contact: [address].

### Regulator

Where personal data is involved follow [data-breach-personal-data](data-breach-personal-data.md). AI-specific facts
to prepare: purpose and type of the system, whether it makes or supports decisions about individuals, the human
oversight in place, the data sources and whether personal data was in prompts, logs or retrieval; the nature of the
failure (injection, leakage, harmful output, drift); the number of interactions or decisions affected; remedies
offered; and the records from your AI management system (risk assessment, impact assessment, monitoring).

### Press holding statement

> Northwind Logistics has temporarily paused its AI assistant after identifying that, in a small number of
> interactions, it [produced incorrect responses / displayed content that did not meet our standards]. We have
> fixed the underlying issue, reviewed the affected interactions and are contacting anyone affected directly. The
> assistant will be restored once our additional safeguards are verified. Media contact: [name, address].

## 7. Evidence and chain of custody

- [ ] Full interaction records for the affected window: system prompt version, user input, retrieved documents,
      tool calls and results, model output, model and parameter versions — exported read-only and hashed.
- [ ] The injection payload or source document (variant A) preserved as a file with hash and origin.
- [ ] Credential and tool-permission inventory for the system's identity; revocation / re-issue log.
- [ ] Guardrail and content-filter logs; monitoring and drift metrics for the window (variant E).
- [ ] Change history: prompt, model, index, tool and configuration changes before the incident.
- [ ] The affected-users / affected-decisions list with the method used to produce it.
- [ ] Vendor correspondence and model/provider incident notices (variant F).
- [ ] Decision log D1–D7 and the re-enable sign-off.

Chain of custody as in [templates/incident-record.md](../templates/incident-record.md). Conversation logs contain
personal data: restrict access, set retention, and record every person who viewed them.

## 8. Post-incident review

Use [templates/post-incident-review.md](../templates/post-incident-review.md), and additionally:

1. Was this failure mode in the AI risk assessment? If not, why was it missed; if yes, why did the control not hold?
2. Did the system have more data, tools or permissions than its purpose required?
3. Was there a human in the loop where the impact was on individuals? Was the override used?
4. How was the incident detected — monitoring, or a user screenshot? What monitoring would have caught it earlier?
5. Is there a regression test for this case now? Is red-teaming scheduled?
6. Update the AI register, the system card, the acceptable-use rules, vendor terms and this playbook.
