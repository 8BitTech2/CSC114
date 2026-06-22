# Build a Small Model with Claude Code in a Codespace

**CSC-114 Artificial Intelligence I · Module 3 Assess · Option 2 (Code Builders)**
*Companion to the Module 3 reading, "How Machine Learning Works." This walks you through setting up Claude Code inside a GitHub Codespace and using it to build, train, save, and explain a small Keras model.*

| Field | Value |
|---|---|
| Assignment | Module 3 Assess — **Option 2** (build a model) |
| Track | Code Builders (Prompt Masters usually pick Option 1, the cheat sheet) |
| Platform | GitHub Codespaces + Claude Code (terminal) |
| Workflow | Sacred Flow: Issue → Branch → PR → Review → Merge, into `module3/` |
| Hand in | Your `.py` file(s) **and** a text document answering the six questions |
| Time | One focused session; the tiny model trains in seconds on Codespaces CPU |

---

## What you're building, and why this way

You will build a small model that either predicts a **number** (regression) or a **category** (classification), using the Keras Python library. You'll do it inside a **Codespace** — a free cloud computer that opens in your browser — and you'll use **Claude Code**, an AI assistant that lives in the terminal and can read your files, write code, and run commands.

Here's the honest framing. Claude Code is allowed to write most of the code. That is not the test. **The test is the text document at the end**, where you explain *what the code does and why* — in your own words. If you can't explain your optimizer choice or read your own loss number, copying the code earned you nothing. So drive the agent, read every change it proposes, and make sure you understand the result.

---

## Before you start

You need three things:

