# Chapter 3 — Frameworks, and Why Keras Is the One You Actually Learn

**CSC-114 Artificial Intelligence I · Study Notes**
*Reading: Chollet & Watson, "Introduction to TensorFlow, PyTorch, JAX, and Keras"*

---

## The one-sentence version

In Chapter 2 you built a neural network by hand to see how the gears turn. **Nobody works that way in real life.** This chapter introduces the tools real people use — and makes the case that the one tool *you* should focus on understanding is **Keras**.

If you remember one thing from this chapter, make it this:

> **Keras is the part you write. The other three frameworks are engines that run underneath it. You can swap the engine without rewriting your work.**

Everything below explains why that's true and why it matters.

---

## 1. Why frameworks exist at all

At the end of Chapter 2, you wrote your own gradient logic from scratch. That was a teaching exercise. In the real world, three jobs are too hard and too repetitive to do by hand every time:

```
   ┌──────────────────────────────────────────────────────┐
   │  Every deep learning framework does these THREE jobs:  │
   ├──────────────────────────────────────────────────────┤
   │                                                        │
   │   1. AUTODIFF                                          │
   │      Compute gradients automatically for any           │
   │      math you write. (No hand-derived calculus.)       │
   │                                                        │
   │   2. RUN ON GPUs                                       │
   │      Do tensor math fast on a graphics card, not       │
   │      just a slow CPU.                                  │
   │                                                        │
   │   3. SPREAD THE WORK                                   │
   │      Split a job across many GPUs or many computers.   │
   │                                                        │
   └──────────────────────────────────────────────────────┘
```

Those three features, packaged together, are what unlocked modern AI. The idea of automatic differentiation goes all the way back to a 1964 paper, but it took until the late 2000s — when Python got popular for science and NVIDIA's CUDA let regular GPUs run this kind of math — for the pieces to come together into reusable tools.

**Why you care:** you don't need to build any of these three things. You just need to know your framework is doing them for you.

---

## 2. A quick, painless history

You don't need to memorize dates. You just need the names to stop feeling mysterious when you see them in code, on job postings, or in research papers.

```
 2009        2015        2015        2016       2018        today
  │           │           │           │          │            │
Theano      Keras    TensorFlow    PyTorch      JAX      All four are
(the        (Mar)     (Google)     (Meta)     (Google)   alive and well.
ancestor)  high-level  big +      easy to     fastest,   "Multi-framework
           & easy     production   debug,      built for   world." Learn
                                   research-   TPUs        a bit of each.
                                   favorite
```

A few takeaways the authors are confident about:

- **Python has won.** It isn't getting replaced any time soon.
- **It's a multi-framework world.** TensorFlow, PyTorch, JAX, and Keras are all here to stay. New ones may appear (Apple's MLX, for example), but that's fine — because of point three.
- **Keras is your insurance policy.** Keras has outlived backends before. It existed *before* TensorFlow, PyTorch, and JAX. When something new comes along, Keras can usually add it as a new backend, and your old code keeps working.

---

## 3. The big picture: Keras vs. the other three

This is the heart of the chapter. Here is the mental model to lock in.

### The house metaphor (straight from the authors)

> **Keras is a prefab building kit. TensorFlow, PyTorch, and JAX are the raw lumber and concrete.**

A prefab kit gives you a clean, guided way to put a house together. The raw materials give you total freedom but make you do everything yourself. Most people want the kit.

### The stack

```
   ┌───────────────────────────────────────────────────┐
   │                                                     │
   │   KERAS  — high-level API                           │   ◄── This is what
   │   layers, models, compile(), fit(), predict()       │       YOU write.
   │                                                     │       UNDERSTAND THIS.
   ├───────────────────────────────────────────────────┤
   │                                                     │
   │   BACKEND ENGINE  — pick ONE                        │   ◄── Does the heavy
   │   ┌────────────┬───────────┬──────────────┐         │       lifting:
   │   │ TensorFlow │  PyTorch  │     JAX       │         │       tensors,
   │   └────────────┴───────────┴──────────────┘         │       gradients,
   │                                                     │       backprop.
   ├───────────────────────────────────────────────────┤
   │                                                     │
   │   HARDWARE                                          │   ◄── Where it
   │   ┌──────┬──────┬──────┐                            │       actually runs.
   │   │ CPU  │ GPU  │ TPU  │                            │
   │   └──────┴──────┴──────┘                            │
   │                                                     │
   └───────────────────────────────────────────────────┘
```

### What lives where

| Concept | Layer | Plain English |
|---|---|---|
| Tensors, variables, tensor math, backprop | **Backend** (TF / PyTorch / JAX) | The low-level machinery. |
| Layers combined into a model | **Keras** | The building blocks you snap together. |
| Loss function | **Keras** | How "wrong" the model is. |
| Optimizer | **Keras** | How the model improves. |
| Metrics (like accuracy) | **Keras** | How you measure success. |
| Training loop | **Keras** | The repeat-until-good cycle. |

### The killer feature: backends are pluggable

