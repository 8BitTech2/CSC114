# C2C Gap Analyzer Agent

An AI agent that analyzes how well a community college curriculum (FTCC's Cloud Management AAS, A25590U) prepares students for real entry-level cloud infrastructure and data center jobs, and generates a natural-language gap report with recommendations.

## What it does

1. Loads real course descriptions (FTCC Cloud Management AAS, NCCCS-standardized text) and real O*NET occupational task data for five relevant occupations.
2. Classifies both against a 9-category skill taxonomy (virtualization, networking, cloud platforms, storage, security/compliance, scripting/automation, monitoring & troubleshooting, hardware/physical infrastructure, ITIL & soft skills) using a TF-IDF + OneVsRest LogisticRegression classifier.
3. Scores curriculum coverage and per-occupation readiness, normalized against the dataset's own achievable ceiling.
4. Calls the Anthropic API (Claude) to turn the scored data into a plain-language gap report with specific recommendations.

## Repo contents

**Essential — the pipeline itself**
- `agent.py`
- `apply_taxonomy.py`
- `onet_client.py`
- `curriculum_courses.json`
- `onet_requirements.json`
- `skill_taxonomy.json`
- `courses_aligned_with_pillars.xlsx`
- `requirements.txt`

**Essential — proof it works**
- `gap_analysis_results.json`
- `gap_report.json`
- `ftcc_readiness_dashboard_v2.html`

**Essential — documentation and validity evidence** (this is what makes the "Critical Thinking" and "Problem-Solving Process" story checkable by someone reading the repo, not just watching a demo)
- `README.md` (this file)
- `skill_taxonomy_expanded_table.md`
- `taxonomy_coding_manual.md`
- `compute_kappa.py`
- `2025SU_IT_CROSSWALK.pdf`

**Demo prep** (optional, but useful if the repo should double as demo material)
- `demo_presentation.html`
- `demo_talking_points_reference.md`
- `demo_backup_plan.md`
- `setup_check.bat`

**Not included / excluded on purpose**
- `skill_taxonomy_v1_backup.json`, `skill_taxonomy_v2.json` — superseded working versions; `git log` preserves this history once committed, so no need to keep dead files around
- `.env` — excluded via `.gitignore`; holds real credentials and must never be committed

## O*NET data: two versions

`onet_requirements.json` was built from manual web searches -- readable, but not repeatable or complete. `onet_client.py` replaces this with the real O*NET Web Services API (structured Tasks, Technology Skills, Skills, and Knowledge, each with standardized importance scores).

To use it:
```bash
export ONET_USERNAME=your_username     # from https://services.onetcenter.org/developer/signup
export ONET_PASSWORD=your_password
python3 onet_client.py
```
This writes `onet_requirements_v2.json`. Review it against `onet_requirements.json` before switching the pipeline over to the new source -- the pipeline currently reads `onet_requirements.json` by default, so this is a deliberate, reviewable swap, not automatic.

## Setup

```bash
pip install -r requirements.txt
```

Set your Anthropic API key (required for the LLM-generated report; without it the agent falls back to a templated report):

```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here      # macOS/Linux
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"       # Windows PowerShell
```

## Run

```bash
python3 agent.py
```

This runs the full pipeline (data load → classify → score) and prints a gap report to the terminal, then writes `gap_analysis_results.json` and `gap_report.json`.

To view the dashboard, just open `ftcc_readiness_dashboard_v2.html` in a browser.

## Known limitations

- The skill taxonomy's keyword lists and category boundaries are single-author and have not been reviewed by a second rater.
- Course/O*NET classification is a small-N weak-labeled model, not a validated instrument. `class_weight="balanced"` was required in the classifier to avoid rare-category underweighting (see commit history) — worth checking for similar issues if new categories or documents are added.
- Course descriptions were pulled from other NC community colleges' catalogs (NCCCS-standardized, identical statewide) because FTCC's own catalog PDFs have a font-encoding bug that corrupts text extraction.
