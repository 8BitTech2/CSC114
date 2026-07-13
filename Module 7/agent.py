"""
C2C Gap Analyzer Agent - step 5 (agent orchestration)

Wraps the existing pipeline (fetch data -> extract -> classify -> score) and
adds an LLM call that turns the structured gap-analysis numbers into a
natural-language gap report with specific, targeted recommendations -
fulfilling the "full agent: LLM-orchestrated loop with dynamic
recommendations" scope decision.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python3 agent.py

If no API key is set, the agent still runs the full data pipeline and falls
back to a templated (non-LLM) report so the rest of the pipeline can be
verified independently of API access.
"""

import json
import os
from pathlib import Path

import requests

from apply_taxonomy import run_gap_analysis

BASE = Path(__file__).parent
MODEL = "claude-sonnet-4-6"


def call_claude(prompt: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": MODEL,
            "max_tokens": 1500,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return "".join(block["text"] for block in data["content"] if block["type"] == "text")


def build_prompt(results: dict) -> str:
    return f"""You are assisting with a curriculum-to-career gap analysis for FTCC's
Cloud Management AAS program (A25590U). Below is structured readiness-score
output (0-100 scale, normalized against the dataset's achievable ceiling) per
skill category, for five relevant O*NET occupations, plus overall curriculum
coverage per category.

DATA:
{json.dumps(results, indent=2)}

Write a concise gap report with:
1. A 2-3 sentence overall summary of curriculum strength/weakness.
2. The 3 weakest skill categories curriculum-wide, with a one-sentence,
   specific, actionable recommendation for each (e.g. name a tool, lab
   activity, or course modification - not generic advice).
3. Any occupation where overall_readiness is notably lower than the others,
   and why that might be (tie it to specific category gaps).

Keep it under 300 words. Do not repeat the raw numbers back verbatim; write
in plain prose a program coordinator could put directly into a report."""


def generate_templated_fallback(results: dict) -> str:
    """Non-LLM fallback: still real, still derived from the data, just
    template-based instead of model-generated prose."""
    cov = results["curriculum_coverage"]
    weakest = sorted(cov.items(), key=lambda kv: kv[1])[:3]
    lowest_occ = min(results["occupations"], key=lambda o: o["overall_readiness"])

    lines = ["GAP REPORT (templated fallback - no ANTHROPIC_API_KEY set)\n"]
    lines.append(
        f"Curriculum coverage is uneven across the taxonomy: strongest in "
        f"networking ({cov.get('networking', 0)}) and security/compliance "
        f"({cov.get('security_compliance', 0)}), weakest in the categories below.\n"
    )
    lines.append("Weakest categories curriculum-wide:")
    for cat, score in weakest:
        lines.append(f"  - {cat}: {score}/100 -- recommend targeted lab coverage or a dedicated module.")
    lines.append(
        f"\nLowest-readiness occupation: {lowest_occ['title']} "
        f"({lowest_occ['overall_readiness']}/100 overall) - "
        f"driven by low scores in: " +
        ", ".join(
            f"{k} ({v})" for k, v in sorted(
                lowest_occ["readiness_by_category"].items(), key=lambda kv: kv[1]
            )[:2]
        )
    )
    return "\n".join(lines)


def run_agent():
    print("[agent] Step 1-4: running data pipeline (fetch -> extract -> classify -> score)...")
    results = run_gap_analysis()

    print("[agent] Step 5: generating gap report with recommendations...")
    try:
        prompt = build_prompt(results)
        report = call_claude(prompt)
        source = "llm"
    except Exception as e:
        print(f"[agent] LLM call unavailable ({e}); using templated fallback.")
        report = generate_templated_fallback(results)
        source = "template"

    output = {"report_source": source, "report": report, "data": results}
    with open(BASE / "gap_report.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n=== GAP REPORT (source: {source}) ===\n")
    print(report)
    return output


if __name__ == "__main__":
    run_agent()
