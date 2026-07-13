# Spring 1 Reflection

## What actually runs right now?

**C2C Gap Analyzer pipeline (doctoral study):**
- A complete, functioning pipeline: data collection → taxonomy definition → classifier training → gap analysis.
- Ingests real FTCC course outlines (Cloud Management AAS, A25590U) and O*NET job requirement data across five occupations.
- Classifier: TF-IDF + OneVsRest LogisticRegression (scikit-learn), multi-label, cosine similarity scoring.
- `ftcc_readiness_dashboard.html` — an interactive dashboard that visualizes readiness scores by skill category and occupation. This is the current primary deliverable and it renders correctly.
- Local job listings (GDIT, Sherpa 6, Abacus Technology, Cumberland County) have been mapped onto the skill taxonomy.
- A methodology bug was found and fixed: the original absolute-similarity-threshold scoring produced near-zero readiness scores across the board. Normalizing against the dataset's actual achievable ceiling fixed this and now produces interpretable results.

**CSC-114:**
- Module 5 (Assess: Machine Learning Workflow) is complete.
- Instructor rubric is finished, covering four student artifacts: `charter.md`, GitHub issue backlog, `agent-guardrails.md`, `reflection.md`.
- Rubric uses a Complete/Redo model with Developing→Proficient descriptors.

## What's still missing or broken?

- **AI agent (`Model_idea.docx`)** — the concept for automating curriculum-to-job-market gap analysis end-to-end is designed but has zero code written. Still idea/planning stage.
- **Security clearance gap is identified but not written up** — most local employer listings require active or obtainable Secret clearance, a readiness dimension entirely absent from FTCC's curriculum. Only the Cumberland County Government listing is a clean entry-level fit without that barrier. This finding hasn't been formalized into the Study Problem or Literature Review sections of the prospectus yet.
- **Scenario-task items / survey questions** drawn from local job listing language — discussed as a way to tie employer requirements to readiness construct validity, but not drafted.
- **Taxonomy table** — flagged as needing expansion as a working artifact; not yet done.

## Are you still on track with the scope from your charter, or has anything changed?

The core scope is intact: the pipeline (data → taxonomy → classifier → gap analysis → dashboard) is built and working as originally scoped, and it's producing real, interpretable output rather than placeholder results.

What's shifted:
- The **security clearance finding** is a new, unplanned dimension the data surfaced — it wasn't part of the original readiness construct but is now a candidate for an explicit finding in the prospectus. This is scope-expanding, not scope-breaking, but it needs a decision on where it lives in the write-up.
- The **AI agent piece** is behind where the charter implied it would be by this point — it's still concept-only. The open question is whether to scope down to a smaller build given deadlines, or commit to the full pipeline-wrapping agent as designed.
