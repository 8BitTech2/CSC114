# Module 4 — Assess: Explain What You Built
**CSC-114 Artificial Intelligence I**

---

## Part 1 — Your Run

**Q1. Which option did you build, and what one change did you make, if any?**

I built the house prices model. The one change I made was experimenting with the K value in K-fold cross-validation — I tried K=4, then K=9, then K=5, and found that K=5 gave the best results.

---

## Part 2 — Your Training Curve

**Q2. Attach your training curve. Looking at your curve, at which epoch does the validation line stop improving? How can you tell from the picture?**

[Insert your validation MAE curve image here — e.g. housing_val_mae.png]

Looking at my curve, the validation MAE stops improving around epoch 28. Before that point, the line drops steeply — MAE falls fast, from close to 0.93 down to around 0.30. After epoch 28, the line flattens out and just bounces around in that same range (roughly 0.28–0.31) for the rest of training, with no further downward trend.

**Q3. What is the model actually doing wrong after that turnaround point?**

After epoch 28, the validation MAE stops improving and just plateaus/bounces around instead of continuing to drop. The likely explanation is overfitting — the model starts fitting quirks of the training data rather than learning patterns that generalize. Normally you'd confirm this by seeing training error keep dropping while validation error flattens or worsens, but my script only saved validation MAE, not training MAE, so I can't directly verify that gap. Based on the plateau alone, overfitting is my best explanation, but I can't rule out that the model has simply reached its performance ceiling on this data.

---

## Part 3 — Working With Your Agent

**Q4. Describe one moment you corrected or pushed back on your agent.**

When I tried K=9, my agent pointed out the mean CV MAE was the lowest yet (0.283). But I pushed back on treating that as "better," because I noticed the per-fold scores were all over the place (0.233 to 0.345) and the CV-to-test gap (0.069) was actually the worst of my three experiments. That told me the individual folds — only ~53 validation samples each — were too small and noisy to trust, even though the average looked good. So instead of keeping K=9, I tried K=5, which gave both a good mean MAE and the tightest CV-to-test gap I'd seen.

**Q5. Name one thing your agent did well that saved you time.**

One thing my agent did well was explain overfitting and suggest experimenting with the K value in cross-validation. This saved me time because instead of guessing randomly at what to change, I had a clear starting point — testing different K values — and understood why it mattered (smaller validation folds are noisier and less reliable). That guidance led directly to the K=9 experiment, which is what tipped me off to the CV-to-test gap problem I described in Q4.

---

## Part 4 — Why Your Settings Are the Right Ones

**Q6. Option B — House Prices**

The last layer has no activation because house prices can be almost any number, not a value squeezed between 0 and 1. If I used sigmoid, the model's output would always be capped between 0 and 1, so it could never correctly predict a house price like 3.0 or 9.0 (in the scaled units my script uses) — it would be mathematically stuck no matter how well it trained.

Accuracy doesn't work well for house prices because it only measures exact matches — right or wrong, with no partial credit for being close. A model predicting $308,900 when the true price is $312,450 would count as a total miss under accuracy, even though it's a good prediction. MAE is a better fit because it measures the average dollar amount the predictions are off by, so it rewards the model for getting close, not just exact.

We normalize using only the training data's mean and standard deviation because the test set is supposed to represent completely unseen, real-world data — used only to check how well the model generalizes after training is done. If we calculated the mean/std using the test data too, some information about the test set would quietly leak into the numbers used to scale the training data, even before the model saw any test examples directly. That would make the test evaluation less honest, since the test set wouldn't be truly "unseen" anymore.

**Q7. Using your own training curve as evidence, explain why "more epochs = better" is not true for your model.**

My curve shows that more epochs did not keep improving the model. Validation MAE dropped fast up to about epoch 28, but from there through epoch 200 — over 170 more epochs — it never improved further; it just plateaued and bounced around in the same ~0.28–0.31 range. So training longer past epoch 28 didn't buy me anything: it likely just let the model overfit more, without any real gain.

---

## Part 5 — Honest Self-Check

**Q8. How much of what you built do you genuinely understand versus trust your agent on?**

I genuinely understand data leakage — why normalizing with test set statistics would let information about the test data quietly influence training, making the evaluation dishonest.

However, I still trust my agent more than myself on the mean/standard deviation normalization step. I understand why we normalize using only training stats, but the actual math behind mean and standard deviation — how they're calculated and what they represent statistically — is something I'd struggle to rebuild from scratch without help.

**Q9. Explain your model to a classmate in three sentences.**

[Note: confirm your input features before submitting — e.g. housing characteristics such as rooms, location, and income level]

My model takes in housing feature data. It predicts the price of a house. The model makes predictions, compares them to the actual prices, and adjusts its internal weights to reduce the error — repeating this process until the predictions are as accurate as possible.

---

## Reflection Questions

**1. What did you change, and how did the results change?**

I experimented with the K value in K-fold cross-validation — testing K=4, K=9, and K=5. K=9 gave the lowest mean CV MAE (0.283) on the surface, but I noticed the per-fold scores were wildly inconsistent (0.233 to 0.345) and the CV-to-test gap was the worst of the three (0.069) — a sign the small ~53-sample validation folds were too noisy to trust. Switching to K=5 gave both a solid mean MAE and the tightest CV-to-test gap (0.025), making it my best configuration.

**2. What surprised you most about your model's behavior, and why did it surprise you?**

What surprised me most was how early the validation curve plateaued. Based on the textbook, I expected the model to take a higher number of epochs before leveling off, but instead it flattened around epoch 28 and then stayed flat for the remaining 170+ epochs with no further improvement. My first instinct was that this pointed to overfitting — the model reaching its limit on this data faster than I'd anticipated.

**3. If you rebuilt this model from scratch tomorrow with no notes, what's the one part you'd get wrong or forget, and why?**

I understand why we normalize using only training stats (to avoid data leakage), but the actual math behind mean and standard deviation — how they're calculated and what they represent statistically — is something I'd struggle to rebuild from scratch without help.

---

## Submission Items

- Training curve image: [attach housing_val_mae.png and/or housing_val_mae_truncated.png]
- Apply PR link / Apply screenshots: [attach here]
