# Demo Talking Points — Factual Reference

Reference material only — the actual explaining in class should be in your own words, especially for "why" and "what I'd revisit," since the rubric is checking whether *you* can answer follow-ups without hesitation.

---

## 1. The goal

The agent checks whether a community college's Cloud Management curriculum actually prepares students for the cloud/data center jobs available in the local area — and produces a plain-language report on where the gaps are.

## 2. The data

- **Curriculum data**: real course descriptions from FTCC's Cloud Management AAS (A25590U), 15 courses. Pulled from NCCCS's statewide standardized course catalog text (identical across NC community colleges) rather than FTCC's own catalog PDFs, which have a font-encoding bug that corrupts text extraction.
- **Job-requirement data**: real O*NET task and technology data for five occupations relevant to this program — Network and Computer Systems Administrators, Information Security Analysts, Computer User Support Specialists, Computer Network Architects, and Computer Systems Engineers/Architects. Currently sourced via web search; an `onet_client.py` script was also built to pull this from O*NET's actual Web Services API instead (structured Tasks, Technology Skills, Skills, and Knowledge with standardized importance ratings) — built but not yet swapped into the live pipeline, since it needs your own O*NET developer credentials to run.
- **Local grounding**: real, currently posted job listings from GDIT (Fort Liberty-area postings) and county-government IT postings, used to word the scenario-based performance tasks and readiness survey items in actual employer language rather than generic phrasing.
- **Expert-coded ground truth**: a hand-coded matrix mapping all 15 courses against all 9 taxonomy categories, coded by you directly — not automated. This now drives curriculum-side scoring (see Example C below).

## 3. The approach

- A 9-category skill taxonomy (virtualization, networking, cloud platforms, storage, security/compliance, scripting/automation, monitoring & troubleshooting, hardware/physical infrastructure, ITIL/soft skills).
- **Curriculum side**: scored directly from your expert-coded matrix — no automated inference. **Job side**: O*NET task text weak-labeled by keyword, then a TF-IDF + OneVsRest LogisticRegression classifier trained on that data (now trained using your expert labels for the curriculum portion, not just noisy keyword labels).
- Scores are normalized against the dataset's own achievable ceiling (not an arbitrary cutoff), producing a 0–100 readiness score per skill category per occupation.
- An agent step wraps that whole pipeline and calls Claude (Anthropic API) to turn the numbers into a natural-language gap report with specific recommendations.

## 4. How it improved — three concrete examples

**Example A — a code fix (classifier bug):**
- **First version**: the dashboard showed `cloud_platforms` scoring 3.5/100, despite one course (CTI-141, "Cloud & Storage Concepts") being dedicated entirely to that topic.
- **First fix tried**: assumed the taxonomy's keyword list was too narrow, so expanded it. Reran the pipeline — score didn't change at all (still 3.5/100).
- **What that ruled out**: checked the weak-labeling directly and confirmed CTI-141 was already correctly tagged for that category before the keyword change — so the labeling step was never the problem.
- **Real cause, found by checking the classifier's per-course predicted probabilities directly**: only 1 of 74 total training documents was a positive example for `cloud_platforms`. Without class balancing, `LogisticRegression` suppressed the predicted probability toward zero even for that one true positive (it was scoring 0.03).
- **Actual fix**: added `class_weight="balanced"` to the classifier.
- **Verified result**: CTI-141's predicted probability rose from 0.03 to 0.89, and the category's score rose from 3.5 to 34.4 — confirmed by rerunning and checking the actual numbers, not just assuming the code change worked.

**Example B — a data fix, caught by noticing the source data was incomplete, not by debugging code:**
- The NCCCS course-description text used to classify curriculum content doesn't actually describe what's taught in enough depth — it's generic, standardized-statewide text, not FTCC's own detailed course content.
- FTCC's official `2025SU_IT_CROSSWALK.pdf` (Computer Technologies Certificate Crosswalk) showed that CTI-240 and CTI-241 — described generically as "virtualization administration" — actually align to the **AWS Certified Solutions Architect – Associate** and **Microsoft Azure Administrator (AZ-104)** exams specifically. The course description text never mentions AWS or Azure by name, so the classifier had no way to detect this.
- **Fix**: added each course's real, official industry-certification names as additional classification signal alongside its description text.
- **Verified result**: `cloud_platforms` curriculum coverage rose from 34.4 to 70.6 — nearly double, grounded in an authoritative FTCC document rather than an inferred code change.

**Example C — trusting expert judgment over automation entirely (the strongest example — consider leading with this one):**
- Hand-coded every course against every taxonomy category yourself, then tested the automated classifier against your own coding as an actual validity check, not another tuning pass.
- **Result**: Cohen's kappa = 0.073 between your expert coding and the classifier's labels — "slight" agreement, essentially none. 84 of 144 cells disagreed, almost entirely in one direction: the classifier was under-counting real coverage you could see and it couldn't.
- **Fix**: rebuilt the pipeline so curriculum-side scoring comes directly from your expert-coded matrix, not classifier predictions. The classifier still exists, but only for scoring the O*NET job-task side, where no expert coding exists — and it's now trained on your labels for the curriculum portion instead of noisy keyword weak-labels.
- **Why this one matters most**: it's not a bug fix — it's you testing whether the automation was trustworthy at all, finding it wasn't, and having a principled fallback (your own domain expertise) ready to use instead. That's the actual skill the rubric's "AI Partnership Quality" and "Critical Thinking" rows are checking for.

## 5. The live demo

Plan: run `agent.py` live, showing it load the real data, train the classifier, score the gap analysis, and call Claude to generate the report. This has been run successfully end-to-end with a real API key (not just the fallback) — a real `source: llm` report was generated and its specific claims (three weakest categories, the one occupation meaningfully below the others) were checked line-by-line against the actual scored JSON and confirmed accurate, not just plausible-sounding text.

If the LLM call doesn't reach the API live on demo day, the script's own fallback produces a templated report from the same real data — that's documented behavior, not a crash (see `demo_backup_plan.md`). You also have a saved copy of a verified real run as backup evidence if needed.

---

## Note on the rubric's "Critical Thinking & Ethics" row

This is intentionally left for you to answer live, not scripted here — but factual material you could draw from if useful:

- The expert-vs-classifier kappa check (Example C) is a real, honest limitation surfaced by your own testing, not hidden — a good candidate for "a place it could fail."
- That comparison is *not* the same as a true inter-rater reliability check (two independent humans agreeing on the taxonomy's boundaries) — a coding manual and kappa calculator exist for that, but a second human rater hasn't been recruited yet. Worth naming as "what I'd revisit with more time" if asked.
- `hardware_physical_infra` remained relatively weak through all three corrections, because only one course (NOS-110) touches it directly — a real, non-artifact curriculum gap, distinct from all three fixes above.
- The O*NET job-side data is still search-based rather than pulled from O*NET's structured API — a known, named limitation with a concrete next step already built (`onet_client.py`), just not yet run.