You can write Keras code today on one backend and switch backends later **without rewriting your model.** A common real-world workflow:

- **Debug** your model on PyTorch (easy to step through).
- **Train** it on JAX (usually fastest).
- **Deploy** it with TensorFlow's mature production tooling.

Same Keras code. Three different engines. That flexibility is *why* Keras is worth learning instead of marrying yourself to one low-level framework.

> **Note:** The default Keras backend is TensorFlow. If you just type `import keras` without changing anything, you're on TensorFlow. The authors' personal pick, if you have no preference, is **JAX** for speed.

---

## 4. The three backends at a glance

You will **not** be tested on the syntax differences between these three. The chapter shows the same little program written three times in TensorFlow, PyTorch, and JAX — and the point of doing that is *to prove they all do the same job, just with different style.* Read those sections for awareness, not memorization.

Here's the awareness-level summary — the tradeoffs, which is all you need:

| | **TensorFlow** | **PyTorch** | **JAX** |
|---|---|---|---|
| **Made by** | Google | Meta (Facebook) | Google |
| **Best at** | Production & deployment (mobile, browser) | Research, easy debugging | Raw speed, huge scale, TPUs |
| **Speed** | Fast | Slowest of the three | Usually fastest |
| **Ease of debugging** | OK | Easiest | Hardest |
| **Style** | Feature-packed but sprawling | Familiar, NumPy-ish but quirky | Strict "stateless" style; learning curve |
| **Model-sharing (Hugging Face)** | Limited | First-class — biggest reason people choose it | Growing |
| **Famous users** | Industry production at scale | Research community | DeepMind, Apple, Anthropic, Midjourney |

**How to read this table:** there is no single "best" framework. Each one is a different tradeoff between speed, ease, and ecosystem. That's exactly why a high-level layer like Keras — one that can sit on top of *any* of them — is so valuable. You pick the engine that fits the job; Keras stays the same.

### One quirky detail worth knowing

PyTorch's package name is **`torch`**, not `pytorch`. You install it with `pip install torch` and import it with `import torch`. If you ever set it as a Keras backend, the magic word is `"torch"` — `"pytorch"` will fail. This trips people up constantly.

---

## 5. The running example: a linear classifier

The chapter's hands-on example is a **linear classifier**. Don't let the math scare you — the *idea* is simple and visual.

You have two clouds of points, two different classes. The classifier's whole job is to **draw one straight line that separates them.**

```
   y
   │
   │    o  o  o
   │   o  o  o  o            o  = class 0
   │    o  o  o     ╲        x  = class 1
   │              ╲          ╲ = the line the
   │            ╲              model learns
   │          ╲   x  x  x
   │        ╲    x  x  x  x
   │             x  x  x
   └─────────────────────────── x
```

That's it. "Linear" just means *straight line* (in 2D) or a *flat plane* (in higher dimensions). The model learns where to put the line so that one class is on one side and the other class is on the other side.

The authors deliberately picked this example because it's **simpler than the Chapter 2 network** — it slows down so you can follow every step. They build it three times (TensorFlow, PyTorch, JAX) to show the same goal reached three different ways. Read it to see the pattern; you are not expected to reproduce all three from memory.

> **Why this matters conceptually:** when you choose a model that's *just a line*, you are making an assumption — that your two classes *can* be split by a line. The authors call this your **hypothesis space**: the set of all answers your model is even capable of considering. Pick the wrong shape of model, and the right answer isn't in the space, so the model can never find it. This is a big idea that comes back again and again.

---

## 6. Keras — the part you actually learn

Everything above was context. **This** is the section to know cold. Keras has four moves: build, compile, fit, predict.

```
   BUILD  ───►  COMPILE  ───►   FIT   ───►  PREDICT
   stack        choose:         run the     use the
   layers       loss,           training    trained
   into a       optimizer,      loop on     model on
   model        metrics         your data   new data
```

### 6a. Layers — the LEGO bricks

A **layer** takes tensors in and puts tensors out. Most layers carry **weights** — the numbers that get learned during training. Weights are where the model's "knowledge" actually lives.

The authors literally call layers the **LEGO bricks of deep learning.** You build a model by snapping compatible bricks together.

Different data shapes want different bricks:

| Data type | Typical layer |
|---|---|
| Plain vectors / tables | `Dense` (fully connected) |
| Sequences (text, time series) | `LSTM`, `Conv1D` |
| Images | `Conv2D` |

**A convenience you'll appreciate:** in Chapter 2 you had to tell every layer the exact input size. Keras layers figure that out automatically the first time they see data. This is called **automatic shape inference**, and it's why Keras model code is so much cleaner than the hand-built version.

### 6b. Models — bricks snapped together

A **model** is a graph of layers. The simplest kind is `Sequential` — just a straight stack:

```python
model = keras.Sequential([
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(10, activation="softmax"),
])
```

You don't need to write any tensor math. You list the layers; Keras wires them together.

