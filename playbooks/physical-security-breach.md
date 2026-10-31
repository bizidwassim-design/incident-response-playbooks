# Playbook — Physical Security Breach

| | |
|---|---|
| **Use when** | Someone gained, or attempted to gain, unauthorised physical access to premises, server rooms, network cabinets, archives or vehicles; equipment was tampered with or stolen on site; a rogue device (keylogger, network implant, rogue access point) was found; or a tailgating / social-engineering entry was reported. |
| **Default severity** | **S3 (Medium)**; **S2 (High)** for access to a server room, network cabinet or archive; **S1 (Critical)** for tampering with infrastructure, a rogue device on the network, or theft of systems holding regulated data. |
| **Incident manager** | Head of Security; Facilities / Physical Security manager co-leads. |
| **Related SOC playbooks** | [lateral-movement](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/lateral-movement.md) (rogue device on the network) · [credential-access](https://github.com/bizidwassim-design/soc-detection-playbooks/blob/main/playbooks/credential-access.md) (keylogger, console access) |
| **Templates** | [incident-record](../templates/incident-record.md) · [timeline](../templates/timeline.csv) · [communication-log](../templates/communication-log.csv) · [post-incident-review](../templates/post-incident-review.md) |

> Physical and cyber incidents share a response: find out what the person could reach, assume they reached it, and
> preserve evidence that is **perishable** (CCTV overwrites in days, visitor logs get tidied, badge logs roll).
> People's safety comes first — nothing in this playbook overrides the building's emergency procedures.

## 1. Scope and triggers

- Badge system: door forced, door held open, access denied repeatedly, badge used at two sites at once, badge used
  outside the holder's hours or after their departure.
- Guard, receptionist or staff report of an unknown person, tailgating, or someone "from IT" nobody recognised.
- Found device: unknown USB device on a workstation, unknown box in a network cabinet, unknown access point.
- Server room, archive or cabinet found unlocked, seals broken, equipment moved or missing.
- Break-in reported by police or alarm company.
- Contractor or cleaner access anomalies.

**Not in scope**: workplace violence, protests, fire or medical emergencies — follow the building emergency plan,
then open this playbook afterwards if security equipment or data was involved.

## 2. Severity matrix

| Factor | S4 Low | S3 Medium | S2 High | S1 Critical |
|---|---|---|---|---|
| Area reached | Public / reception | General office | Server room, network cabinet, archive, executive floor | Data centre hall, OT control room, backup vault |
| What happened | Attempt, no entry | Entry, no evidence of interaction | Equipment handled, documents accessed, device left | Device planted on network, systems removed, tampering with infrastructure |
| Duration unaccounted | Minutes, observed | < 1 h | Hours | Days / unknown — logs missing |
| Perpetrator | Known staff, policy breach | Unknown, opportunistic | Social engineering, prepared | Targeted, organised |
| Evidence | Complete CCTV + logs | Partial | Gaps | None / tampered |

## 3. Roles

| Role | Responsibilities in this playbook |
|---|---|
| **Incident manager** | Timeline, severity, decisions, linking the physical and cyber threads. |
| **Facilities / Physical security** | Badge and CCTV evidence, locks and codes, guards, alarm company, police liaison on site. |
| **IT / Network** | Identify what the area contained; sweep for rogue devices; check switch ports, MAC tables, wireless; isolate. |
| **SOC** | Hunt for activity from the rogue device or console access; integrity of systems in the area. |
| **HR** | If staff or contractors are involved; contractor agency liaison. |
| **Legal** | Police report, trespass, insurance, data-protection consequences. |
| **Site manager** | Operational impact, local communications. |
| **Comms** | Only if visible externally (break-in, press). |

## 4. Decision points

| # | Decision | Owner | Guidance |
|---|---|---|---|
| D1 | Is anyone at risk now? | SITE MANAGER | If yes: building emergency plan and police; everything else waits. |
| D2 | Treat the area's systems as compromised? | IM + IT | Yes if a server room, cabinet or unattended workstation was reachable for an unaccounted period. Sweep before trusting. |
| D3 | Isolate network ports / segments in the area? | IT | Yes when a rogue device is found or suspected; disable unused ports permanently. |
| D4 | Rotate credentials and keys? | IT + FACILITIES | Door codes, cabinet keys, local admin passwords on reachable consoles, any credential written on a whiteboard or sticky note the person could see. |
| D5 | Police report and prosecution? | LEGAL + EXEC | Always for break-in or planted device; recommended for social-engineering entry. |
| D6 | Data-protection assessment? | DPO | If documents, archives or systems holding personal data were reachable — [data-breach-personal-data](data-breach-personal-data.md). |
| D7 | Contractor / cleaning / guard provider consequences? | HR + PROCUREMENT | After facts are established; contract review. |

## 5. Timeline template

| Phase | Target | Actions | Owner |
|---|---|---|---|
| **T0 — Report** | 0 | Decision D1. Open incident record. Secure the area (do not touch found devices; photograph in place). Guard posted if needed. | SITE MANAGER, FACILITIES |
| **T+1 h** | 1 h | **Preserve perishable evidence**: export CCTV for the window ±2 h on every camera on the route, badge logs for the doors, visitor book, alarm logs. Identify the person if possible. | FACILITIES |
| **T+2 h** | 2 h | Inventory what was in the area and what the person could reach. Decision D2 and D3. Found device bagged, labelled, photographed; port disconnected and switch logs captured. | IT, SOC |
| **T+8 h** | 8 h | Rogue-device sweep of the area (visual, port audit, wireless scan). Console / workstation checks for new USB devices, logons, hardware changes. Decision D4. Police report (D5). | IT, FACILITIES, LEGAL |
| **T+24 h** | 24 h | SOC hunt for activity from the device or the area's systems during the window. Decision D6. Staff reminder sent. | SOC, DPO, COMMS |
| **T+72 h** | 72 h | Physical fixes: locks, door closers, badge rules, camera coverage. Contractor review (D7). | FACILITIES, HR |
| **T+30 d** | 30 d | Post-incident review with Facilities and IT together. | IM |

## 6. Communication templates

All templates are **fictional** examples for *Northwind Logistics*.

### Internal

> **Subject:** Security reminder — access to [site]
>
> On [date] an unauthorised person gained access to [area] at [site]. No one was harmed and the matter is being
> handled with the police. Please: wear your badge visibly, do not hold doors for people you do not know, direct
> visitors to reception, and challenge or report anyone without a badge in restricted areas — call [number]. If you
> notice unfamiliar equipment plugged into your workstation or a network socket, do not remove it; report it.

### Customers

Rarely needed. If customer equipment, documents or data were in the area, use the customer template in
[data-breach-personal-data](data-breach-personal-data.md), stating what was physically reachable and whether there
is evidence of access.

### Regulator

If personal data in paper or on systems in the area may have been accessed, follow the regulator section of
[data-breach-personal-data](data-breach-personal-data.md). Physical specifics to prepare: area and its protections
(locks, badges, cameras), the unaccounted window, what was stored there and how (locked cabinets, encrypted disks),
the evidence of access or absence of it, and the physical remediation.

### Press holding statement

> Northwind Logistics reported an unauthorised entry at its [site] premises on [date] to the police. No one was
> hurt. We are reviewing the incident with the authorities and have taken additional security measures. We have no
> evidence that customer information was affected. Media contact: [name, address].

## 7. Evidence and chain of custody

- [ ] CCTV exports (native format, with the system's time offset recorded) for every relevant camera, ±2 h around the window.
- [ ] Badge, alarm and visitor logs for the doors and period, exported and hashed.
- [ ] Photographs of the scene before anything is moved; found devices bagged, labelled, sealed, with collector and time.
- [ ] Switch port logs, MAC tables, DHCP leases, wireless controller logs for the area during the window.
- [ ] Inventory of the area with serial numbers; list of items missing or moved.
- [ ] Workstation / console checks (USB history, logon events, hardware change events).
- [ ] Police report reference; statements from witnesses (name, time, what they saw).
- [ ] Decision log D1–D7.

Chain of custody as in [templates/incident-record.md](../templates/incident-record.md). Physical items follow the
same rules as digital ones: one custodian, sealed, logged at every hand-over, including to the police.

## 8. Post-incident review

Use [templates/post-incident-review.md](../templates/post-incident-review.md), and additionally:

1. How did the person get in — tailgating, social engineering, unlocked door, stolen badge, contractor access?
2. Did the physical controls work (badges, cameras, locks, guards)? Were logs available for the full window?
3. Did staff challenge or report? Did they know how?
4. What could be reached in the area that should not have been reachable without a second control (locked cabinets, disabled ports, screen locks)?
5. Were physical and cyber teams working from one timeline? Where did information get lost between them?
6. Update access rules, contractor vetting, camera retention, port security, visitor process and this playbook.
