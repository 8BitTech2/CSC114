# Spring 1 Reflection

*Module 5: Assess — Machine Learning Workflow*
*Case study: Curriculum-to-Career (C2C) Gap Analyzer*

> Note: This is the reflection, with annotations explaining *why* each part meets the Proficient bar on the rubric rather than Developing. I will use this version when walking students through what separates a vague reflection from a strong one.

---

## 1. What actually runs right now?

My charter (`charter.md`) scoped a pipeline that takes FTCC's Cloud Management course outlines on one side and real job requirement data (O*NET occupation data across five target occupations) on the other, classifies both onto a shared skill taxonomy, and produces a readiness score per skill category. As of today, that full pipeline runs end-to-end: data collection pulls in the course outlines and O*NET data, `apply_taxonomy.py` labels both sides against `skill_taxonomy.json`, a TF-IDF + OneVsRest logistic regression classifier trains on the labeled data, and the gap-analysis step outputs readiness scores by category. Those scores render in `ftcc_readiness_dashboard.html`, which is the actual deliverable I can hand someone and have them click through.

I also ran the agent against all three test cases from my test plan: known-good, trap, and edge, rather than only the one that worked. On the **known-good** case (a course outcome that explicitly says "configure AWS EC2 instances"), it correctly classifies into the cloud-platforms category. It fails the **trap** case: a job listing line like "comfortable working in a cloud-based team environment" uses "cloud" in a non-technical sense, and the classifier still tags it as a cloud-platforms skill requirement, inflating that category's readiness score. On the **edge** case, a job listing with a blank or single-word requirement line, the pipeline doesn't crash, but it silently drops the row instead of flagging it, so I don't currently know how many rows are getting dropped this way.

So in short: **ingestion → taxonomy labeling → classifier training → gap scoring → dashboard** is a real, repeatable pipeline right now. What's *not* running yet is the agent-orchestration loop described in `Model_idea.docx`. That's still a design document, not code. Today the steps run as a sequence I trigger manually, not as an autonomous agent that fetches, scores, and reports on its own.

> **📝 Why this is Proficient, not Developing:**
> - Names the *actual pipeline stages* by their real file/step names (`apply_taxonomy.py`, `skill_taxonomy.json`, `ftcc_readiness_dashboard.html`) instead of saying "my project works."
> - Distinguishes what runs (the manual sequence) from what was scoped but doesn't exist yet (the autonomous agent loop). A Developing response tends to blur "I built an agent" with "I wrote scripts I run by hand."
> - Reports results on **all three** test cases, including the two it fails, and explains *why* the trap-case failure matters (it inflates the most important category) rather than just noting it failed.

---

## 2. What's still missing or broken?

Two things stand out. First, the trap-case failure above isn't cosmetic, it's a real threat to the study's validity, since misclassifying "soft" uses of a keyword as technical requirements would overstate readiness in exactly the category (cloud platforms) that matters most for the research question. I need better negative examples in training data before I'd trust that category's score. Second, the agent-orchestration layer itself is missing: right now I am the orchestration, and I run each script by hand in sequence. The `agent-guardrails.md` I wrote describes what a human-in-the-loop checkpoint should look like before the agent regenerates a gap report, but there's no agent loop yet for that guardrail to actually gate.

There's also a finding that surfaced during this sprint that wasn't in the original taxonomy: most local employer listings require an active or obtainable Secret clearance, and that's a readiness dimension the current taxonomy doesn't capture at all, it's not a skill category, it's a hiring-pipeline gate that sits outside curriculum content entirely. My GitHub backlog has an open issue to decide whether to add it as a taxonomy dimension or handle it as a separate finding in the report.

> **📝 Why this is Proficient, not Developing:**
> - Connects a bug (trap-case misclassification) to its downstream consequence for the actual research question, not just "the classifier has an error."
> - Names the gap between "guardrail is documented" and "guardrail is enforced by running code," a subtle but important distinction a Developing response usually collapses into "guardrails are in place."
> - Surfaces an unplanned finding (security clearance) honestly, and shows it's tracked (open backlog issue) rather than mentioned once and forgotten.

---

## 3. Are you still on track with the scope from your charter, or has anything changed?

Mostly on track, with two real changes worth naming honestly instead of glossing over. First, my original gap-scoring approach used an absolute similarity threshold, which produced near-zero readiness scores across the board, not because the curriculum was bad, but because the threshold didn't account for what's actually achievable given the dataset. I corrected this by normalizing scores against the dataset's achievable ceiling instead, which produced meaningful, interpretable results. That's a methodology change I've documented rather than a quiet fix, because it affects how the scores should be interpreted. Second, the security clearance finding above wasn't in the charter's scope at all. The charter focused on skill-content gaps, not hiring-pipeline gaps. I'm not pulling it into the classifier pipeline, but I am flagging it as a finding worth naming explicitly rather than ignoring because it doesn't fit the original taxonomy.

Everything else: the core "curriculum vs. job market, scored by category" shape of the project, is unchanged. I think both adjustments were the right call: a scoring method that's actually interpretable, and a willingness to report a real finding even when it falls outside the original scope, are both more valuable than rigidly sticking to a plan that turned out to be incomplete.

> **📝 Why this is Proficient, not Developing:**
> - Two changes, each with what changed, why, and where it's documented: a Developing response usually reports zero changes (because it didn't check) or one change with no reasoning.
> - Distinguishes a *methodology* fix (normalization) from a *scope* addition (clearance finding) rather than lumping every change into one vague "some things changed" statement.
> - Explicitly defends the decision not to force the clearance finding into the existing taxonomy, showing judgment about what belongs in the model versus what belongs in the narrative around it.

---

## 4. Share-Out Talking Points

*The four-line spoken version of everything above: the compressed script for saying this out loud at Check-In, rather than reading the full reflection aloud.*

| Say this | What I'd actually say |
|---|---|
| **What I'm building** | An agent that compares FTCC's Cloud Management curriculum against real job requirements and scores readiness by skill category. |
| **What runs today** | Right now it takes course outlines and O*NET job data and gives back a readiness dashboard scored per category. |
| **What's broken or missing** | It fails my trap test case, it misreads non-technical uses of "cloud" as technical skill matches, and the agent-orchestration loop is still just a design doc, not code. |
| **What I'm doing next** | Before Check-In 2, I'm fixing the trap-case misclassification first since it directly inflates my most important category. |

> **📝 Why this translation works:**
> - Each line is **one sentence**, matching the "same as your charter" and "X gives back Y" prompts literally.
> - "What's broken" names the specific failure mode (misreading non-technical "cloud") instead of softening into "still tuning the model."
> - "What's next" prioritizes the fix with the biggest validity impact, not just the easiest one to make.

---

### Rubric alignment summary

| Question | Developing looks like... | Proficient looks like... |
|---|---|---|
| What runs? | Vague ("mostly works") | Named stages + linked artifacts (specific files, specific scripts) |
| Test cases | Reporting only the passing case, or "testing TBD" | All three (known-good, trap, edge) reported, with the failure's real-world consequence explained |
| What's missing/broken? | A list with no stakes | Gaps explained with consequences, tied to backlog |
| Scope check | Unchecked "yes, on track" or unexplained drift | Explicit changes, reasoning, and documentation trail; methodology fixes distinguished from scope additions |
