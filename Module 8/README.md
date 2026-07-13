# C2C Gap Analyzer Agent

An AI agent that analyzes how well a community college curriculum (FTCC's Cloud Management AAS, A25590U) prepares students for real entry-level cloud infrastructure and data center jobs, and generates a natural-language gap report with recommendations.

## What it does

1. Loads real course descriptions (FTCC Cloud Management AAS, NCCCS-standardized text) and real O*NET occupational task data for five relevant occupations.
2. Classifies both against a 9-category skill taxonomy (virtualization, networking, cloud platforms, storage, security/compliance, scripting/automation, monitoring & troubleshooting, hardware/physical infrastructure, ITIL & soft skills) using a TF-IDF + OneVsRest LogisticRegression classifier.
3. Scores curriculum coverage and per-occupation readiness, normalized against the dataset's own achievable ceiling.
4. Calls the Anthropic API (Claude) to turn the scored data into a plain-language gap report with specific recommendations.

## Files

| File | Purpose |
|---|---|
| `curriculum_courses.json` | Real FTCC AAS course data (15 courses) |
| `onet_requirements.json` | Real O*NET task/technology data for 5 occupations |
| `skill_taxonomy.json` | 9-category skill taxonomy with course/certification/occupation crosswalks |
| `apply_taxonomy.py` | Steps 1-4: data loading, classifier training, gap scoring |
| `agent.py` | Step 5: orchestrates the pipeline and calls Claude for the natural-language report |
| `ftcc_readiness_dashboard_v2.html` | Standalone interactive dashboard (self-contained, no server needed) |
| `gap_analysis_results.json` / `gap_report.json` | Sample output from the last run |

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
