# Incident Response Playbooks Pack

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![CI](https://github.com/bizidwassim-design/incident-response-playbooks/actions/workflows/ci.yml/badge.svg)](https://github.com/bizidwassim-design/incident-response-playbooks/actions/workflows/ci.yml) [![Fictional data](https://img.shields.io/badge/sample%20data-fictional-informational)](SECURITY.md)

Ten **incident-manager-level** playbooks for the incidents that put an organisation in front of a regulator, a
customer or a journalist — with the severity matrix, roles, decision points, timeline, communication templates,
chain-of-custody checklist and post-incident review each one needs. Built to sit on top of the analyst-level
[SOC Detection Rules & Playbooks](https://github.com/bizidwassim-design/soc-detection-playbooks): the SOC stops
the attacker; this pack runs the crisis around it.

> 🇫🇷 Résumé en français en bas de page.

## Layout

```
playbooks/     10 crisis-level playbooks, one incident type each, identical structure
templates/     incident-record.md · timeline.csv · communication-log.csv
               post-incident-review.md · severity-matrix.md · roles-raci.csv
docs/          incident-management-process.md — how the two levels fit together (NIST SP 800-61 phases)
               tabletop-exercise-kit.md — 3 scripted scenarios with timed injects, plus an inject bank
               tips-and-tricks.md — field notes: automated isolation, tuning, release procedure, lightweight SOAR, phishing hygiene
detections/    defender-tamper-custom-detection.kql — Defender XDR custom detection for T1562.001 (two-rule pattern)
scripts/       check_playbooks.py — structure validation, run by CI
```

## Quick start

1. Read [docs/incident-management-process.md](docs/incident-management-process.md) (10 minutes).
2. Copy `templates/` to the place your crisis team can reach **when the corporate tenant is compromised**
   (a separate tenant, an offline folder, printed copies). Fill in the role names and out-of-band numbers.
3. Replace the legal regimes in [data-breach-personal-data.md](playbooks/data-breach-personal-data.md) with the ones
   that apply to you, and have counsel confirm the clocks.
4. Run a tabletop from [docs/tabletop-exercise-kit.md](docs/tabletop-exercise-kit.md) with Legal, Comms, HR and an
   executive. Fix what the exercise breaks.
5. Validate your edits: `python scripts/check_playbooks.py`.
6. Read [docs/tips-and-tricks.md](docs/tips-and-tricks.md) before arming any automatic response.

## What's inside

| Playbook | Use when | Crisis-specific content |
|---|---|---|
| [data-breach-personal-data](playbooks/data-breach-personal-data.md) | Personal data accessed, disclosed or lost | Awareness definition; GDPR / Loi 25 / PIPEDA notification clocks; phased regulator notification; what to tell individuals |
| [insider-threat](playbooks/insider-threat.md) | Employee or contractor misusing access | Lawful-basis gate, need-to-know circle, covert-vs-overt decision, HR-led interview, court-grade evidence |
| [supply-chain-vendor-compromise](playbooks/supply-chain-vendor-compromise.md) | MSP, SaaS, dependency or build pipeline compromised | Three variants (access / data / component), disconnect decision, questions to put to the vendor, contract levers |
| [ddos](playbooks/ddos.md) | Service unavailable due to attack traffic | Scrubbing engagement, order of sacrifice, extortion handling, smokescreen checks, status-page cadence |
| [lost-or-stolen-device](playbooks/lost-or-stolen-device.md) | Laptop, phone, token or paper lost | "Can we prove encryption?" test, lock-then-wipe, credential rotation scope, police / insurer |
| [web-application-compromise](playbooks/web-application-compromise.md) | Web shell, skimmer, injection, CMS admin abuse | Offline-vs-observe decision, snapshot-before-fix, secret rotation list, card-data obligations |
| [ai-system-incident](playbooks/ai-system-incident.md) | Prompt injection, data leakage, harmful output, unsafe agent action, model drift | Six variants, degrade-vs-disable, affected-decisions list, re-enable criteria, AI register updates |
| [privileged-account-compromise](playbooks/privileged-account-compromise.md) | Admin / cloud / identity account under attacker control | Out-of-band channel, trusted circle, tier model, break-glass and rotation, "evicted" criteria |
| [malware-outbreak](playbooks/malware-outbreak.md) | Malware on many hosts or spreading | Isolation level decision, spread-vector block, reimage logistics, recovery order, contained / recovered criteria |
| [physical-security-breach](playbooks/physical-security-breach.md) | Unauthorised entry, rogue device, on-site theft | Perishable evidence (CCTV, badge logs), rogue-device sweep, joint physical / cyber timeline |

Every playbook has the same eight sections — **scope and triggers · severity matrix · roles · decision points ·
timeline template · communication templates (internal, customers, regulator, press holding statement) · evidence and
chain of custody · post-incident review** — so a tired incident manager at 03:00 always finds things in the same place.

## Design choices

* **Crisis level, not analyst level.** No queries, no indicators, no "check the EDR" — those live in
  [soc-detection-playbooks](https://github.com/bizidwassim-design/soc-detection-playbooks) and are linked from the
  metadata table of each playbook. Here you get decisions, owners, clocks and words.
* **Decisions have defaults.** Every decision table says what happens if nobody decides by the deadline ("assume
  personal data in scope", "notify the regulator"). Under pressure, the default is the plan.
* **Awareness is defined.** Regulatory clocks start at a timestamp someone must write down; the playbooks tell you
  what that moment is and how to evidence it.
* **Templates are fictional and marked as such.** All messages are written for *Northwind Logistics* and its
  fictional suppliers *Contoso* and *Fabrikam*. Legal approves every external message before it goes out.
* **Validated structure.** `scripts/check_playbooks.py` enforces the eight sections, the four communication
  templates, the severity scale, the decision and evidence minimums, link integrity and CSV headers. A playbook that
  drifts from the structure fails CI.
* **Standards by name only.** NIST SP 800-61 phases are referenced, not reproduced. Nothing here is legal advice.

## How it relates to the sibling repositories

| Repository | Relationship |
|---|---|
| [soc-detection-playbooks](https://github.com/bizidwassim-design/soc-detection-playbooks) | The analyst layer: Sigma rules and technical playbooks (phishing/BEC, ransomware, credential access, cloud account compromise, lateral movement, data exfiltration). This pack links to them and does not duplicate them. |
| [grc-control-crosswalk](https://github.com/bizidwassim-design/grc-control-crosswalk) | Map the "incident management" controls these playbooks evidence across ISO 27001, NIST CSF and CIS. |
| [iso27001-iso42001-toolkit](https://github.com/bizidwassim-design/iso27001-iso42001-toolkit) | The AI-system playbook feeds the AI management system records (risk register, impact assessment). |
| [ciso-executive-dashboard](https://github.com/bizidwassim-design/ciso-executive-dashboard) | Incident metrics from the post-incident reviews (time to awareness, to containment, to notification). |
| [application-risk-assessment-template](https://github.com/bizidwassim-design/application-risk-assessment-template) | Application risk ratings decide which severity an application compromise starts at. |
| [public-scripts](https://github.com/bizidwassim-design/public-scripts) | Operational scripts for the technical steps the SOC takes during containment. |

## Contributing

New incident types (OT, cloud misconfiguration at scale, deepfake fraud), regime-specific notification tables,
tabletop scenarios and translations are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Run
`python scripts/check_playbooks.py` before opening a pull request.

## Disclaimer

These playbooks are templates for organisations to adapt, not legal or regulatory advice. Notification regimes,
deadlines and thresholds change and vary by jurisdiction and sector; confirm them with qualified counsel. Example
companies, people, systems and incidents are fictional.

## License

[MIT](LICENSE).

---

## 🇫🇷 Résumé

Pack de **10 playbooks de réponse à incident au niveau gestionnaire de crise** (violation de données personnelles
avec les délais RGPD / Loi 25 / LPRPDE, menace interne, compromission de fournisseur, DDoS, appareil perdu ou volé,
compromission d'application web, incident de système d'IA, compromission de compte privilégié, épidémie de logiciel
malveillant, intrusion physique). Chaque playbook suit la même structure : matrice de gravité, rôles, points de
décision avec valeurs par défaut, chronologie, modèles de communication (interne, clients, régulateur, déclaration
de presse — fictifs), preuves et chaîne de conservation, revue post-incident. Fourni avec des modèles (fiche
d'incident, chronologie, journal de communication, RACI), un processus aligné sur les phases du NIST SP 800-61 et
un kit d'exercice sur table avec trois scénarios. Complète les playbooks techniques du dépôt `soc-detection-playbooks`.
Licence MIT ; données fictives uniquement ; ne constitue pas un avis juridique.
