#!/usr/bin/env python3
"""Validate the structure of every incident-response playbook and template.

Checks (all must pass, CI fails otherwise):

* each ``playbooks/*.md`` has the title form ``# Playbook — <name>``;
* the metadata table carries the five required rows;
* the eight numbered sections are present, in order, with the exact headings;
* section 6 contains the four communication templates and is marked fictional;
* section 2 has a severity table covering S1–S4, section 4 at least five decisions,
  section 7 at least five checklist items;
* every relative Markdown link resolves to a file in the repository;
* no forbidden strings (real-looking secrets, placeholder leaks);
* CSV templates parse and carry the expected header;
* README.md links every playbook.

Run from anywhere: ``python scripts/check_playbooks.py``.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAYBOOK_DIR = ROOT / "playbooks"
TEMPLATE_DIR = ROOT / "templates"

TITLE_RE = re.compile(r"^# Playbook — \S.*$")

METADATA_ROWS = (
    "**Use when**",
    "**Default severity**",
    "**Incident manager**",
    "**Related SOC playbooks**",
    "**Templates**",
)

SECTIONS = (
    "## 1. Scope and triggers",
    "## 2. Severity matrix",
    "## 3. Roles",
    "## 4. Decision points",
    "## 5. Timeline template",
    "## 6. Communication templates",
    "## 7. Evidence and chain of custody",
    "## 8. Post-incident review",
)

COMMS_SUBSECTIONS = (
    "### Internal",
    "### Customers",
    "### Regulator",
    "### Press holding statement",
)

SEVERITY_LEVELS = ("S1", "S2", "S3", "S4")

FORBIDDEN = (
    "AKIA",  # AWS access key prefix
    "BEGIN PRIVATE KEY",
    "password=",
    "TODO",
    "lorem ipsum",
)

CSV_HEADERS: dict[str, list[str]] = {
    "timeline.csv": [
        "incident_id",
        "timestamp_utc",
        "phase",
        "event_type",
        "description",
        "actor",
        "source_or_evidence",
        "decision_ref",
        "clock_ref",
    ],
    "communication-log.csv": [
        "incident_id",
        "timestamp_utc",
        "audience",
        "channel",
        "subject_or_summary",
        "sender",
        "approved_by",
        "template_used",
        "status",
        "reference",
    ],
    "roles-raci.csv": [
        "activity",
        "phase",
        "incident_manager",
        "legal",
        "comms",
        "hr",
        "it_soc",
        "dpo",
        "business_owner",
        "executive_sponsor",
    ],
}

RACI_VALUES = {"", "R", "A", "C", "I", "R/A"}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def split_sections(text: str) -> dict[str, str]:
    """Return a mapping of H2 heading -> body text (until the next H2)."""
    sections: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buffer)
            current = line.rstrip()
            buffer = []
        elif current is not None:
            buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer)
    return sections


def check_links(path: Path, text: str) -> list[str]:
    problems: list[str] = []
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        file_part = target.split("#", 1)[0]
        if not file_part:
            continue  # same-page anchor
        resolved = (path.parent / file_part).resolve()
        if not resolved.exists():
            problems.append(f"broken link: {target}")
    return problems


def check_playbook(path: Path) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or not TITLE_RE.match(lines[0]):
        problems.append("first line must be '# Playbook — <name>'")

    for row in METADATA_ROWS:
        if f"| {row} |" not in text:
            problems.append(f"metadata table missing row {row}")

    headings = [line.rstrip() for line in lines if line.startswith("## ")]
    if headings != list(SECTIONS):
        missing = [s for s in SECTIONS if s not in headings]
        extra = [h for h in headings if h not in SECTIONS]
        if missing:
            problems.append(f"missing sections: {missing}")
        if extra:
            problems.append(f"unexpected H2 headings: {extra}")
        if not missing and not extra:
            problems.append("sections are out of order")

    sections = split_sections(text)

    severity = sections.get(SECTIONS[1], "")
    table_lines = [line for line in severity.splitlines() if line.startswith("|")]
    if len(table_lines) < 4:
        problems.append("section 2 must contain a severity table")
    for level in SEVERITY_LEVELS:
        if not any(level in line for line in table_lines):
            problems.append(f"severity table does not mention {level}")

    decisions = sections.get(SECTIONS[3], "")
    decision_rows = re.findall(r"^\| D\d+ \|", decisions, flags=re.MULTILINE)
    if len(decision_rows) < 5:
        problems.append(f"section 4 needs at least 5 decisions (found {len(decision_rows)})")

    timeline = sections.get(SECTIONS[4], "")
    if "| **T0" not in timeline:
        problems.append("section 5 timeline must start at T0")

    comms = sections.get(SECTIONS[5], "")
    for sub in COMMS_SUBSECTIONS:
        if not re.search(rf"^{re.escape(sub)}\s*$", comms, flags=re.MULTILINE):
            problems.append(f"section 6 missing template {sub!r}")
    if "fictional" not in comms.lower():
        problems.append("section 6 must state that the templates are fictional")

    evidence = sections.get(SECTIONS[6], "")
    items = re.findall(r"^- \[ \] ", evidence, flags=re.MULTILINE)
    if len(items) < 5:
        problems.append(f"section 7 needs at least 5 checklist items (found {len(items)})")
    if "custody" not in evidence.lower():
        problems.append("section 7 must describe chain of custody")

    review = sections.get(SECTIONS[7], "")
    if "post-incident-review.md" not in review:
        problems.append("section 8 must link the post-incident review template")

    for term in FORBIDDEN:
        if term.lower() in text.lower():
            problems.append(f"forbidden string present: {term!r}")

    for line_no, line in enumerate(lines, start=1):
        if line != line.rstrip():
            problems.append(f"trailing whitespace on line {line_no}")

    problems.extend(check_links(path, text))
    return problems


def check_csv(path: Path, expected_header: list[str]) -> list[str]:
    problems: list[str] = []
    raw = path.read_bytes()
    if b"\r\n" in raw:
        problems.append("must use LF line endings")
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return ["empty file"]
    if rows[0] != expected_header:
        problems.append(f"header mismatch: {rows[0]} != {expected_header}")
    if len(rows) < 2:
        problems.append("needs at least one example row")
    for index, row in enumerate(rows[1:], start=2):
        if len(row) != len(expected_header):
            problems.append(f"row {index} has {len(row)} columns, expected {len(expected_header)}")
    if path.name == "roles-raci.csv":
        for index, row in enumerate(rows[1:], start=2):
            cells = row[2:]
            bad = [cell for cell in cells if cell not in RACI_VALUES]
            if bad:
                problems.append(f"row {index} has invalid RACI values {bad}")
            if not any("A" in cell for cell in cells):
                problems.append(f"row {index} has no accountable (A) role")
    return problems


def check_readme(playbooks: list[Path]) -> list[str]:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    return [
        f"README.md does not link playbooks/{p.name}" for p in playbooks if f"playbooks/{p.name}" not in readme
    ]


def main() -> int:
    playbooks = sorted(PLAYBOOK_DIR.glob("*.md"))
    if not playbooks:
        print("no playbooks found", file=sys.stderr)
        return 1

    failures = 0
    for path in playbooks:
        problems = check_playbook(path)
        status = "OK " if not problems else "ERR"
        print(f"[{status}] {path.relative_to(ROOT).as_posix()}")
        for problem in problems:
            print(f"      - {problem}")
        failures += len(problems)

    for name, header in CSV_HEADERS.items():
        path = TEMPLATE_DIR / name
        problems = check_csv(path, header) if path.exists() else ["file missing"]
        status = "OK " if not problems else "ERR"
        print(f"[{status}] {path.relative_to(ROOT).as_posix()}")
        for problem in problems:
            print(f"      - {problem}")
        failures += len(problems)

    for name in ("incident-record.md", "post-incident-review.md", "severity-matrix.md"):
        path = TEMPLATE_DIR / name
        problems = [] if path.exists() else ["file missing"]
        if path.exists():
            problems.extend(check_links(path, path.read_text(encoding="utf-8")))
        status = "OK " if not problems else "ERR"
        print(f"[{status}] {path.relative_to(ROOT).as_posix()}")
        for problem in problems:
            print(f"      - {problem}")
        failures += len(problems)

    for doc in sorted((ROOT / "docs").glob("*.md")):
        problems = check_links(doc, doc.read_text(encoding="utf-8"))
        status = "OK " if not problems else "ERR"
        print(f"[{status}] {doc.relative_to(ROOT).as_posix()}")
        for problem in problems:
            print(f"      - {problem}")
        failures += len(problems)

    readme_problems = check_readme(playbooks)
    for problem in readme_problems:
        print(f"[ERR] {problem}")
    failures += len(readme_problems)

    print(f"\n{len(playbooks)} playbooks checked, {failures} problem(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
