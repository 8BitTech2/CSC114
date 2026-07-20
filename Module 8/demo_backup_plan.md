# Live Demo Backup Plan

## Before class
- Have `ftcc_readiness_dashboard_v2.html` already open in a browser tab (minimized, ready to switch to).
- Have a saved copy of `gap_report.json` from a known-good run — printed, or open in a second tab/text editor — as a comparison point if the live run looks different.
- Run `python3 agent.py` on the actual demo machine at least once beforehand, start to finish, not just the API connectivity check.

## Failure point 1 — `agent.py` won't run at all (missing file, import error, crash)
**What to show:** Switch to the already-open dashboard tab.
**What to say:** "The live run isn't cooperating right now — here's the dashboard from my last successful run, showing the actual scored output," then walk through it.

## Failure point 2 — pipeline runs, but the LLM call fails (network, rate limit, etc.)
**What to show:** The script's own fallback output — it will print `report_source: template` instead of `llm` in `gap_report.json`, and still produce a real report from the same scored data.
**What to say:** "The LLM step didn't reach the API this time — that's a built-in fallback in my code, not a crash. Here's the templated version it produced instead, using the same real scored data." This demonstrates working error handling, not failure.

## Failure point 3 — everything runs, but numbers/report differ from rehearsal
**What to do:** Don't panic-explain. State what you expected, then state what happened, and compare against the saved known-good `gap_report.json`.
**What to say:** "I expected [X] — let's see what it says this time," then read the actual output and note the difference honestly.

## General principle
If something breaks live, talking through what you expected to happen and why is a legitimate part of the demo — the rubric explicitly says so ("if something breaks live, talk through what you expected to happen — that's still a legitimate part of the demo").
