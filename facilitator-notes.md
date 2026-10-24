# Facilitator notes

Workshop entry point: [README.md](README.md). Attendees don't need this file.

## Before the workshop

- **Do a dry run** on a clean clone, following the steps exactly as written: `uv sync`, `uv run extract.py`, `uv run hello_jev.py`, `uv run pytest`, then steps 3–7. Expect the [numbers below](#expected-numbers).
- **API keys:** hand out one key per attendee, or a shared key with enough rate limit (see [Budget](#budget)). Keys look like `apikey_...` and go in `.env` (copied from `.env.example`; `.env` is gitignored).
- **Ask attendees to install [uv](https://docs.astral.sh/uv/getting-started/installation/) and run `uv sync` beforehand.** Setup is the step most likely to overrun its 10 minutes.
- **The corpus ships in the repo** as nine `*.tar.bz2` archives (about 13 MB). `extract.py` unpacks them into `dataset/`, which is gitignored.

## References

* [typesafe.ai](https://typesafe.ai/)
* [jev introduction](https://docs.typesafe.ai/introduction)

## Budget

Per attendee, following steps 1–7:

| Step               | Requests | Input tokens (approx.)                        |
| ------------------ | -------- | --------------------------------------------- |
| 1 `hello_jev.py`   | 1        | small                                         |
| 3 `first_call.py`  | 1        | ~1k                                           |
| 5 `solve.py train` | 10       | ~41k                                          |
| 6 `solve.py train` | 10       | ~45k (the criteria are repeated per question) |
| 7 `solve.py test`  | 10       | ~41k                                          |
| **Total**          | **32**   | **~130k**                                     |

Token counts are extrapolated from one measured batch of 10 train emails (4127 input tokens). `solve.py` sends up to 8 requests in parallel (`CONCURRENCY` in `solve.py`), so a room of 20 on one shared key can send 160 requests at once. Check the rate limit beforehand.

Step 8 (hill-climbing) is open-ended. The autonomous Claude prompt caps itself at 20 train runs, which is 200 requests or about 1M input tokens per attendee.

## Timing

| #   | Step           | Time | Watch out for                                                                                         |
| --- | -------------- | ---- | ----------------------------------------------------------------------------------------------------- |
| 1   | Setup          | 10   | uv not installed, `.env` missing or in the wrong folder. On PowerShell, `cp .env.example .env` works. |
| 2   | Meet the data  | 5    | Nothing tricky. Keep it moving.                                                                       |
| 3   | First Jev call | 10   | The Windows console may show `£` as `�`. That's the console's encoding, not a bug.                    |
| 4   | Batching       | 5    | A reading step. Skip the optional trade-off experiments.                                              |
| 5   | Baseline       | 10   | Make sure attendees **write down** their numbers, because step 6 overwrites `out/train.jsonl`.        |
| 6   | Improve        | 15   | Most errors are copy-paste errors in `spam/jev.py`. `uv run pytest` catches them.                     |
| 7   | Test set       | 5    | Tight: the explainer is long. Take time from step 6 if needed.                                        |

## Expected numbers

Jev's answers vary from run to run. Two identical train runs differed by about 0.01 accuracy (one email).

| Run             | auc  | accuracy  | precision | recall    | hard_ham |
| --------------- | ---- | --------- | --------- | --------- | -------- |
| Train, baseline | 0.98 | 0.91      | 0.82      | 1.00      | 0.55     |
| Train, criteria | 1.00 | 0.97–0.98 | 0.97      | 0.95–0.98 | 0.95     |
| Test, baseline  | 0.98 | 0.93      | 0.85      | 1.00      | 0.70     |
| Test, criteria  | 1.00 | 0.94      | 0.89      | 0.98      | 0.80     |

- **Step 3:** the Ryanair hard-ham email scores about 0.95 spam.
- **Step 5 misses:** 9 hard-ham newsletters and shop mails (CNET ×3, Amazon, DivX, Ryanair, DayTips, dELiA*s, All Things New England).

## Points to land

- **Step 3:** `state` is what Jev looks at, questions point into it by name. The 0.95 on a legitimate email sets up step 6.
- **Step 4:** billing is per token, not per request. Batching shares a fixed per-request overhead (about 260 input tokens, derived from one measurement). Only `state` is shared: per-question criteria are repeated in every batch.
- **Step 5:** read the misses before you change anything. They all share one pattern.
- **Step 6:** criteria draw the line better than a one-line definition. Precision is the metric that matters for spam, because flagged ham is the costly mistake.
- **Step 7:** the train gain (+0.06) mostly disappears on test (+0.01, one email). That's overfitting, measured.

## Known limitations (be upfront if asked)

- **Small sets.** 100 emails per set, 20 per partition. One email is 0.01 accuracy overall and 0.05 on `hard_ham`. The test gain from step 6 is within noise.
- **The ~260-token overhead** is inferred from a single comparison of 10 single requests against 1 batched request, not from documentation.
- **The quality effects of batching** (neighbouring emails influencing each other, larger batches answering worse) are listed as risks. None were measured.
- **Jev only sees** From, Subject and the first 2000 characters of the body (`spam/message.py`), so header signals like `List-Unsubscribe` are lost. Step 8 suggests adding them.
- **The model is `jev-preview`** (`spam/jev.py`), as in the Where's Waldo workshop.

## How the data was prepared

- **Corpus:** the [SpamAssassin public corpus](https://spamassassin.apache.org/old/publiccorpus/). Only the latest release of each partition is used, because later releases fix and replace earlier ones (`latest_releases` in `spam/corpus.py`): `20030228_{easy_ham, easy_ham_2, hard_ham, spam}` and `20050311_spam_2`. That leaves 6046 emails.
- **Splits:** `split.py` draws 20 emails per partition for each set with seed 42. The two sets are disjoint, and each has 60 ham and 40 spam. They're committed in `splits/`. Re-running `split.py` with another `PER_PARTITION` redraws **both** sets.
- **Output:** `solve.py` writes per-email scores to `out/<set>.jsonl`, which is gitignored.
