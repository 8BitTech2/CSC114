"""
C2C Gap Analyzer - core pipeline (steps 1-4)

1. Data collection: load real FTCC curriculum course descriptions + real O*NET
   task data (both bundled locally as JSON, sourced from NCCCS Combined Course
   Library and O*NET OnLine).
2. Taxonomy: 9 skill categories (skill_taxonomy.json), matching Model_idea.docx.
3. Classification: weak-label each course/task snippet against the taxonomy via
   keyword matching, then train a TF-IDF + OneVsRestClassifier(LogisticRegression)
   multi-label model on those weak labels (mirrors the original pipeline's
   classifier choice) and use predicted probabilities for smoother scoring.
4. Gap analysis: compute per-category coverage on both curriculum and job sides,
   normalize against the dataset's achievable ceiling (not an absolute
   threshold) per the methodology fix already validated in the doctoral study,
   and produce a readiness score 0-100 per category per occupation.

Output: gap_analysis_results.json - consumed by agent.py (step 5) and by the
HTML dashboard.
"""

import json
import re
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics.pairwise import cosine_similarity

BASE = Path(__file__).parent


def load_json(name):
    with open(BASE / name) as f:
        return json.load(f)


def weak_label(text, categories):
    """Assign 0/1 labels per taxonomy category via keyword presence.
    This produces the weak/silver labels used to train the classifier,
    since no hand-labeled ground truth exists for this small-N dataset."""
    text_l = text.lower()
    labels = []
    for cat in categories:
        hit = any(re.search(r"\b" + re.escape(kw) + r"", text_l) for kw in cat["keywords"])
        labels.append(1 if hit else 0)
    return labels


def build_dataset():
    taxonomy = load_json("skill_taxonomy.json")["categories"]
    cat_ids = [c["id"] for c in taxonomy]

    curriculum = load_json("curriculum_courses.json")["courses"]
    onet = load_json("onet_requirements.json")["occupations"]

    # curriculum snippets
    curr_texts, curr_labels, curr_meta = [], [], []
    for course in curriculum:
        txt = f"{course['title']}. {course['description']}"
        curr_texts.append(txt)
        curr_labels.append(weak_label(txt, taxonomy))
        curr_meta.append({"code": course["code"], "title": course["title"]})

    # job-requirement snippets (one per task line, tagged with occupation)
    job_texts, job_labels, job_meta = [], [], []
    for occ in onet:
        for task in occ["tasks"]:
            job_texts.append(task)
            job_labels.append(weak_label(task, taxonomy))
            job_meta.append({"soc_code": occ["soc_code"], "title": occ["title"]})

    return {
        "taxonomy": taxonomy,
        "cat_ids": cat_ids,
        "curr_texts": curr_texts,
        "curr_labels": np.array(curr_labels),
        "curr_meta": curr_meta,
        "job_texts": job_texts,
        "job_labels": np.array(job_labels),
        "job_meta": job_meta,
        "onet": onet,
    }


def train_classifier(all_texts, all_labels):
    """TF-IDF + OneVsRest LogisticRegression multi-label classifier,
    matching the pipeline used in the dissertation study.

    class_weight='balanced' is required here: several taxonomy categories
    (e.g. cloud_platforms) have very few positive examples in this small-N
    dataset (as few as 1 of 74 documents). Without balancing, LogisticRegression
    underweights rare classes so heavily that even the one true positive
    example scores near-zero probability -- diagnosed directly by comparing
    per-document predicted probabilities before/after this change."""
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
    X = vectorizer.fit_transform(all_texts)
    clf = OneVsRestClassifier(LogisticRegression(max_iter=1000, class_weight="balanced"))
    clf.fit(X, all_labels)
    return vectorizer, clf


def score_coverage(vectorizer, clf, texts, cat_ids):
    """Return predicted probability matrix (n_texts x n_categories)."""
    X = vectorizer.transform(texts)
    probs = clf.predict_proba(X)
    return probs


def normalize_to_ceiling(raw_scores):
    """Normalize against the dataset's own achievable ceiling rather than an
    absolute threshold -- this is the fix already validated in the doctoral
    study after the original absolute-threshold scoring produced near-zero
    readiness scores across the board."""
    raw_scores = np.array(raw_scores, dtype=float)
    ceiling = raw_scores.max() if raw_scores.max() > 0 else 1.0
    return np.clip((raw_scores / ceiling) * 100, 0, 100)


def run_gap_analysis():
    data = build_dataset()
    cat_ids = data["cat_ids"]

    vectorizer, clf = train_classifier(
        data["curr_texts"] + data["job_texts"],
        np.vstack([data["curr_labels"], data["job_labels"]]),
    )

    curr_probs = score_coverage(vectorizer, clf, data["curr_texts"], cat_ids)
    curr_coverage_raw = curr_probs.sum(axis=0)  # total curriculum weight per category

    results = {"categories": cat_ids, "occupations": []}

    for occ in data["onet"]:
        occ_task_idx = [i for i, m in enumerate(data["job_meta"]) if m["soc_code"] == occ["soc_code"]]
        occ_texts = [data["job_texts"][i] for i in occ_task_idx]
        occ_probs = score_coverage(vectorizer, clf, occ_texts, cat_ids)
        job_demand_raw = occ_probs.sum(axis=0)  # total job-requirement weight per category

        # readiness = curriculum coverage relative to what this occupation demands,
        # normalized against the dataset's achievable ceiling (not an absolute cutoff)
        per_cat_raw = []
        for c in range(len(cat_ids)):
            demand = job_demand_raw[c]
            supply = curr_coverage_raw[c]
            if demand <= 0:
                per_cat_raw.append(0.0)
            else:
                per_cat_raw.append(min(supply / demand, 2.0))  # cap ratio before normalization

        readiness = normalize_to_ceiling(per_cat_raw)

        results["occupations"].append({
            "soc_code": occ["soc_code"],
            "title": occ["title"],
            "readiness_by_category": {cat_ids[i]: round(float(readiness[i]), 1) for i in range(len(cat_ids))},
            "overall_readiness": round(float(np.mean(readiness)), 1),
        })

    # curriculum-side coverage summary (independent of occupation) for the dashboard
    curr_cov_norm = normalize_to_ceiling(curr_coverage_raw)
    results["curriculum_coverage"] = {cat_ids[i]: round(float(curr_cov_norm[i]), 1) for i in range(len(cat_ids))}

    with open(BASE / "gap_analysis_results.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


if __name__ == "__main__":
    res = run_gap_analysis()
    print(json.dumps(res, indent=2))
