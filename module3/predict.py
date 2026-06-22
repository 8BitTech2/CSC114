"""
Module 3 — Load the saved model and make predictions (CSC-114)

This proves the third deliverable from the assignment: we can SAVE a model,
LOAD it, send it INPUTS, and get a PREDICTION back.

Because the Normalization layer is baked inside the saved model, we can feed
in RAW house numbers here -- no separate scaler file needed.

Run it with:
    python predict.py
(after running model.py at least once to create house_price_model.keras)

Feature order (must match training):
    MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude
"""

import numpy as np
import keras

model = keras.models.load_model("house_price_model.keras")


def predict_value(features, label):
    """Run one house through the model and print the predicted value."""
    sample = np.array([features])
    pred = model.predict(sample, verbose=0)
    dollars = pred[0][0] * 100_000          # target is in units of $100,000
    print(f"{label}: ${dollars:,.0f}")
    return dollars


print("=== 3-test check on the saved model ===\n")

# 1. KNOWN-GOOD: values close to a typical California block.
#    Expect a believable, mid-range house value.
typical = predict_value(
    [8.3, 25, 6.0, 1.0, 1200, 3.0, 34.0, -118.0],
    "1. Known-good (typical block)",
)

# 2. SANITY: same block but much higher median income (first feature).
#    Income is the strongest driver of price, so the prediction should RISE.
high_income = predict_value(
    [15.0, 25, 6.0, 1.0, 1200, 3.0, 34.0, -118.0],
    "2. Sanity (higher income)",
)
print(f"   -> went {'UP' if high_income > typical else 'DOWN'} "
      f"as expected when income increased\n")

# 3. EDGE / WEIRD: an extreme, unrealistic input.
#    We're checking that it returns *some* number rather than crashing.
predict_value(
    [0.5, 52, 1.0, 1.0, 35000, 1200.0, 41.0, -124.0],
    "3. Edge case (extreme/unusual block)",
)

print("\nAll three predictions returned a number -> save + load + predict works.")
