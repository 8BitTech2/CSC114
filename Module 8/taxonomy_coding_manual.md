# Skill Taxonomy Coding Manual

Purpose: make category boundaries explicit enough that a second rater can apply them independently, without needing to guess at judgment calls that currently only exist in the original author's head. Use this manual when coding any course description or O*NET task line against the 9-category skill taxonomy.

## How to use this manual

For each document (course description or O*NET task line), read the full text and decide, for each of the 9 categories: does this document belong to this category? (Yes/No). A document can belong to more than one category (multi-label) — that's expected, not an error.

When a document could plausibly fit more than one category, use the **decision rule** for each relevant category below, in the order listed. If a document still fits two categories after applying the decision rules, code it as both — that reflects genuine overlap in the content, not coder error.

Record your answers as Yes/No per category per document. Do not discuss your codes with the other rater until both of you have finished coding the full sample independently — coordinating in advance defeats the purpose of measuring agreement.

---

## Category 1: Virtualization

**Include if:** the text describes creating, configuring, migrating, or managing virtual machines, hypervisors, or virtual desktop infrastructure — regardless of which vendor platform.

**Exclude if:** the text only mentions "cloud" in a general sense without describing VM/hypervisor-level administration (that's `cloud_platforms` instead — see the boundary rule below).

**Boundary with cloud_platforms:** This is the trickiest boundary in the taxonomy. Use this rule: if the text describes *generic virtualization administration tasks* (managing VMs, snapshots, resource allocation) without naming a specific cloud platform, code `virtualization` only. If the text names a specific platform (AWS, Azure, GCP) or describes platform-specific services (S3, EC2, Azure AD), code `cloud_platforms` as well, even if the primary content is virtualization administration. Known example: CTI-240/CTI-241 course descriptions are generic virtualization text with no platform named, but their industry-certification alignment (AWS Solutions Architect, Azure Administrator) shows they teach platform-specific content — code these using certification text as well as description text, per the fix already applied in `apply_taxonomy.py`.

## Category 2: Networking

**Include if:** the text describes designing, configuring, or explaining network architecture, addressing schemes, routing, switching, or network standards.

**Exclude if:** the text is about *diagnosing or fixing* a network problem after the fact rather than designing or configuring it — that's `monitoring_troubleshooting` (see boundary rule below).

**Boundary with monitoring_troubleshooting:** Ask whether the task is prospective (building/configuring something that doesn't yet exist or isn't yet broken) or reactive (responding to an existing problem). "Configure VLANs" = `networking`. "Troubleshoot inter-VLAN routing" = both `networking` and `monitoring_troubleshooting`, since it requires networking knowledge applied reactively.

## Category 3: Cloud Platforms (AWS/Azure/GCP)

**Include if:** the text names a specific cloud platform or vendor (AWS, Azure, GCP), or describes cloud-specific concepts (cloud storage, cloud terminology, elasticity, multi-tenancy) rather than on-premises equivalents.

**Exclude if:** the text is about on-premises hardware or generic IT concepts with no cloud-specific framing.

**See the boundary rule under Virtualization above** — this is the same boundary, viewed from the other side.

## Category 4: Storage

**Include if:** the text describes storage provisioning, SAN/NAS administration, backup, or disaster recovery.

**Exclude if:** storage is only mentioned in passing as part of a broader virtualization or cloud task with no dedicated storage-administration content.

## Category 5: Security / Compliance

**Include if:** the text describes access control, secure configuration, compliance policy, risk assessment, or identity/authentication.

**Exclude if:** the text describes *responding to* a security incident that's already occurred — that's `monitoring_troubleshooting`, not `security_compliance` (see boundary rule below).

**Boundary with monitoring_troubleshooting:** This is the second-trickiest boundary. Ask: is this about *designing or enforcing* a security control (→ `security_compliance`), or *detecting/responding to* a violation or incident after it happens (→ `monitoring_troubleshooting`, and often both)? "Create an information security policy" = `security_compliance` only. "Respond to computer security breaches" = both.

**Note:** Security clearance requirements themselves are explicitly *excluded* from this category's scoring — clearance is a labor-market eligibility factor, not a technical competency, per the Study Problem framing. Do not code job postings' clearance requirements as `security_compliance` content.

## Category 6: Scripting / Automation

**Include if:** the text describes writing, testing, or debugging scripts or programs, or automating a routine task.

**Exclude if:** a tool is merely "used" without any scripting/programming activity described (e.g., "using monitoring software" is not automatically `scripting_automation`).

## Category 7: Monitoring & Troubleshooting

**Include if:** the text describes diagnosing, detecting, or resolving a problem; monitoring system health; or responding to an alert or incident.

**Exclude if:** the text is purely about building/configuring something new, with no diagnostic or reactive component.

**See boundary rules under Networking and Security/Compliance above** — this category legitimately overlaps with both.

## Category 8: Hardware / Physical Infrastructure

**Include if:** the text describes physical equipment — cabling, racking, physical server installation, or datacenter physical layout.

**Exclude if:** "hardware" is mentioned only as a category label without physical/tactile installation or maintenance content (e.g., "computer hardware" in a general IT-literacy course description does not automatically qualify — check whether physical installation/maintenance is actually described).

## Category 9: ITIL / Business & Soft Skills

**Include if:** the text describes business-process alignment, documentation practices, stakeholder communication, project management, or ITIL-framework concepts.

**Exclude if:** communication is only implied (e.g., any job inherently requires "talking to people") without explicit documentation, briefing, or business-process content.

---

## After coding: what to do with disagreements

1. For each category, calculate Cohen's kappa between the two raters' Yes/No codes across the full sample (see `compute_kappa.py`).
2. For any category with kappa below 0.6, pull every document where the raters disagreed and read both raters' reasoning.
3. Ask: was the disagreement caused by an ambiguous rule in this manual, or a one-off misread of the document? If it's a rule problem, revise the decision rule above and note the revision and why below.
4. Optionally, re-code the disagreed subset using the revised rule and recompute kappa on that subset only, to confirm the revision helped.

## Revision log

*(Add entries here as you revise category boundaries based on inter-rater disagreement.)*

- No revisions yet — this manual reflects the taxonomy as of the initial write-up, prior to any second-rater coding.