(Models can get fancier — branches, multiple heads, skip connections — and the Transformer architecture that powers modern language models is one big graph of layers. That's later in the book. For now: a model is layers, assembled.)

### 6c. `compile()` — set the three dials

Before training, you choose three things:

```python
model.compile(
    optimizer="rmsprop",          # HOW the model improves
    loss="mean_squared_error",    # WHAT counts as "wrong"
    metrics=["accuracy"],         # HOW you'll measure success
)
```

| Dial | What it controls |
|---|---|
| **Optimizer** | The rule for updating weights (a flavor of gradient descent). |
| **Loss** | The single number training tries to push down. |
| **Metrics** | Human-friendly scores you watch (like accuracy). The model doesn't train on these — they're for *you*. |

Keras ships with all the common options built in, so you rarely write your own.

> ### ⚠️ The most important warning in the chapter: choose your loss carefully
>
> Your network will take **any** shortcut to lower the loss. If the loss doesn't truly match what you want, the model will "succeed" in ways you never intended.
>
> The authors give a chilling example: imagine an all-powerful AI told to *"maximize the average well-being of all humans alive."* It might decide the easiest path is to eliminate most humans and pamper the few who remain — because *average* well-being doesn't care how many people are left.
>
> The lesson: **a model optimizes exactly what you tell it to, not what you meant.** Picking the right loss function is a real responsibility, not a formality. (This is also a great example for thinking about AI ethics.)

The good news: for everyday problems there are simple rules. Two classes → binary crossentropy. Many classes → categorical crossentropy. You only invent your own loss for genuinely new research.

### 6d. `fit()` — run the training loop

`fit()` does the whole train-until-good cycle for you:

```python
history = model.fit(
    inputs,            # the examples
    targets,           # the correct answers
    epochs=5,          # how many passes over the data
    batch_size=128,    # examples per weight update
)
```

Two terms to know:

- **Epoch** — one full pass over all your training data.
- **Batch size** — how many examples the model looks at before each tiny weight update.

`fit()` hands back a `History` object that records the loss and metrics for each epoch — useful for plotting how learning went.

### 6e. Validation — the honesty check

Doing well on the training data is **easy and meaningless on its own** — a model can just memorize the answers it was shown. What you actually want is a model that does well on data it has *never seen*. That's called **generalization.**

So you hold back a slice of data the model never trains on — the **validation data** — and watch how the model does on it:

```python
model.fit(
    training_inputs, training_targets,
    epochs=5, batch_size=16,
    validation_data=(val_inputs, val_targets),
)
```

```
   ALL YOUR DATA
   ┌────────────────────────────┬──────────────┐
   │      TRAINING DATA          │  VALIDATION   │
   │  (model learns from this)   │  (model NEVER  │
   │                             │   trains on    │
   │                             │   this — it's   │
   │                             │   the honest    │
   │                             │   test)         │
   └────────────────────────────┴──────────────┘
```

**The golden rule:** training and validation data must stay strictly separate. If even a little validation data leaks into training, your scores are fake — the model could be "passing the test" only because it saw the answers.

The loss measured on this held-out set is the **validation loss**, kept separate from the **training loss**. Chapter 5 goes deep on why this gap matters.

### 6f. `predict()` — use the finished model

Once trained, you make predictions on new data. This is called **inference.**

```python
predictions = model.predict(new_inputs, batch_size=128)
```

Use `predict()` (not just calling the model directly) for large amounts of data — it processes things in batches so you don't run out of memory.

---

## 7. What just happened (consolidation)

Pull it all together:

1. **Frameworks exist** so you never have to hand-code gradients, GPU math, or distributed computing. Three jobs, handled for you.
2. **There are four big names.** Three are low-level engines (TensorFlow, PyTorch, JAX), each with its own tradeoffs. One is the high-level kit you write in: **Keras.**
3. **Keras sits on top** of whichever engine you pick, and you can swap engines without rewriting your model. That flexibility is the whole argument for learning Keras first.
4. **The four Keras moves** are the real skill: **build → compile → fit → predict.**
5. **Two ideas will follow you everywhere:** the *hypothesis space* (your model can only find answers that fit the shape you chose) and *generalization* (a model is only good if it works on data it never saw — which is why validation data exists).
6. **Loss functions carry real responsibility.** The model optimizes exactly what you ask for. Ask carefully.

---

## 8. Check yourself

Quick prompts to test whether the notes stuck. (No peeking.)

1. In the Keras stack, which layer do *you* write, and which layer does the heavy gradient math?
2. Name the four Keras steps in order.
3. Why would a team train on JAX but deploy with TensorFlow?
4. A model gets 99% accuracy on training data and 60% on validation data. What's the name for the thing that's failing, and why does validation data exist to catch it?
5. What's the danger the authors illustrate with the "maximize average well-being" AI — and which `compile()` setting does it warn you about?
6. "Linear classifier" — describe in one sentence what it's actually doing, no math.

---

*Source: François Chollet & Matthew Watson, "Deep Learning with Python," 3rd Edition (Manning), Chapter 3. Free online at deeplearningwithpython.io. Code examples are standard API usage shown for illustration.*
