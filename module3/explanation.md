# Module 3 — Model Explanation (CSC-114)

> **NOTE TO SELF:** This is a draft with the real numbers from my run. The
> grade is on explaining this *in my own words*, so I should reword each
> answer in my own voice before submitting. The numbers and facts below are
> correct for my run.

## What I built
A small Keras neural network that predicts the **median house value** of a
California neighborhood block from the California Housing dataset (which ships
with scikit-learn, already cleaned).

---

### 1. What are the attributes (features) of the dataset, and what is the target?
The dataset has **8 input features**, all numbers describing a block of houses:

| Feature | Meaning |
|---|---|
| MedInc | median income of the block |
| HouseAge | median house age |
| AveRooms | average rooms per household |
| AveBedrms | average bedrooms per household |
| Population | block population |
| AveOccup | average household occupancy |
| Latitude | location (N/S) |
| Longitude | location (E/W) |

The **target** is the **median house value**, reported in units of $100,000
(so a target of `2.5` means about $250,000).

### 2. Is the model regression or classification?
**Regression.** The target is a continuous number (a dollar value), not a fixed
category. The giveaways in the code: the final layer is `Dense(1)` (one number
out) and the loss is `mean_squared_error`. A classification model would instead
end in `Dense(num_classes, activation="softmax")` and use a cross-entropy loss.

### 3. What optimizer trained the model, and why?
**Adam.** An optimizer is the rule for *how* the model adjusts its weights after
each batch to shrink the loss. Adam adapts the step size for each weight
automatically and includes momentum, so it trains reliably without me having to
hand-tune a learning rate. It's the standard, dependable default — that's why I
picked it over plain SGD.

### 4. About how many epochs did it take to reach the best result?
I set an upper limit of **100 epochs** but used an `EarlyStopping` callback that
watches the validation loss. Training actually ran **59 epochs**, and the lowest
validation loss was at **epoch 49** — EarlyStopping then restored the weights
from that best epoch. So the honest answer is **~49 epochs**; the extra 10 were
just confirming it had stopped improving. (Reading the curve instead of trusting
the number I set is the point here.)

### 5. What was the lowest loss the model reached?
On the held-out **test set** (data it never trained on):
- **Test loss (MSE): 0.2672**
- Average miss (MAE): about **$34,670**

The MSE of 0.2672 is in units of (×$100,000)², which is hard to read directly —
that's why I also report MAE, which says the model is off by about $35k on a
typical prediction.

### 6. Can I save the model, send it inputs, and get a prediction? (Yes — proof)
`model.py` saves the trained model with `model.save("house_price_model.keras")`.
`predict.py` loads it with `keras.models.load_model(...)` and runs my 3-test check:

| Test | Input idea | Predicted value |
|---|---|---|
| Known-good | a typical block | **$388,436** |
| Sanity | same block, higher income | **$443,076** (went UP, as expected) |
| Edge case | extreme/unrealistic block | **$355,312** (didn't crash) |

The sanity test is the important one: raising the income feature pushed the
predicted price up, which matches real life — confirming the model learned a
sensible relationship, not noise.

---

## Bonus — one thing the AI got wrong / I had to check
A couple of honest catches from this build:

1. **The loss number isn't in dollars.** It would be easy to report "loss =
   0.2672" and imply the model is off by 27 cents. It isn't — MSE is in squared
   units of $100k. I added the MAE metric so I had a number I could actually
   explain ("off by ~$35k").

2. **My edge-case prediction barely moved.** The extreme/unrealistic block
   ($355k) came out *lower* than the typical one, even though I made several
   features huge. That's a real limitation: the model only learned the range of
   normal California blocks and doesn't extrapolate well to crazy inputs. Good to
   know the model's prediction is only trustworthy inside the kind of data it
   was trained on.

3. **"50 epochs" in the starter prompt was arbitrary.** Rather than trust a
   fixed number, I let EarlyStopping find that the real best point was epoch 49.
   That changed my answer to Q4 from a guess into something I measured.
