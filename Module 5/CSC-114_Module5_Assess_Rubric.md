# CSC-114 Module 5 — Assess: Grading Rubric
## Inception — Mini-Project Charter, Backlog, Guardrails, Reflection

**Grading model:** Complete / Redo per artifact, with a **Developing → Proficient** band describing what separates a bare Complete from strong work in each rubric category. Nothing here is letter-graded; a "Redo" simply routes the student back to fix and resubmit before it counts.

**Rubric categories** (weight emphasis for Module 5 noted): **Problem-Solving Process** (primary), **Professional Communication** (primary), **AI Partnership Quality** (light this module), **Critical Thinking & Ethics** (light this module).

---

## 1. Artifact → Category Map

| Artifact | Primary category | Secondary category |
|---|---|---|
| `charter.md` | Problem-Solving Process | Professional Communication |
| Issue backlog (3–5 issues) | Problem-Solving Process | — |
| `agent-guardrails.md` | AI Partnership Quality | — |
| `reflection.md` | Critical Thinking & Ethics | Problem-Solving Process |

---

## 2. `charter.md`

**Complete requires all six charter fields present and non-generic:**
- [ ] One-sentence problem/task statement
- [ ] Cohort declared (Tabular / Image / NLP / Agent)
- [ ] Data or tools named specifically (dataset + source, or agent tools/instructions)
- [ ] Definition of "good enough" — **must contain both** a metric/ruler *and* a threshold drawn on it (see cohort table below). One without the other = Redo.
- [ ] Scope guard: 2–3 specific things they are choosing *not* to do
- [ ] Team & roles (solo, or pair + who reviews whose PRs)

**Redo triggers:**
- Definition of "good enough" gives only a metric name with no threshold (e.g., "we'll use accuracy" and stops there)
- Scope guard is missing, vague ("we'll keep it simple"), or lists things that aren't actually tempting/likely
- Charter describes a scope no pair could plausibly finish in three iterations (Modules 6–8) — this is the single most common Redo reason

**Developing → Proficient band (Problem-Solving Process):**
| Developing | Proficient |
|---|---|
| Fields are filled in but generic; threshold is a guess with no baseline reference | Threshold is tied to a stated baseline (e.g., "beats predict-the-mean" or "beats always-guess-majority") and is specific enough that a reader could check it objectively |
| Scope guard lists trivial exclusions | Scope guard names the *actually tempting* over-build the pair is likely to attempt |

**Developing → Proficient band (Professional Communication):**
| Developing | Proficient |
|---|---|
| Charter is readable by the author but assumes shared context | Charter is legible to someone outside the course — no unexplained jargon, dataset named and findable, "what we're building" understandable in one read |

**Cohort-specific "good enough" check (must match one row):**

| Cohort | Must contain |
|---|---|
| Tabular | Metric (e.g., MAE / accuracy) + evaluation protocol (train/val split or k-fold) + baseline-beating threshold |
| Image | Same as Tabular, plus a realistic note on dataset size / download cost for Codespaces |
| NLP | Same as Tabular, on a text-appropriate metric |
| Agent | The three-test set (known-good, trap, edge) named as the evaluation protocol — no dataset required |

---

## 3. Issue Backlog (3–5 GitHub Issues)

**Complete requires:**
- [ ] 3–5 issues present in the repo
- [ ] Each issue is in the student's own words (not copy-pasted from the charter)
- [ ] Issues collectively describe the **walking skeleton** — the first working, end-to-end version (Module 6's target) — not a finished/tuned product
- [ ] No issue smuggles in Module 7-level work (tuning, scaling, regularization)

**Redo triggers:**
- Fewer than 3 issues, or issues that just restate the charter sentence
- Issues describe a "good" model rather than a "running" one (wrong level — that's Module 7)

---

## 4. `agent-guardrails.md`

**Complete requires:**
- [ ] What the AI partner **is** allowed to do
- [ ] What it must **never** do unprompted
- [ ] How the student will **check** its work before merging

**Redo triggers:**
- Guardrails are boilerplate/generic with no connection to *this* project's risk (e.g., doesn't mention the specific files, scope, or tasks the agent will touch)
- No verification step described

**Developing → Proficient band (AI Partnership Quality):**
| Developing | Proficient |
|---|---|
| Guardrails are a generic list of dos/don'ts | Guardrails anticipate a specific plausible failure for *this* project (e.g., "must not rewrite the training loop without a PR") and name the check that would catch it |

---

## 5. `reflection.md`

**Complete requires an honest answer to both:**
- [ ] Which workflow step were you on when California Housing stopped (per Module 4)?
- [ ] What's different this time — in the project itself or in how you're approaching the process?

**Redo triggers:**
- Answer is purely descriptive of Housing with no connection drawn to the new project
- "What's different" is a restatement of the charter rather than a reflection on process/approach

**Developing → Proficient band (Critical Thinking & Ethics):**
| Developing | Proficient |
|---|---|
| Names the stopping point but not *why* it happened | Connects the stopping point to a specific habit they're changing this round (e.g., "last time we didn't define done, so we kept tuning past the turnaround — this charter's threshold exists so that doesn't happen again") |

---

## 6. Cross-Cutting Redo Flags (apply across all four artifacts)

- [ ] **Rubber-stamp review:** a PR was merged with only "looks good" and no specific comment quoting a line and explaining why. Reviewing is graded work here, not a formality — flag and require a real review before final Complete.
- [ ] **Solo review substitute missing:** solo students must document their self-review or AI-partner rubber-duck check in writing on the PR; an unreviewed solo merge is a Redo.
- [ ] **Mixed-cohort pair:** both partners in a pair must have selected the same cohort.
- [ ] **No metric/threshold split:** anywhere "good enough" appears without both a ruler and a line drawn on it, send it back — this is the Module 5 boss fight and the most common miss.

---

## 7. Quick Grading Pass (suggested order)

1. Open `charter.md` — check cohort match, then the good-enough field first (this is where most Redos originate).
2. Skim scope guard — does it name a real risk for *this* project?
3. Check issue backlog against charter — do they describe a skeleton, not a finished model?
4. Check `agent-guardrails.md` for project-specific (not generic) content.
5. Check `reflection.md` for an actual causal link, not just a restatement.
6. Spot-check one PR per team for review quality (catches rubber-stamping).

**Escalation contacts:** Mallory Milstead · Andrew Norris
