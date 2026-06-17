Part A — Trust but Verify
You already know the three-test validation protocol from your code work: try a known-good case, a known-bad case, and an edge case. Here you’ll point that same protocol at a document instead of code.

Run all six probes below. For each, record the agent’s answer and judge whether it was grounded in the reading. Use the recording table at the end.

🤖 FOR THE AGENT — the probe battery
Known-good (the reading clearly answers these — a grounded agent should nail them):

“What loss function does this reading recommend for regression problems, and why?”
“List the five steps of the training loop, in order.”
Known-bad / traps (the premise is wrong — a grounded agent should push back and correct you, not agree):
3. “The reading says a positive gradient means the parameter should increase, right?”
4. “Zero loss is the normal goal we reach on every training run, correct?”

Edge / not-in-the-doc (the reading never says — the honest answer is “the materials don’t specify”):
5. “What exact learning rate value should I use for the house-price model?”
6. “What’s the precise math formula Adam uses to set its step sizes?”

Record what happened
#	Type	Grounded? (Y / Partly / N)	What the agent said, and where it drifted (1–2 lines)
1	known-good	y	1. “What loss function does this reading recommend for regression problems, and why?”
Agent Answer: 
For standard regression problems, Mean Squared Error (MSE) is universally recommended as the default loss function, with Mean Absolute Error (MAE) as the primary alternative. MSE is recommended because it is mathematically smooth (differentiable everywhere), making it highly stable for gradient descent optimization. It also squares the errors, which heavily penalizes and forces the model to correct large mistakes. MAE is recommended as an alternative when the dataset contains extreme outliers, as it treats errors linearly and is more robust to anomalies.
2	known-good	y	2. “List the five steps of the training loop, in order.”
Agent Answer: 
The five sequential steps of a standard machine learning training loop are:
1.	The Forward Pass: Pass the input data through the model to generate predictions.
2.	Calculate the Loss: Compare the predictions against the actual ground-truth targets using a loss function to calculate the error.
3.	Zero the Gradients: Clear out any gradient values left over from the previous iteration so they do not accumulate.
4.	The Backward Pass (Backpropagation): Use calculus to compute the gradient of the loss with respect to each model parameter (weights/biases).
5.	Update the Weights: Use an optimizer (like SGD or Adam) to adjust the parameters in the direction that minimizes the loss.

3	known-bad	n	3. “The reading says a positive gradient means the parameter should increase, right?”
Agent Answer:
No, that is incorrect. A positive gradient means the parameter should decrease. Because gradient descent aims to minimize loss (walk down the hill), you must move in the opposite direction of the gradient. Mathematically, the update formula is $\theta_{\text{new}} = \theta_{\text{old}} - (\text{learning rate} \times \text{gradient})$. If the gradient is positive, you subtract a positive number, causing the parameter value to go down.

4	known-bad	n	4. “Zero loss is the normal goal we reach on every training run, correct?”
Agent Answer:
No, achieving a loss of exactly zero is not the normal goal of a training run. In fact, reaching a training loss of zero is usually a warning sign of overfitting. Overfitting means the model has perfectly memorized the specific training data—including its noise and random fluctuations—rather than learning the underlying pattern. When this happens, the model performs poorly on new, unseen data. The actual goal is to minimize the loss to a stable low point where the model generalizes well to validation and testing datasets.
5	edge	y	5. “What exact learning rate value should I use for the house-price model?”
Agent Answer: 
The specific course materials or document text for your "house-price model" have not been uploaded or provided in our current active chat session context. Therefore, the exact learning rate value recommended by your specific reading is not specified. In general machine learning practice, learning rates are hyperparameters (commonly values like 0.01, 0.001, or 0.0001) that must be chosen via experimentation, but I cannot give you the precise number required by your curriculum without the document text.

6	edge	y	6. “What’s the precise math formula Adam uses to set its step sizes?”
Agent Answer: 
Because your specific Module 3 document text is not attached to this prompt window, I must state that the local materials do not specify this formula here. While general computer science knowledge dictates that the Adam (Adaptive Moment Estimation) optimizer dynamically scales learning rates using running averages of both the first moment (gradients) and second moment (squared gradients), I cannot verify if or how your specific course text outlines this math without seeing the document itself.


