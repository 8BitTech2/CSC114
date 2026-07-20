"""
Inter-rater reliability calculator for the skill taxonomy coding manual.

Computes Cohen's kappa per category, comparing two independent raters'
Yes/No codes on the same sample of documents, plus a macro-average kappa
across all categories.

Input format: a CSV with columns:
    doc_id, category, rater1, rater2

Where rater1/rater2 are "Yes" or "No" (case-insensitive). One row per
document per category -- so if you coded 20 documents against all 9
categories, you'll have 180 rows.

A template CSV is generated if none exists, so you can see the expected
format and fill it in with real data.

Usage:
    python3 compute_kappa.py rater_codes.csv
"""

import csv
import sys
from collections import defaultdict


def cohens_kappa(rater1_labels, rater2_labels):
    """Standard Cohen's kappa for two raters' binary (Yes/No) codes."""
    n = len(rater1_labels)
    if n == 0:
        return None

    agree = sum(1 for a, b in zip(rater1_labels, rater2_labels) if a == b)
    po = agree / n  # observed agreement

    r1_yes = sum(1 for x in rater1_labels if x == "yes") / n
    r1_no = 1 - r1_yes
    r2_yes = sum(1 for x in rater2_labels if x == "yes") / n
    r2_no = 1 - r2_yes

    pe = (r1_yes * r2_yes) + (r1_no * r2_no)  # expected agreement by chance

    if pe == 1.0:
        return 1.0 if po == 1.0 else 0.0

    kappa = (po - pe) / (1 - pe)
    return kappa


def interpret(kappa):
    if kappa is None:
        return "N/A (no data)"
    if kappa < 0:
        return "poor (worse than chance)"
    if kappa < 0.2:
        return "slight"
    if kappa < 0.4:
        return "fair"
    if kappa < 0.6:
        return "moderate"
    if kappa < 0.8:
        return "substantial"
    return "near-perfect"


TEMPLATE_ROWS = [
    ["doc_id", "category", "rater1", "rater2"],
    ["CTI-141", "cloud_platforms", "Yes", "Yes"],
    ["CTI-141", "virtualization", "No", "No"],
    ["CTI-240", "virtualization", "Yes", "Yes"],
    ["CTI-240", "cloud_platforms", "Yes", "No"],
]


def write_template(path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(TEMPLATE_ROWS)
    print(f"No input file found. Wrote a template to: {path}")
    print("Fill it in with your two raters' actual codes, then rerun this script on it.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 compute_kappa.py rater_codes.csv")
        write_template("rater_codes_template.csv")
        return

    path = sys.argv[1]
    try:
        f = open(path)
    except FileNotFoundError:
        write_template(path)
        return

    reader = csv.DictReader(f)
    by_category = defaultdict(lambda: {"rater1": [], "rater2": []})

    for row in reader:
        cat = row["category"].strip()
        r1 = row["rater1"].strip().lower()
        r2 = row["rater2"].strip().lower()
        by_category[cat]["rater1"].append(r1)
        by_category[cat]["rater2"].append(r2)

    f.close()

    print(f"{'Category':<28} {'N':>5} {'Kappa':>8}  Interpretation")
    print("-" * 70)

    kappas = []
    for cat in sorted(by_category.keys()):
        r1 = by_category[cat]["rater1"]
        r2 = by_category[cat]["rater2"]
        k = cohens_kappa(r1, r2)
        if k is not None:
            kappas.append(k)
        k_str = f"{k:.3f}" if k is not None else "N/A"
        print(f"{cat:<28} {len(r1):>5} {k_str:>8}  {interpret(k)}")

    if kappas:
        macro_avg = sum(kappas) / len(kappas)
        print("-" * 70)
        print(f"{'MACRO AVERAGE':<28} {'':>5} {macro_avg:>8.3f}  {interpret(macro_avg)}")
        print()
        print("Categories with kappa below 0.6 need review per the coding manual's")
        print("'After coding: what to do with disagreements' section.")


if __name__ == "__main__":
    main()
