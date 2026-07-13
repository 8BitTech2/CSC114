# cloud_platforms Fix — Before/After Data

## Metrics

| Metric | Before | After |
|---|---|---|
| Curriculum coverage score (0–100 scale) | 3.5 | 34.4 |
| CTI-141 predicted probability (0–1 scale) | 0.03 | 0.89 |
| Positive training examples for this category | 1 of 74 documents | 1 of 74 documents (unchanged) |

## What changed

`class_weight="balanced"` was added to the `LogisticRegression` classifier in `apply_taxonomy.py`. No data changed — only how the classifier weighted the single positive example for this category during training.

## Note on the chart version

The visual chart shown in this conversation scales the predicted probability by ×100 (0.03 → 3, 0.89 → 89) so both metrics fit the same 0–100 axis for visual comparison. The actual predicted probability values are 0.03 and 0.89, not 3 and 89 — see the table above for the real values.