1. **A GitHub account** with access to your CSC-114 repository. (You've used this since Module 1.)
2. **A way to log Claude Code in.** This is the part people miss: **the free Claude.ai plan does not include Claude Code.** You need *one* of these:
   - An **Anthropic API key** (from the Console). For this class, your instructor may give you one, or tell you how to add a small amount of credit. This is the recommended path.
   - A paid **Claude Pro or Max** subscription, which lets you log in through the browser.
3. **Codespaces hours.** Your GitHub plan includes free Codespaces hours each month (typically 60–90 with the Student Developer Pack). A tiny model uses almost none.

> If you're not sure which login you have, **ask before you start** — don't burn lab time stuck on authentication. See the escalation note at the bottom.

---

## Part 1 — Start the Sacred Flow and open a Codespace

Same workflow you've used all term. Do the GitHub bookkeeping first so your work has a home.

1. In your CSC-114 repo, **create an Issue**: *"Module 3 Option 2 — build a small Keras model."* Write one or two sentences on what you plan to predict.
2. **Create a branch** from that Issue (e.g., `12-module3-model`).
3. Click the green **Code** button → **Codespaces** tab → **Create codespace on `12-module3-model`**. A browser-based VS Code opens. This is your cloud computer.
4. In the file explorer, make a folder named **`module3/`** if it isn't there yet. Everything you build goes inside it.

You now have a terminal at the bottom of the screen. That's where Claude Code will live.

---

## Part 2 — Install Claude Code

In the Codespace terminal, use **one** of these. The native installer is simplest because it doesn't depend on Node versions.

**Option A — native installer (recommended):**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Option B — npm (Codespaces already has Node installed):**
```bash
npm install -g @anthropic-ai/claude-code
```

Then **open a new terminal tab** (so it picks up the new command) and verify:
```bash
claude --version
claude doctor
```

`claude --version` should print a version number. `claude doctor` checks your setup and tells you if anything is off — run it any time something misbehaves.

> **If `claude` isn't found:** close and reopen the terminal. If it still fails, run `claude doctor` and read what it says.

---

## Part 3 — Log Claude Code in

Pick the path that matches what you set up in "Before you start."

**Path 1 — API key as a Codespaces secret (recommended for class):**
1. On GitHub: your profile → **Settings** → **Codespaces** → **Secrets** → **New secret**.
2. Name it exactly `ANTHROPIC_API_KEY`. Paste your key as the value. Give it access to your CSC-114 repo. Save.
3. Back in the Codespace, **rebuild or restart** it (Command Palette → "Codespaces: Rebuild Container", or just stop and reopen) so the secret loads as an environment variable.
4. Run `claude`. The first time, it may ask you to confirm using the key — say yes.

This keeps your key out of your code files, where it could be exposed. **Never paste an API key into a `.py` file or commit it to GitHub.**

**Path 2 — browser login (if you have Claude Pro or Max):**
1. Run `claude`.
2. It prints a sign-in URL. Open it, log in with your paid Claude account, and authorize. The token is stored for you; you won't log in every time.

Either way, when you see Claude Code's prompt, you're connected.

---

## Part 4 — Drive the agent to build your model

Start Claude Code from inside your module folder:
```bash
cd module3
claude
```

Now you talk to it in plain English. **You decide what to build; it writes the code; you read and approve each change.** Below are starter prompts. Edit them — the more specific you are, the better the result.

**Pick a problem first.** Your model must predict either a number (regression) or a category (classification), and you must use a dataset that already exists and is clean.

> 🤖 *"I'm in CSC-114. Help me build a small Keras regression model on the California Housing dataset from scikit-learn. It predicts median house value, which is a number, so this is regression. Use the Adam optimizer and mean-squared-error loss. Put scaling inside the model with a Normalization layer so I can predict from raw inputs later. Write it to `model.py`, train for 50 epochs, print the test loss, and save the model as a `.keras` file. Explain each step in a comment as you go."*

If you'd rather do **classification**, swap in something like the Iris or Penguins dataset and predict a category instead — tell the agent to use a cross-entropy loss (e.g., `sparse_categorical_crossentropy`).

As it works:
- **Read every diff** before you accept it. If you don't understand a line, ask: *"What does this line do?"*
- **Install what you need** when it asks, or run it yourself:
  ```bash
  pip install tensorflow scikit-learn
  ```
  (`tensorflow` brings Keras with it; scikit-learn provides the clean datasets. CPU is fine.)
- **Run the file** and watch the loss drop across epochs:
  ```bash
  python model.py
  ```

When training finishes, you should see the loss get smaller over the epochs — exactly the loop from the reading: feed → predict → loss → gradient → update.

---

## Part 5 — Save it, then test the saved model

The assignment asks: *can you save your model, send it inputs, and get a prediction?* Prove it. Ask the agent for a second file:

> 🤖 *"Write `predict.py` that loads `house_price_model.keras`, feeds it one made-up house, and prints the predicted value."*

Then run your own **three-test check** — the same validation habit from earlier modules:

1. **Known-good:** feed values close to a real house in the data. Is the prediction in a believable range?
2. **Sanity:** make one feature much bigger (e.g., far more rooms). Does the prediction move the way you'd expect?
3. **Edge / weird input:** feed something extreme or unusual. Does it break, or just give a strange answer? Either is worth noting.

If something looks wrong, that's not failure — that's information. Change **one** thing, re-run, and see what happened.

---

## Part 6 — Write the text document (this is the graded part)

Create `module3/explanation.md` (or `.txt`). Answer the six questions below **in your own words.** You may ask Claude Code to explain your code first — but then close the agent and write your own version. If your wording is the agent's wording, you haven't shown understanding.

Answer all of these, plus anything else you think matters:

1. **What are the attributes (features) of your dataset, and what is the target?**
2. **Is your model regression or classification?** How do you know?
3. **What optimizer trained your model, and why that one?** (Connect it to what an optimizer actually does.)
4. **About how many epochs did it take to reach the best result?** (Look at where the loss stops improving — not just the number you set.)
5. **What was the lowest loss your model reached?** Report the actual number from your run.
6. **Can you save the model, send it inputs, and get a prediction?** Show that you did.

> One good move for the rubric: name **one thing the agent got wrong, was unsure about, or could have done better**, and say how you caught it. Quote the moment if you can. This is exactly the kind of critical check this course rewards.

---

## Part 7 — Submit through the Sacred Flow

1. Make sure these files are in `module3/`:
   - `model.py` — builds, trains, and saves the model
   - `predict.py` — loads the saved model and makes a prediction
   - your saved model file (e.g., `house_price_model.keras`)
   - `explanation.md` (or `.txt`) — the six answers
2. Commit with a clear message: *"Add Module 3 regression model and explanation (closes #12)."*
3. Open a **Pull Request**, request review per your normal process, and **merge** once approved.

**Do not commit your API key.** If you ever see it in a diff, stop and remove it before committing.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `claude: command not found` | New terminal didn't pick up the install | Close and reopen the terminal; run `claude doctor`. |
| Claude Code won't authenticate | Free plan, or key not loaded | Confirm you have a paid plan or an API key. If using a secret, rebuild the Codespace so it loads. |
| `ModuleNotFoundError: No module named 'tensorflow'` | Library not installed | `pip install tensorflow scikit-learn`, then re-run. |
| Loss is `nan` or never drops | Learning rate / data scaling issue | Keep the Normalization layer; ask the agent to lower the learning rate or check the data. Change **one** thing at a time. |
| Prediction looks absurd | Inputs not in the same shape/order as training | Match the feature order; if you scaled outside the model, scale the new input the same way. |
| Training is slow | Model or data is bigger than "small" | Shrink it. A small, clean dataset on CPU should finish fast. Only reach for Google Colab's GPU if you truly need it. |

> **Failure is exercise.** A model that won't train, a prediction that's wrong, an agent that argues with you — these are reps, not disasters. Note what you changed and what happened. That note often *is* the best answer to question 6's bonus.

---

## Two warnings worth keeping

**Cost.** Using Claude Code costs money — either per-token API usage or your subscription's limits. A tiny model is pennies, but don't leave long, rambling sessions running. Stay focused, and stop the Codespace when you're done (it also uses your hours).

**This field moves fast.** Install commands, login steps, model names, prices, and library versions in AI tooling change often. If a command here doesn't match what you see, trust the current official docs (`docs.claude.com`) and ask your instructor.

---

## Need help?

For account, access, or technical blockers that are eating your time — not ordinary trial-and-error — reach out to the course escalation contacts, **Mallory Milstead** or **Andrew Norris**, per your course materials.

---

```text
=====================================================================
INSTRUCTOR APPENDIX — not student-facing
=====================================================================

REFERENCE SOLUTION (California Housing, regression). Self-contained;
scaling lives inside the model via a Normalization layer, so the saved
model predicts from raw inputs with no external scaler file. Runs on
Codespaces CPU in seconds.

--- module3/model.py ------------------------------------------------
# Small regression model on the California Housing dataset.
# Predicts median house value (a NUMBER) -> this is REGRESSION.
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
import keras
from keras import layers

# 1. FEED DATA: a clean dataset that ships with scikit-learn.
data = fetch_california_housing()
X = data.data            # 8 features per house
y = data.target          # target: median value, in units of $100,000
print("Features:", data.feature_names)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Put scaling INSIDE the model so saved-model predictions take raw input.
normalizer = layers.Normalization()
normalizer.adapt(X_train)

# 2-3. BUILD. The two dials from the reading live in compile().
model = keras.Sequential([
    keras.Input(shape=(X_train.shape[1],)),
    normalizer,
    layers.Dense(64, activation="relu"),
    layers.Dense(64, activation="relu"),
    layers.Dense(1),                      # ONE number out -> regression
])
model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])

# 4. TRAIN: feed -> predict -> loss -> gradient -> update, repeated.
history = model.fit(
    X_train, y_train, validation_split=0.2,
    epochs=50, batch_size=32, verbose=1,
)

# 5. CHECK on data it never trained on.
test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
print(f"\nLowest test loss (MSE): {test_loss:.4f}")
print(f"Average miss (MAE): about ${test_mae*100_000:,.0f}")

# 6. SAVE.
model.save("house_price_model.keras")
print("Saved house_price_model.keras")

--- module3/predict.py ----------------------------------------------
# Load the saved model and predict from raw inputs.
import numpy as np
import keras

model = keras.models.load_model("house_price_model.keras")

# Feature order: MedInc, HouseAge, AveRooms, AveBedrms,
#                Population, AveOccup, Latitude, Longitude
sample = np.array([[8.3, 25, 6.0, 1.0, 1200, 3.0, 34.0, -118.0]])
pred = model.predict(sample, verbose=0)
print(f"Predicted median value: ${pred[0][0]*100_000:,.0f}")

--- setup -----------------------------------------------------------
pip install tensorflow scikit-learn
python model.py
python predict.py

EXPECTED ANSWERS TO THE SIX QUESTIONS
1. Features = the 8 housing attributes (MedInc, HouseAge, AveRooms,
   AveBedrms, Population, AveOccup, Latitude, Longitude). Target =
   median house value (in $100k units).
2. Regression — the target is a continuous number, not a category.
   (Reading section 4.)
3. Adam — adaptive per-parameter step sizes; the sensible default that
   trains reliably without hand-tuning a learning rate. (Reading
   section 7.) Accept SGD if the student justifies the trade-off.
4. There is no single "right" number. Strong answers read it off the
   validation-loss curve: the epoch where loss flattens / stops
   improving, not just the 50 they set. Bonus credit for mentioning
   early stopping.
5. The actual test MSE from THEIR run. The point is that they read
   their own number, not that it hits a target.
6. Yes: model.save(...keras) -> keras.models.load_model(...) ->
   model.predict(...). predict.py demonstrates it.

CATCH-THE-AI CHECK
The graded weight is explanation.md, not the code. Copy-pasted code
with a vague or agent-voiced explanation should score low on Critical
Thinking & Ethics. Reward the "where the agent was wrong / unsure"
note: students who push the agent reliably find one (a wrong loss for
the problem type, a deprecated import, a hand-wave on epochs, scaling
left out so predictions are nonsense, etc.).

RUBRIC MAPPING (four categories)
- AI Partnership Quality: drove the agent with specific prompts;
  reviewed diffs rather than blind-accepting.
- Problem-Solving Process: Issue -> branch -> PR; ran the three-test
  check on the saved model; changed one thing at a time.
- Professional Communication: clear explanation.md and PR; readable
  code comments.
- Critical Thinking & Ethics: own-words explanation; correctly read
  loss/epochs; caught/corrected an agent error; did not commit a key.

KNOWN GOTCHAS
- Scaling: if a student scales OUTSIDE the model, the saved model will
  mispredict on raw inputs. The Normalization-layer pattern above
  avoids this; if they go the external-scaler route, they must save and
  reapply the scaler (joblib) in predict.py.
- Classification path: steer toward sparse_categorical_crossentropy and
  a final Dense(num_classes, activation="softmax"); report accuracy
  alongside loss.

FAST-MOVING-TARGET — RE-VERIFY EACH TERM
- Claude Code install command and recommended method (native installer
  vs npm) and the Node 18+ requirement for npm.
- Login flow and whether the free Claude.ai plan still excludes Claude
  Code; current Pro/Max/Console pricing.
- Keras 3 / TensorFlow versions and the .keras save format.
- scikit-learn dataset availability (fetch_california_housing).
- GitHub Codespaces free-hours allotment and the Secrets UI path.

OPTIONAL: drop a .devcontainer/devcontainer.json in the repo so the
Python image and `pip install tensorflow scikit-learn` run on create,
and document the ANTHROPIC_API_KEY Codespaces secret once for the class.
=====================================================================
```
