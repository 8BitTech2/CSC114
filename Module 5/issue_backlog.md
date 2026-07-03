# Issue Backlog — Curriculum Gap Analyzer (Walking Skeleton for Module 6)

These issues describe the first working version: the smallest end-to-end
pipeline that runs, even badly. Not the polished final product.

---

### Issue 1: Load and clean course outcome data
Pull FTCC Cloud Management course descriptions/outcomes into a simple
structured format (CSV or list of strings) that later steps can consume.

### Issue 2: Collect job posting snapshot
Manually gather ~30–50 datacenter/cloud job postings into a fixed CSV
(title + requirements text). One-time collection — no live scraping.

### Issue 3: Label a small training set
Hand-label a subset of course-outcome and job-posting snippets with the
8 taxonomy categories (virtualization, networking, cloud platforms,
storage, security/compliance, scripting/automation,
monitoring & troubleshooting, hardware/physical infrastructure) to
train and validate the classifier.

### Issue 4: Build baseline classifier
TF-IDF + logistic regression, trained on labeled snippets. Must beat a
majority-class baseline on held-out validation accuracy.

### Issue 5: Generate a rough gap report
Run the classifier on all course outcomes and job postings, tally
category counts, and output a basic readiness score per category
(a printed table is fine for this version).
