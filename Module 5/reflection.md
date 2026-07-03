# Reflection — Curriculum Gap Analyzer

## Which workflow step was I on when Housing "stopped"?

My validation MAE plateaued around epoch 28, but the final model in the
provided script still trained for 130 epochs — well past the turnaround.
It ran past the point where the model was actually improving because the
epoch count was hardcoded in advance, without checking where the
validation curve had already leveled off. Nobody (including me, at the
time) stopped to verify the model against its own curve before training
the final version. So the honest answer is: I stopped on "scale up," but
I didn't actually catch and act on the overfitting signal — the script
just ran to a fixed number regardless of what the curve was telling me.

## What's different this time?

This time, I plan to actually watch validation accuracy as training
happens, rather than picking a fixed number of epochs up front. I'll
identify a baseline (the majority-class guess) before building anything,
so I have a real floor to compare against — and I'll use the validation
split to check whether the classifier is actually improving, rather than
assuming more training automatically means a better result. The Housing
project showed me that a model can look like it's working while quietly
running past the point where it stopped helping; this time, "good
enough" means checking that signal directly instead of trusting a
preset number.
