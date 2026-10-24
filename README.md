# Build with Jev: a spam filter in one hour

Let's build a spam filter on the [SpamAssassin public corpus](https://spamassassin.apache.org/old/publiccorpus/) by asking Jev yes/no questions about emails. Then you'll measure it, improve it once, and check whether the improvement holds on emails you haven't looked at.

## You need

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (it installs Python 3.12 for you)
- A TypeSafe API key (ask the facilitator)
- A terminal open in this folder

Typesafe clients are available for Javascript and other languages as well, but you and your agent will be on your own porting the workshop to them and struggling with API inconsistencies.

## On the use of coding agents

Coding agents are encouraged but not essential to reduce the toil, you'll learn most effectively by going through the workshop step by step and making sure you understand each part before moving on. Protip: ask the agent for clarifications whenever something is unclear!

Jev is quite fresh and not yet part of the model weights, so you might want to copy the following skill for better results when working with typesafe/jev: [typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md](https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md)

## Agenda

| #   | Step                                                 | Time   |
| --- | ---------------------------------------------------- | ------ |
| 1   | [Setup](workshop/01-setup.md)                        | 10 min |
| 2   | [Meet the data](workshop/02-meet-the-data.md)        | 5 min  |
| 3   | [Your first Jev call](workshop/03-first-jev-call.md) | 10 min |
| 4   | [Ten emails, one request](workshop/04-batching.md)   | 5 min  |
| 5   | [Measure the baseline](workshop/05-baseline.md)      | 10 min |
| 6   | [Improve the question](workshop/06-improve.md)       | 15 min |
| 7   | [Check on the test set](workshop/07-test-set.md)     | 5 min  |

Start with [step 1](workshop/01-setup.md).

After the workshop: [Exploring further](workshop/08-exploring-further.md) covers hill-climbing, by hand or with Claude doing the climbing for you.

## Project map

| Path              | What it does                                                       |
| ----------------- | ------------------------------------------------------------------ |
| `extract.py`      | Unpacks the corpus archives into `dataset/`                        |
| `split.py`        | Writes the train and test sets to `splits/` (already done for you) |
| `spam/message.py` | Reduces a raw email to sender, subject and the start of the body   |
| `spam/jev.py`     | Builds one Jev request for a batch of emails and reads its answers |
| `spam/solver.py`  | Sends every batch, a few at a time                                 |
| `spam/metrics.py` | AUC, accuracy, precision and recall                                |
| `solve.py`        | Classifies a set and prints its scores                             |
| `tests/`          | Unit tests: `uv run pytest`                                        |
