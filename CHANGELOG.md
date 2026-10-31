# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [1.0.0] — 2026-10-31

### Added
- Ten crisis-level playbooks: data breach (personal data) with GDPR / Loi 25 / PIPEDA clocks, insider threat,
  supply-chain and vendor compromise, DDoS, lost or stolen device, web application compromise, AI system incident,
  privileged account compromise, malware outbreak, physical security breach.
- Templates: incident record, timeline CSV, communication log CSV, post-incident review, generic severity matrix,
  roles RACI CSV.
- `docs/incident-management-process.md` (NIST SP 800-61 phases, two-level model with the SOC playbooks) and
  `docs/tabletop-exercise-kit.md` (three scripted scenarios with timed injects and an inject bank).
- `scripts/check_playbooks.py` structure validator, run in CI together with a syntax check of the script.
- Governance files: license, code of conduct, security policy, contributing guide, Dependabot, CI workflow.
