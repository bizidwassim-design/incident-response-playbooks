# Contributing

Playbooks improve when people who have run real incidents read them. Welcome contributions:

* new incident types (operational technology, large-scale cloud misconfiguration, deepfake / voice-clone fraud,
  certificate or domain hijack);
* notification tables for regimes not covered (sector regulators, other countries) — with a source reference;
* tabletop scenarios and injects;
* corrections and simplifications: shorter is better;
* translations of playbooks or templates.

## Playbooks

1. One file per incident type in `playbooks/`, named in lower-case kebab-case.
2. Keep the exact structure — `scripts/check_playbooks.py` enforces it:
   title `# Playbook — <name>`, the metadata table (use when, default severity, incident manager, related SOC
   playbooks, templates), then sections 1–8 with the headings used in the existing playbooks, the four
   communication templates in section 6, S1–S4 in the severity table, at least five decisions and five evidence items.
3. Decisions must have an **owner** and a **default** — what happens if nobody decides.
4. Communication templates are fictional, written for *Northwind Logistics*, and marked as such.
5. Technical steps belong in [soc-detection-playbooks](https://github.com/bizidwassim-design/soc-detection-playbooks);
   link to them rather than repeating them.
6. Reference standards and laws by name and clause only; never paste their text.
7. Add the playbook to the README table and to the "Choosing the playbook" table in
   `docs/incident-management-process.md`.
8. Run `python scripts/check_playbooks.py` — it must print zero problems.

## Templates and docs

Keep CSV templates with LF line endings and the header documented in the checker. Keep example rows fictional
(`INC-2026-042`, `Northwind Logistics`, `Contoso`, `Fabrikam`).

## Ground rules

* No real incidents, people, organisations, hostnames, addresses or indicators.
* Respect the [Code of Conduct](CODE_OF_CONDUCT.md).
* By contributing you agree your work is released under the [MIT License](LICENSE).
