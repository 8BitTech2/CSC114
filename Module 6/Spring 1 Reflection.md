# Spring 1 Reflection — C2C Gap Analyzer

*Module 5: Assess: Machine Learning Workflow*

> Note: This is the reflection, with annotations explaining *why* each part meets the Proficient bar on the rubric rather than Developing.
> Use this version when walking through what separates a vague reflection from a strong one.

---

## 1. What actually runs right now?

My charter (`charter.md`) scoped a small text-classification pipeline: pull a handful of sample documents, extract basic features, train a classifier, and report accuracy on a held-out set. As of today, the data loading and preprocessing steps run cleanly end-to-end. 
I can point the script at my sample data folder and get back a cleaned, tokenized dataset without errors. 
The training step also runs: a baseline model fits on the training split and produces predictions on the test split. 
I have a working accuracy score printed at the end of the run, and I've committed the script along with a short `agent-guardrails.md` describing the limits I built in (e.g., the agent won't retrain automatically without a human confirming the data looks right).

So in short: **ingestion → preprocessing → training → basic evaluation** is a real, repeatable pipeline right now, not just a plan.

> **📝 Why this is Proficient, not Developing:**
> - Names the *actual pipeline stages* (ingestion, preprocessing, training, evaluation) instead of saying "my project works."
> - Ties each claim back to a specific artifact (`charter.md`, `agent-guardrails.md`), the reflection references real evidence an instructor could go check.
> - Distinguishes "runs" from "runs well." It says accuracy prints, not that the model is good. That precision is what a Developing response usually blurs.

---

## 2. What's still missing or broken?

A few things from the charter aren't there yet. First, my evaluation is thinner than I wanted. I'm only reporting accuracy, not precision/recall/F1, so I don't actually know how the model performs on the minority class, which matters given my dataset is imbalanced. 
Second, the "human-in-the-loop" checkpoint I described in `agent-guardrails.md` is only partially implemented: the script pauses and prints a summary before training, but it doesn't yet require an explicit confirmation input, so it's more of a warning than a real gate. 
Third, two issues in my GitHub backlog are still open and blocking: one about handling malformed rows instead of silently dropping them, and one about logging model runs so I can compare experiments later. Neither is hard, but neither is done.

> **📝 Why this is Proficient, not Developing:**
> - Each gap is described with *consequence*, not just listed ("I don't know how it performs on the minority class", explains why the gap matters, not just that it exists).
> - Self-assessment is calibrated: it distinguishes "partially implemented" from "not implemented," which shows the student actually understands their own guardrail design rather than treating it as done/not-done.
> - Ties gaps directly to open backlog issues: reflection and project tracking are consistent with each other, which the rubric rewards as evidence the artifacts weren't produced in isolation.
> - A Developing response here would typically say something like "a few bugs still need fixing" with no specifics.

---

## 3. Are you still on track with the scope from your charter, or has anything changed?

Mostly on track, with one real scope change. The charter originally proposed comparing three different classifier types. After getting the first one working, I realized that was overambitious for this sprint,  most of my time went into data cleaning I hadn't planned for, since the sample data was messier than expected. I've scaled back to one solid baseline model this sprint and pushed the comparison of additional models to a stretch goal, which I've noted directly in the backlog rather than quietly dropping it. Everything else in the charter (the guardrails concept, the basic pipeline shape) is unchanged. I think this was the right call: a single pipeline that actually runs and is honestly evaluated is more valuable right now than three half-working ones.

> **📝 Why this is Proficient, not Developing:**
> - States *what changed*, *why it changed*, and *where the change is documented* (backlog), three things an instructor looks for to confirm the scope change was managed, not just noticed after the fact.
> - Makes a judgment call explicit ("I think this was the right call...") and defends it, which shows ownership of the decision rather than reporting drift passively.
> - A Developing response typically either claims "no changes" without checking, or lists a change with no reasoning, this response does neither.

---

### Rubric alignment summary

| Question | Developing looks like... | Proficient looks like... |
|---|---|---|
| What runs? | Vague ("mostly works") | Named stages + linked artifacts |
| What's missing/broken? | A list with no stakes | Gaps explained with consequences, tied to backlog |
| Scope check | Unchecked "yes, on track" or unexplained drift | Explicit change, reasoning, and documentation trail |
