# Data Collection Instruments (Draft)
Cloud Infrastructure Exposure and Data Center Technician Readiness Study

These three instruments operationalize the variables named in the Study Purpose section: the **independent variable** (cloud infrastructure instructional exposure) via Instrument 1, and the **dependent variables** (data center technician readiness and cloud infrastructure technical performance) via Instruments 2 and 3. Scenario language in Instrument 3 is grounded in real, currently posted requirements from GDIT (Fort Liberty-area cloud/systems administration roles) and general local government IT support postings, so the tasks reflect actual entry-level demands rather than generic lab exercises.

---

## Instrument 1: Cloud Infrastructure Exposure Inventory

Self-report checklist of completed coursework and lab activity, mapped directly to the FTCC Cloud Management AAS course sequence. Administered once, near the end of the semester.

| # | Course | Have you completed this course? | Approx. hands-on lab hours | Certification/credential attempted (if any) |
|---|---|---|---|---|
| 1 | CTI-120 Network & Sec Foundation | Yes / No / In Progress | ___ | |
| 2 | CTI-141 Cloud & Storage Concepts | Yes / No / In Progress | ___ | |
| 3 | CTI-240 Virtualization Admin I | Yes / No / In Progress | ___ | |
| 4 | CTI-241 Virtualization Admin II | Yes / No / In Progress | ___ | |
| 5 | CTI-289 CTI Capstone Project | Yes / No / In Progress | ___ | |
| 6 | NOS-110 Operating Systems Concepts | Yes / No / In Progress | ___ | |
| 7 | NOS-120 Linux/UNIX Single User | Yes / No / In Progress | ___ | |
| 8 | NOS-125 Linux/UNIX Scripting | Yes / No / In Progress | ___ | |
| 9 | NOS-220 Linux/UNIX Admin I | Yes / No / In Progress | ___ | |
| 10 | NOS-230 Windows Administration I | Yes / No / In Progress | ___ | |
| 11 | NET-125 Introduction to Networks | Yes / No / In Progress | ___ | |
| 12 | NET-126 Switching and Routing | Yes / No / In Progress | ___ | |
| 13 | CSC-121 Python Programming | Yes / No / In Progress | ___ | |
| 14 | CTS-115 Info Sys Business Concepts | Yes / No / In Progress | ___ | |
| 15 | SEC-110 Security Concepts | Yes / No / In Progress | ___ | |

**Additional items:**
- Total semesters completed in the program: ___
- Certifications held or in progress (CompTIA A+/Network+/Security+/Cloud+, AWS Cloud Practitioner, Microsoft AZ-900, other): free text
- Do you currently hold, or have you ever held, a security clearance? Yes / No / Prefer not to answer *(for descriptive/control-variable purposes only — not used to exclude participants)*

---

## Instrument 2: Data Center Technician Readiness Survey

5-point Likert scale (1 = Not at all prepared/confident, 5 = Extremely prepared/confident). One to two items per skill taxonomy category; item wording draws on language from actual entry-level postings (GDIT skill tags: *Backup and Recovery, Operating Systems, Troubleshooting, Virtual Environments, Computer Networking, Group Problem Solving*; county-level postings: *general IT assistance, timely response to help desk issues*).

| # | Category | Item |
|---|---|---|
| 1 | Virtualization | I am prepared to install, configure, and troubleshoot virtual machines and hypervisors in a datacenter environment. |
| 2 | Virtualization | I am confident managing virtual machine migration, snapshots, and resource allocation. |
| 3 | Networking | I am prepared to configure and troubleshoot routers, switches, and VLANs to resolve connectivity issues. |
| 4 | Cloud Platforms | I am confident performing installation, configuration, and management tasks in a cloud storage or cloud computing environment (e.g., AWS, Azure). |
| 5 | Storage | I am prepared to provision, monitor, and troubleshoot storage systems (SAN/NAS) and perform backup and recovery tasks. |
| 6 | Security/Compliance | I am confident applying access control and secure configuration practices when deploying systems or services. |
| 7 | Security/Compliance | I am prepared to identify and document information security risks in a system I am responsible for. |
| 8 | Scripting/Automation | I am confident writing and troubleshooting shell or Python scripts to automate routine administrative tasks. |
| 9 | Monitoring/Troubleshooting | I am prepared to rapidly troubleshoot Tier-1 support issues and escalate appropriately when a problem exceeds my scope. |
| 10 | Monitoring/Troubleshooting | I am confident using logs and monitoring tools to diagnose the root cause of a system or network problem. |
| 11 | Hardware/Physical Infrastructure | I am prepared to perform basic hardware installation, cabling, and physical troubleshooting tasks in a datacenter or server room. |
| 12 | ITIL/Business & Soft Skills | I am confident writing clear technical documentation and briefing non-technical stakeholders on an issue or its resolution. |
| 13 | Overall | Overall, I feel prepared to perform entry-level data center technician or cloud support tasks in a live work environment. |

---

## Instrument 3: Scenario-Based Performance Tasks

Rubric-scored, hands-on tasks (not self-report). Each task is drawn from real skill requirements in currently posted local roles. Score each on a 0–3 scale across the five dimensions used throughout the Technical Performance Measurement theme: **configuration accuracy, troubleshooting accuracy, task completion, escalation decisions, documentation completeness.**

**Task 1 — VM Deployment & Configuration** *(sourced from GDIT VDI System Administrator postings: "Citrix VDI, Microsoft VDI, Virtual Desktop Infrastructure (VDI), VMware VDI")*
Deploy a virtual machine from a template, configure networking and storage per a provided spec sheet, and document the build.

**Task 2 — Backup and Recovery** *(sourced from GDIT Systems Administrator postings: "Backup and Recovery (Software), Operating Systems (OS)")*
Given a simulated system failure, restore a system or dataset from backup and verify integrity, documenting each step taken.

**Task 3 — Network Troubleshooting** *(sourced from GDIT Network Administrator postings: "Computer Networking, Computer Systems, Group Problem Solving, Network Systems")*
Diagnose and resolve a staged connectivity fault (e.g., misconfigured VLAN or routing issue) within a defined time window.

**Task 4 — Tier-1 Escalation Judgment** *(sourced from GDIT Cloud Service Operations Specialist posting: "able to rapidly troubleshoot Tier-1 support issues")*
Given a helpdesk ticket describing a user-reported issue, determine whether it is resolvable at Tier-1 or requires escalation, and draft the escalation note if applicable.

**Task 5 — Secure Configuration Review** *(sourced from SEC-110 learning outcomes and NIST SP 800-207A access-control guidance already cited in your literature review)*
Given a server or cloud resource with several misconfigured access controls, identify and correct the misconfigurations, and document the security rationale for each change.

---

## Notes for methodology writeup

- Instruments 2 and 3 together operationalize the "perceived preparedness" and "demonstrated capability" language already used in your Research Question section — Instrument 2 is the perception measure, Instrument 3 is the performance measure.
- The rubric dimensions in Instrument 3 (configuration accuracy, troubleshooting accuracy, task completion, escalation decisions, documentation completeness) are the exact five named in your existing "Technical Performance Measurement and Quantitative Design" literature theme — worth citing that alignment explicitly when you write this up, since it shows the instrument wasn't built independently of the lit review.
- None of these items reference clearance eligibility directly — that stays a contextual/descriptive variable (see the last item in Instrument 1), not a performance or readiness measure, consistent with the Study Problem framing that clearance is a labor-market gatekeeping factor separate from technical readiness.
- These are drafts, not validated instruments — they still need expert/content review and a pilot administration before use, per standard survey development practice you'd cite from Creswell & Creswell.
