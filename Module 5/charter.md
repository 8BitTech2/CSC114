# Project Charter: Curriculum Gap Analyzer

## What I am building (one sentence)
A model that classifies FTCC Cloud Management course outcomes and datacenter job posting requirements into a shared skill taxonomy, then compares them to produce a per-category readiness/gap score.

## Cohort
NLP

## The data or tools I will use
- FTCC course catalog (course descriptions/outcomes) for the Cloud Management program
- A fixed, one-time-collected snapshot of datacenter/cloud job postings (~30–50 postings, manually or one-time scraped, saved to CSV — not a live re-scraping pipeline)
- Skill taxonomy (8 categories): virtualization, networking, cloud platforms, storage, security/compliance, scripting/automation, monitoring & troubleshooting, hardware/physical infrastructure
- TF-IDF vectorization + logistic regression classifier to tag course-outcome/job-requirement snippets into taxonomy categories

## Definition of "good enough"
Before I build, I agree this project is good enough when:
- The classifier beats a dumb baseline (majority-class guess) on skill-category accuracy, measured on a held-out validation split of labeled snippets
- The gap report correctly surfaces at least one real, defensible mismatch between course coverage and job posting frequency for a category (a sanity check that the pipeline's output is meaningful, not just accurate on paper)

## What I am NOT doing (scope guard)
- No live/repeated job-posting scraping — using a fixed one-time snapshot instead
- No optional LLM layer for natural-language summaries or named-entity extraction (may revisit as a stretch goal in a later iteration)
- No ITIL/soft-skills category in the taxonomy this cycle
- No sentence-transformer embeddings or Keras neural net — TF-IDF + logistic regression only, as the baseline model

## Team & roles
Solo.