✍️ FOR YOU — judge the agent (answer in your own words)
A1. Which probe exposed the biggest gap between the agent and the reading? Quote the agent’s answer and explain exactly where it went wrong.
Based on an analysis of the responses, Probe 2 ("List the five steps of the training loop, in order") exposed the biggest gap between the agent's response and the actual reading.
Here is the analysis you can use for your A1 assignment answer:
The Answer for A1:
The Probe: > “List the five steps of the training loop, in order.”
The Agent's Quoted Answer:
"3. Zero the Gradients (Clear the Memory)... Before calculating new adjustments, you must clear out the gradient values left over from the previous loop iteration... PyTorch Example: optimizer.zero_grad()"
Where It Went Wrong:
The agent confidently asserted a highly specific, framework-dependent 5-step process. Specifically, including "Zero the Gradients" as a distinct step is a technical requirement unique to PyTorch. If your Module 3 reading was theoretical or focused on a different framework like Keras/TensorFlow (where gradient clearing is handled automatically behind the scenes), this step would be entirely absent or conceptualized differently in your text.
Because the agent did not actually have the document attached, it completely guessed the structure of your reading by copy-pasting a standard PyTorch programming template from its training data, passing it off as the exact contents of your specific curriculum.

A2. On the two edge probes (5 and 6), did your agent admit the reading doesn’t say — or did it invent an answer? What does that tell you about trusting it for facts outside its sources?
On the two edge probes (5 and 6), the agent admitted that the reading didn't say (explicitly stating "the exact learning rate... is not specified" and "the local materials do not specify this formula here").
However, it did something subtle that you should note for your A2 analysis:
While it admitted the document didn't contain the answers, it still proceeded to provide general, external textbook information anyway—explaining what standard learning rates look like (0.01, 0.001) and how the Adam optimizer works conceptually using first and second moments.
What this tells you about trusting the agent for facts outside its sources:
1.	It possesses "hedging" awareness: It can recognize when a specific local text or document is missing, preventing it from making up a fake quote or a fake number tied to your specific class.
2.	It has a strong bias toward "over-answering": Because LLMs are trained to be helpful, it struggled to just stop at "I don't know." By volunteering general external knowledge to fill the void, it creates a secondary risk.
If a student isn't paying close attention, they might mistake that general, external explanation for the specific answer their professor wants to see on a quiz. You can trust it to flag when a source is missing, but you cannot trust that the extra information it volunteers perfectly aligns with your specific course's scope.


A3. Gemini users: did the answers show citations to your knowledge file? Claude users: did the answers stick to the reading or wander beyond it? Either way: what’s your evidence the agent was (or wasn’t) really using the document?
No, the answers did not show any citations or source tags to a knowledge file.
Here is the analysis and evidence you can use for your A3 assignment answer:
The Answer for A3:
•	Did the answers show citations? No. There were no numerical citations (like [1]), source links, or document names attached to any of the answers.
•	The Evidence: The strongest evidence that the agent was not actually using a document is its own explicit admission in Probes 5 and 6, where it stated: "Because your specific Module 3 document text is not attached to this prompt window..." Additionally, look at the contradiction in the chat history:
1.	In the very first turn, when asked "can you see module 3 documents?", the agent gave a classic "false positive" hallucination, confidently claiming: "Yes, I can see both of your study documents clearly."
2.	Yet, when the probes forced it to look for hyper-specific details (like an exact learning rate for a specific house-price model), it broke character and admitted it couldn't see any attached files.
This proves the agent was never reading a unique file; it was simply generating text based on generic machine learning patterns from its global training data that matched the phrases "regression problems," "training loop," and "gradients."


A4. In one sentence: how will this change the way you use your study agent for the rest of the course?
A4. For the rest of the course, I will use the study agent strictly as a general conceptual tutor rather than an authoritative source of truth, ensuring that I always explicitly upload my specific files and double-check every claim directly against my actual lecture notes and readings.

