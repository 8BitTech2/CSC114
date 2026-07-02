# Code Walkthrough — How This Model Works

*A guided tour of `model.py` and `predict.py` for someone who has learned the
core machine-learning ideas (features, target, the training loop) and now wants
to understand exactly what each part of the program is doing and why.*

---

## The big picture in one paragraph

We have a table of California neighborhoods. For each neighborhood we know 8
facts (income, house age, location, etc.) and the thing we want to predict: the
median house value. We're going to build a small **neural network** that learns
the relationship "given these 8 facts → guess the price," train it by showing it
thousands of real examples, check how good it got, and save it so we can ask it
about new houses later. That's the entire program.

The training itself is the loop you've already met:

```
feed data → make a prediction → measure how wrong it was (loss)
          → figure out which direction to nudge the weights (gradient)
          → update the weights → repeat
```

Everything below is just the machinery that makes that loop run.

---

## Part 1 — `model.py`, step by step

### The imports

```python
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
import keras
from keras import layers
```

- **`numpy`** — the standard library for number arrays. Neural networks eat
  arrays of numbers, not Python lists, so we use this for any hand-built input.
- **`sklearn.datasets`** — scikit-learn ships with several clean, ready-to-use
  datasets. `fetch_california_housing` is one of them. "Clean" matters: we don't
  have to fix missing values or junk data, which is half the work in real ML.
- **`train_test_split`** — a helper that splits our data into a *training* pile
  and a *testing* pile (more on why below).
- **`keras` / `layers`** — Keras is the library we use to describe and train the
  network. `layers` holds the building blocks (Dense, Normalization, …).

### Step 1 — Load the data and split it

```python
data = fetch_california_housing()
X = data.data            # the 8 input features
y = data.target          # the answer we want to predict

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

By convention, **`X`** is the inputs (the "questions") and **`y`** is the target
(the "answers"). `X` here is a 20,640 × 8 grid — 20,640 neighborhoods, 8 numbers
each. `y` is a list of 20,640 prices.

**Why split into train and test?** If you study for an exam using the exact
questions that will be on it, a high score doesn't prove you learned anything —
you just memorized. Same with models. So we hide 20% of the data
(`test_size=0.2`) and *never* train on it. At the end we test on that hidden 20%
to get an honest measure of how the model does on neighborhoods it has never
seen. This is how we catch **overfitting** (memorizing instead of learning).

`random_state=42` just makes the random split reproducible — run it twice, get
the same split, so your results don't wobble for no reason.

### Step 2 — Build the model

```python
normalizer = layers.Normalization()
normalizer.adapt(X_train)

model = keras.Sequential([
    keras.Input(shape=(X_train.shape[1],)),   # 8 numbers in
    normalizer,                                # scale them
    layers.Dense(64, activation="relu"),
    layers.Dense(64, activation="relu"),
    layers.Dense(1),                           # 1 number out
])
```

A **`Sequential`** model is just a stack of layers — data flows top to bottom,
each layer feeding the next.

**The Normalization layer (the important trick).** Look at the raw features:
income might be `8.3`, population might be `1200`, latitude is `34.0`. Those live
on wildly different scales. A network trains badly when one input is in the
thousands and another is near zero, because the big numbers drown out the small
ones. Normalization rescales every feature to roughly the same range (mean 0,
spread 1). `adapt(X_train)` is the step where it *measures* the average and
spread of each column so it knows how to rescale.

**Why put it *inside* the model?** We could scale the data outside the model
before training — but then we'd have to remember to do the exact same scaling
by hand every time we make a prediction later. Bake it into the model instead,
and the saved model accepts raw house numbers directly. (This is the single most
common beginner bug: scale during training, forget to scale at prediction time,
and every prediction comes out nonsense.)

**The Dense layers.** A `Dense` layer is a set of "neurons," each of which mixes
all its inputs together with learned weights. `Dense(64)` means 64 neurons.
Stacking two of them lets the model learn non-linear patterns — like "price
depends on income *and* location *together*," not just each one separately.

**`activation="relu"`.** Without an activation function, stacking layers would
just collapse into one big straight-line formula and the model couldn't learn
curves. ReLU ("keep positive numbers, zero out negatives") is the simple, cheap
function that lets the network bend and capture complex relationships.

**The final `Dense(1)`.** This is the answer layer. **One** output, with **no**
activation, because we want a single raw number (a price). *This line is what
makes it regression.* If this were classification, this layer would instead have
one output per category and a `softmax` activation to turn them into
probabilities.

### Step 3 — Compile (set the two "dials")

```python
model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])
```

Compiling tells Keras *how* to train. Three settings:

- **`loss="mean_squared_error"` (MSE)** — the loss is the score the model is
  trying to make as small as possible. MSE = average of (prediction − truth)².
  Squaring does two things: it makes all errors positive, and it punishes big
  misses much harder than small ones. MSE is the standard loss for predicting a
  number.
- **`optimizer="adam"`** — the optimizer is the *strategy* for adjusting the
  weights to lower the loss. After each batch it asks "which way, and how far,
  should I nudge each weight?" Adam adjusts the step size for each weight
  automatically and adds "momentum" so it doesn't get stuck. It's the reliable
  default that works without hand-tuning, which is exactly why we chose it over
  plain gradient descent (SGD).
- **`metrics=["mae"]`** — a metric is an extra score we watch for our own
  benefit; it doesn't affect training. MAE (mean absolute error) is just the
  average miss in plain units. We track it because "off by $35,000" is something
  a human can understand, whereas the MSE number is in squared dollars and is
  hard to interpret.

### Step 4 — Train

```python
early_stop = keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=10, restore_best_weights=True
)

