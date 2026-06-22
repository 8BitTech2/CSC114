"""
Module 3 — Build a Small Keras Model (CSC-114)

A small REGRESSION model on the California Housing dataset.
It predicts the median house value of a neighborhood block -- a NUMBER --
so this is regression (not classification).

The whole script follows the learning loop from the reading:
    feed data -> predict -> measure loss -> compute gradient -> update weights
...repeated for many passes (epochs) until the loss stops improving.

Run it with:
    pip install tensorflow scikit-learn
    python model.py
"""

import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
import keras
from keras import layers


# ---------------------------------------------------------------------------
# 1. FEED DATA
#    California Housing ships with scikit-learn and is already clean, so we
#    don't have to do any messy data cleaning ourselves.
# ---------------------------------------------------------------------------
data = fetch_california_housing()
X = data.data            # 8 numeric features describing each block
y = data.target          # target: median house value, in units of $100,000

print("Features:", data.feature_names)
print(f"Dataset shape: {X.shape[0]} rows, {X.shape[1]} features")

# Hold back 20% of the data the model never sees during training, so we can
# honestly measure how well it does on brand-new houses.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ---------------------------------------------------------------------------
# 2. BUILD THE MODEL
#    Putting a Normalization layer INSIDE the model is the important trick:
#    the 8 features live on very different scales (income vs. latitude vs.
#    population). Normalizing makes training stable, and because the scaling
#    is baked into the saved model, predict.py can feed in RAW house numbers
#    later with no separate scaler file to worry about.
# ---------------------------------------------------------------------------
normalizer = layers.Normalization()
normalizer.adapt(X_train)          # learns the mean/variance of each feature

model = keras.Sequential([
    keras.Input(shape=(X_train.shape[1],)),   # 8 inputs in
    normalizer,                                # scale them
    layers.Dense(64, activation="relu"),       # hidden layer
    layers.Dense(64, activation="relu"),       # hidden layer
    layers.Dense(1),                           # ONE number out -> regression
])

# 3. COMPILE -- the two "dials" from the reading:
#    optimizer = HOW the weights get updated (Adam: adaptive, reliable default)
#    loss      = WHAT we are minimizing (MSE: standard for predicting numbers)
#    metrics   = a human-friendly extra score (MAE = average dollars we miss by)
model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])
model.summary()


# ---------------------------------------------------------------------------
# 4. TRAIN
#    EarlyStopping watches the validation loss and stops once it stops
#    improving, then restores the best weights. This answers the "how many
#    epochs did it really take?" question honestly -- not just the 100 we set.
# ---------------------------------------------------------------------------
early_stop = keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=10, restore_best_weights=True
)

history = model.fit(
    X_train, y_train,
    validation_split=0.2,    # carve a validation slice out of the training data
    epochs=100,              # an upper limit; EarlyStopping usually ends sooner
    batch_size=32,
    callbacks=[early_stop],
    verbose=1,
)

# Report the epoch where the model was actually at its best.
best_epoch = int(np.argmin(history.history["val_loss"])) + 1
print(f"\nBest epoch (lowest validation loss): {best_epoch}")


# ---------------------------------------------------------------------------
# 5. CHECK on the held-out test set (data the model never trained on).
# ---------------------------------------------------------------------------
test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
print(f"Test loss (MSE): {test_loss:.4f}")
print(f"Average miss (MAE): about ${test_mae * 100_000:,.0f}")


# ---------------------------------------------------------------------------
# 6. SAVE the trained model so predict.py can load it later.
# ---------------------------------------------------------------------------
model.save("house_price_model.keras")
print("\nSaved house_price_model.keras")
