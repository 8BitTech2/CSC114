# Skill Taxonomy — Expanded Reference Table (v2)

Base 9 categories as originally defined in `Model_idea.docx`, expanded with explicit crosswalks to FTCC courses, certifications, O*NET occupations, and real employer language. This is the human-readable companion to `skill_taxonomy_v2.json`, which is the machine-readable version the pipeline actually loads.

| Category | FTCC Course(s) | Relevant Certifications | O*NET Occupations | Example Real Employer Language |
|---|---|---|---|---|
| **Virtualization** | CTI-141, CTI-240, CTI-241 | VMware VCTA/VCP, Microsoft AZ-800, CompTIA Cloud+ | Network & Computer Systems Administrators; Computer Systems Engineers/Architects | "Citrix VDI, Microsoft VDI, Virtual Desktop Infrastructure (VDI), VMware VDI" — GDIT, Fort Liberty |
| **Networking** | CTI-120, NET-125, NET-126 | CompTIA Network+, Cisco CCNA | Network & Computer Systems Administrators; Computer Network Architects | "Computer Networking, Computer Systems, Group Problem Solving, Network Systems" — GDIT Network Administrator |
| **Cloud Platforms (AWS/Azure)** | CTI-141 | AWS Cloud Practitioner, Microsoft AZ-900, CompTIA Cloud+ | Network & Computer Systems Administrators; Information Security Analysts; Computer Systems Engineers/Architects | "familiar with cloud technologies and principles" — GDIT Cloud Service Operations Specialist |
| **Storage** | CTI-141, CTI-240, CTI-241 | Vendor-specific SAN/NAS certs | Network & Computer Systems Administrators; Information Security Analysts | "Backup and Recovery (Software)" — GDIT Systems Administrator |
| **Security / Compliance** | CTI-120, SEC-110 | CompTIA Security+ | Information Security Analysts; Computer Network Architects | Secret/TS clearance requirement itself — see Study Problem clearance finding |
| **Scripting / Automation** | CSC-121, NOS-125 | Python Institute PCEP/PCAP, CompTIA Linux+ | Network & Computer Systems Administrators; Computer Systems Engineers/Architects | Shell scripting, process control — NOS-125 course description |
| **Monitoring & Troubleshooting** | CTI-241, NOS-110, NET-126 | CompTIA A+ | Network & Computer Systems Administrators; Computer User Support Specialists; Computer Network Architects | "rapidly troubleshoot Tier-1 support issues" — GDIT Cloud Service Operations Specialist |
| **Hardware / Physical Infrastructure** | NOS-110 | CompTIA A+ | Network & Computer Systems Administrators | Cable Technician roles posted alongside GDIT IT Infrastructure listings |
| **ITIL / Business & Soft Skills** | CTS-115, CTI-289 | ITIL Foundation | Computer User Support Specialists; Computer Systems Engineers/Architects | "Good written and technical briefing skills" — GDIT Cloud Service Operations Specialist |

## What changed from v1

- **Course crosswalk added** — each category now names the specific FTCC courses that cover it, rather than relying on the classifier to infer this from course descriptions alone.
- **Certification and occupation crosswalks added** — ties each category to concrete, citable external standards (useful for the "Workforce Standards, Certifications, and Gray Literature" literature theme).
- **Keyword lists expanded**, particularly for `cloud_platforms` and `security_compliance`, to capture more phrasing variants.
- **Classifier bug found and fixed during this expansion**: `cloud_platforms` was scoring 3.5/100 curriculum coverage in the original pipeline despite CTI-141 being weak-labeled correctly. Diagnosis: only 1 of 74 training documents was a positive example for that category, and `LogisticRegression` without class balancing suppressed its predicted probability to near-zero even for the true positive. Adding `class_weight="balanced"` to the classifier raised CTI-141's predicted probability from 0.03 to 0.89, and curriculum coverage for the category from 3.5 to 34.4. This fix is now in `apply_taxonomy.py`.
- **Hardware/physical infrastructure flagged as a genuine (not artifact) weak category** — only one course (NOS-110) touches it directly, and it remained among the lowest-scoring categories even after the classifier fix.

## Still not done

- Category boundaries (e.g., overlap between `monitoring_troubleshooting` and `security_compliance` for incident response) haven't been reviewed by a second rater — this is still a single-author taxonomy.
- No inter-rater reliability check has been run on the weak-labeling keyword lists.
- Course crosswalks were built from the real NCCCS course descriptions gathered earlier in this project, not from a formal content analysis — worth strengthening before this table goes into the dissertation as a validated instrument rather than a working artifact.
