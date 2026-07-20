"""
O*NET Web Services API client (v2.0)

Replaces the manual web-search approach used earlier in this project with
real, structured, repeatable O*NET data: Tasks, Technology Skills, Skills,
and Knowledge -- each with standardized importance scores, not just task
sentences pulled from search snippets.

Setup:
    1. Sign up for a free developer account: https://services.onetcenter.org/developer/signup
    2. Set credentials as environment variables:
        export ONET_USERNAME=your_username
        export ONET_PASSWORD=your_password
    (O*NET Web Services uses HTTP Basic Auth with the username/password
    issued at signup -- confirm this against your account's specific
    instructions page after signing up, since account-specific setup notes
    sometimes vary.)

Usage:
    python3 onet_client.py                  # fetch data for the 5 occupations already in this pipeline
    python3 onet_client.py 15-1244.00        # fetch data for a specific O*NET-SOC code
"""

import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE = Path(__file__).parent
load_dotenv(BASE / ".env")  # loads ONET_USERNAME/ONET_PASSWORD from a local .env file if present

API_ROOT = "https://api-v2.onetcenter.org"

# Optional: hardcode credentials here instead of using environment variables or .env.
# If set, these take priority. Leave both as None to use ONET_USERNAME/ONET_PASSWORD
# from the environment or .env file instead.
HARDCODED_USERNAME = None  # e.g. "your_username"
HARDCODED_PASSWORD = None  # e.g. "your_password"

# The five occupations already used elsewhere in this pipeline
DEFAULT_OCCUPATIONS = [
    "15-1244.00",  # Network and Computer Systems Administrators
    "15-1212.00",  # Information Security Analysts
    "15-1232.00",  # Computer User Support Specialists
    "15-1241.00",  # Computer Network Architects
    "15-1299.08",  # Computer Systems Engineers/Architects
]


def get_auth():
    username = HARDCODED_USERNAME or os.environ.get("ONET_USERNAME")
    password = HARDCODED_PASSWORD or os.environ.get("ONET_PASSWORD")
    if not username or not password:
        raise RuntimeError(
            "No credentials found. Either set HARDCODED_USERNAME/HARDCODED_PASSWORD "
            "near the top of this script, or set ONET_USERNAME and ONET_PASSWORD as "
            "environment variables / in a .env file. "
            "Sign up at https://services.onetcenter.org/developer/signup to get credentials."
        )
    return (username, password)


def fetch_all_pages(endpoint, auth, item_key):
    """O*NET paginates results (start/end params). Fetch every page and
    concatenate results, since occupations can have 15-30+ items per section."""
    results = []
    start = 1
    page_size = 20
    while True:
        url = f"{API_ROOT}{endpoint}?start={start}&end={start + page_size - 1}"
        resp = requests.get(url, auth=auth, headers={"Accept": "application/json"}, timeout=30)
        if resp.status_code == 401:
            raise RuntimeError("Authentication failed -- check ONET_USERNAME/ONET_PASSWORD.")
        if resp.status_code == 422:
            raise RuntimeError(f"O*NET API error: {resp.json().get('error', resp.text)}")
        resp.raise_for_status()
        data = resp.json()
        items = data.get(item_key, [])
        results.extend(items)
        total = data.get("total", len(results))
        if start + page_size - 1 >= total or not items:
            break
        start += page_size
        time.sleep(0.2)  # be polite to the API
    return results


def fetch_occupation_data(soc_code, auth):
    """Fetch Tasks, Technology Skills, Skills, and Knowledge for one occupation."""
    print(f"  fetching {soc_code}...")

    tasks = fetch_all_pages(f"/online/occupations/{soc_code}/details/tasks", auth, "task")
    tech_skills = fetch_all_pages(f"/online/occupations/{soc_code}/details/technology_skills", auth, "category")
    skills = fetch_all_pages(f"/online/occupations/{soc_code}/details/skills", auth, "element")
    knowledge = fetch_all_pages(f"/online/occupations/{soc_code}/details/knowledge", auth, "element")

    # occupation title comes from the overview endpoint
    overview_resp = requests.get(
        f"{API_ROOT}/online/occupations/{soc_code}/",
        auth=auth, headers={"Accept": "application/json"}, timeout=30,
    )
    overview_resp.raise_for_status()
    title = overview_resp.json().get("title", soc_code)

    return {
        "soc_code": soc_code,
        "title": title,
        "tasks": [t["title"] for t in tasks],
        "tasks_detail": tasks,  # keeps importance/category scores for future weighting
        "technology_skills": [
            {"category": cat.get("title", {}).get("name", ""), "examples": [e.get("name", "") for e in cat.get("example", [])]}
            for cat in tech_skills
        ],
        "skills": [{"name": s.get("element", {}).get("name", s.get("name", "")), "importance": s.get("score", {}).get("value")} for s in skills],
        "knowledge": [{"name": k.get("element", {}).get("name", k.get("name", "")), "importance": k.get("score", {}).get("value")} for k in knowledge],
    }


def main():
    try:
        auth = get_auth()
    except RuntimeError as e:
        print(f"Setup needed: {e}")
        sys.exit(1)

    soc_codes = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_OCCUPATIONS

    print(f"Fetching O*NET data for {len(soc_codes)} occupation(s)...")
    occupations = []
    for soc_code in soc_codes:
        try:
            occupations.append(fetch_occupation_data(soc_code, auth))
        except Exception as e:
            print(f"  FAILED for {soc_code}: {e}")

    output = {
        "source": "O*NET Web Services API v2.0 (services.onetcenter.org), fetched live",
        "occupations": occupations,
    }

    out_path = BASE / "onet_requirements_v2.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved {len(occupations)} occupation(s) to {out_path}")
    print("Review this against onet_requirements.json (the search-based version) before switching the pipeline over.")


if __name__ == "__main__":
    main()