history = model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=100,
    batch_size=32,
    callbacks=[early_stop],
    verbose=1,
)
```

`model.fit(...)` *is* the training loop. A few terms:

- **epoch** — one full pass through all the training data. `epochs=100` is an
  upper limit on how many passes we'll allow.
- **batch_size=32** — the model doesn't look at all 16,000-ish training rows at
  once; it processes them in small groups of 32, updating its weights after each
  group. Smaller batches = more frequent updates.
- **`validation_split=0.2`** — carves a *third* slice (20% of the training data)
  to check progress *during* training. Note we now have three piles: train (what
  it learns from), validation (a progress check it doesn't learn from), and test
  (the final untouched exam from Step 1).

**EarlyStopping — the smart part.** Training for a fixed 100 epochs is wasteful
and can even hurt: past a certain point the model starts memorizing the training
data and gets *worse* on new data. EarlyStopping watches the validation loss
(`monitor="val_loss"`); if it hasn't improved for 10 epochs in a row
(`patience=10`), it halts and rewinds to the best version it saw
(`restore_best_weights=True`). This is what lets us honestly answer "how many
epochs did it *really* take" instead of just trusting the number we set.

```python
best_epoch = int(np.argmin(history.history["val_loss"])) + 1
```

`history` is a record of the loss at every epoch. `np.argmin` finds the position
of the lowest validation loss — i.e., the epoch where the model was at its best.
*(In this run that was epoch 49; training ran to 59 then rewound.)*

### Step 5 — Evaluate on the hidden test set

```python
test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
```

Now we finally use `X_test`/`y_test` — the 20% the model has never touched.
`evaluate` runs those examples through and reports the loss and MAE. This is the
honest grade. *(This run: MSE 0.2672, MAE ≈ $34,670.)*

### Step 6 — Save

```python
model.save("house_price_model.keras")
```

Writes the whole trained model — its structure, its learned weights, *and* the
fitted Normalization layer — into one `.keras` file. That file is now a
self-contained predictor we can load anywhere.

---

## Part 2 — `predict.py`, step by step

This file answers the assignment's "can you save it, send it inputs, and get a
prediction?" question.

```python
model = keras.models.load_model("house_price_model.keras")
```

Loads the saved model back into memory. Because Normalization was baked in, this
loaded model takes **raw** house numbers — no extra setup.

```python
def predict_value(features, label):
    sample = np.array([features])
    pred = model.predict(sample, verbose=0)
    dollars = pred[0][0] * 100_000
    print(f"{label}: ${dollars:,.0f}")
    return dollars
```

A small helper that:
1. Wraps one house's 8 features in a numpy array. The **double brackets**
   `[features]` matter — the model expects a *batch* of rows, so even a single
   house has to be shaped as "a list containing one row."
2. Calls `model.predict(...)`, which returns the prediction (in $100k units).
3. `pred[0][0]` digs out the single number (first row, first output), then we
   multiply by 100,000 to turn it into real dollars.

### The 3-test check

This is a deliberate sanity-testing habit, not just "does it run":

1. **Known-good** — feed a typical neighborhood and confirm the price is
   believable, not absurd.
2. **Sanity** — change *one* feature in a way you can predict (raise the income),
   and confirm the output moves the right direction (price goes up). This is the
   strongest test: it shows the model learned a *real relationship*, not noise.
3. **Edge case** — feed something extreme and confirm it doesn't crash. Here it's
   also informative: the prediction barely moves for crazy inputs, which is a
   real and useful limitation to know — the model is only trustworthy *inside*
   the range of data it was trained on.

---

## Glossary (quick reference)

| Term | Plain-English meaning |
|---|---|
| **Feature** | One input fact about an example (e.g. median income) |
| **Target** | The thing we're trying to predict (the house value) |
| **Regression** | Predicting a number (vs. classification = predicting a category) |
| **Weights** | The adjustable numbers inside the model that get learned |
| **Loss** | A score of how wrong the model is; training tries to minimize it |
| **MSE** | Mean Squared Error — the loss we use; squares each miss |
| **MAE** | Mean Absolute Error — average miss in plain units, easy to read |
| **Optimizer** | The strategy for adjusting weights to lower the loss (we use Adam) |
| **Epoch** | One full pass through all the training data |
| **Batch** | A small group of examples processed together before an update |
| **Normalization** | Rescaling features to comparable ranges so training is stable |
| **Activation (ReLU)** | The bend that lets stacked layers learn non-straight-line patterns |
| **Overfitting** | Memorizing the training data instead of learning the pattern |
| **EarlyStopping** | Auto-halts training once it stops improving, keeps the best version |
| **Train / validation / test** | Learn-from / progress-check / final-honest-exam data splits |

---

## How to run it yourself

```bash
pip install tensorflow scikit-learn   # one-time setup
python model.py                       # trains and saves the model (seconds on CPU)
python predict.py                     # loads the saved model and predicts
```

If you change one thing and re-run, watch the validation loss and the test
number — that's the feedback loop that tells you whether your change helped.
