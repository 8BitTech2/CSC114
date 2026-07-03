# Agent Guardrails — Curriculum Gap Analyzer

Rules that keep my AI partner on task for this project.

## What the agent CAN do without asking
- Write boilerplate code (data loading, file I/O, standard TF-IDF/logistic
  regression setup, plotting/report scaffolding)
- Suggest taxonomy label assignments for individual snippets, as a starting
  point for me to review — not a final decision

## What the agent must NEVER do unprompted
- Scrape live job posting sites beyond the fixed, one-time snapshot defined
  in the charter — no re-scraping, no expanding the dataset without my
  explicit go-ahead
- Invent or auto-generate labeled training data in place of me actually
  hand-labeling snippets — labels must reflect my own judgment, not a
  fabricated shortcut
- Silently swap the chosen model architecture (TF-IDF + logistic
  regression) for something else (e.g., embeddings, a neural net) without
  flagging the change and getting my agreement first

## How I'll check its work
- I review every pull request myself before merging — nothing goes to
  main un-reviewed
- I spot-check classifier predictions against my own judgment on a sample
  of snippets, rather than trusting reported accuracy numbers alone
