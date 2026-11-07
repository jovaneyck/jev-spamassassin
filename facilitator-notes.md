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
* [Don't call it a decision model](https://typesafe.ai/blog/dont-call-it-a-decision-model): judgments vs. decisions, the idea step 6 is built on
* [Models and aliases](https://docs.typesafe.ai/go/models.md)

## Budget

Per attendee, following steps 1–7:

| Step               | Requests | Input tokens (approx.)                        |
| ------------------ | -------- | --------------------------------------------- |
| 1 `hello_jev.py`   | 1        | small                                         |
| 3 `first_call.py`  | 1        | ~1k                                           |
| 5 `solve.py train` | 10       | ~41k                                          |
| 6 `solve.py train` | 10       | ~50k (3 questions per email, `scam` criteria repeated per email) |
| 7 `solve.py test`  | 10       | ~41k                                          |
| **Total**          | **32**   | **~140k**                                     |

Token counts are extrapolated from one measured batch of 10 train emails (4127 input tokens). `solve.py` sends up to 8 requests in parallel (`CONCURRENCY` in `solve.py`), so a room of 20 on one shared key can send 160 requests at once. Check the rate limit beforehand.

Step 8 (hill-climbing) is open-ended. The autonomous Claude prompt caps itself at 20 train runs, which is 200 requests or about 1M input tokens per attendee.

## Timing

| #   | Step           | Time | Watch out for                                                                                         |
| --- | -------------- | ---- | ----------------------------------------------------------------------------------------------------- |
| 0   | Intro to Jev   | 10   | Take your time here. See [Opening](#opening-explain-jev).                                             |
| 1   | Setup          | 10   | uv not installed, `.env` missing or in the wrong folder. On PowerShell, `cp .env.example .env` works. |
| 2   | Meet the data  | 5    | Nothing tricky. Keep it moving.                                                                       |
| 3   | First Jev call | 10   | The Windows console may show `£` as `�`. That's the console's encoding, not a bug.                    |
| 4   | Batching       | 5    | A reading step. Skip the optional trade-off experiments.                                              |
| 5   | Baseline       | 10   | Make sure attendees **write down** their numbers, because step 6 overwrites `out/train.jsonl`.        |
| 6   | Split decision | 20   | Most errors are copy-paste errors. Make sure attendees see the decision tests fail before they paste `spam`. |
| 7   | Test set       | 5    | Tight: the explainer is long. Take time from step 6 if needed.                                        |
| –   | Closing circle | 5    | Don't skip it, even when running late. See [Closing circle](#closing-circle).                         |

Each step ends with a **🧠 Self-check**: questions with collapsed answers. Point attendees to them, and ask one out loud when the room is ahead of schedule.

## Opening: explain Jev

Before step 1, take time to explain Jev. Attendees who skip this treat it as a chat LLM and get lost in step 3. Cover:

- **What it is:** an API that answers typed questions about data you give it, not a chat model. See the [jev introduction](https://docs.typesafe.ai/introduction).
- **`state` and `questions`:** `state` is the data, questions point into it by name between backticks.
- **Noul:** a yes/no question answered as a number from 0.0 to 1.0. Mention that other question types exist.
- **Judgments, not decisions:** Jev makes judgments, code makes decisions. Plant it here, and step 6 cashes it in. Avoid calling Jev a "decision model".
- **Model and SDK:** `jev-1.14.0` via `typesafe_sdk`, and the [skill](https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md) for coding agents, since Jev isn't in their training data.

## Closing circle

Last 5 minutes. Everyone answers in one sentence, round the room:

- What surprised you?
- Where would you use Jev in your own work?

Collect open questions and follow up afterwards.

## Expected numbers

Jev's answers vary from run to run. Two identical train runs differed by about 0.01 accuracy (one email).

| Run             | auc  | accuracy  | precision | recall    | hard_ham |
| --------------- | ---- | --------- | --------- | --------- | -------- |
| Train, baseline | 0.98 | 0.92–0.94 | 0.83–0.87 | 1.00      | 0.60–0.70 |
| Train, split    | 1.00 | 0.95–0.96 | 0.97      | 0.90–0.93 | 1.00     |
| Test, baseline  | 0.98 | 0.94      | 0.87      | 1.00      | 0.70     |
| Test, split     | 0.99 | 0.95      | 0.95      | 0.93      | 0.90     |

Measured on `jev-1.14.0` (pinned in `spam/jev.py`), 2026-11-07. Train runs were repeated twice; test runs once.

- **Step 1:** `hello_jev.py` scores about 0.75.
- **Step 3:** the Ryanair hard-ham email scores about 0.93–0.95 spam.
- **Step 5 misses:** 6–8 hard-ham newsletters and shop mails, from CNET ×3, Amazon, Ryanair, DayTips, dELiA*s and All Things New England.
- **Step 6 misses:** at most one ham (boingboing, `legit_sender` ≈ 0.50) and 3–4 spam business ads from senders that look legitimate.
- **Step 7 misses:** 2 hard ham (Red Hat Network, Buy4Now) and 3 spam, two of them with a faked `List-Unsubscribe` header.

## Points to land

- **Step 3:** `state` is what Jev looks at, questions point into it by name. The 0.95 on a legitimate email sets up step 6.
- **Step 4:** billing is per token, not per request. Batching shares a fixed per-request overhead (about 260 input tokens, derived from one measurement). Only `state` is shared: per-question criteria are repeated in every batch.
- **Step 5:** read the misses before you change anything. They all share one pattern.
- **Step 6:** Jev makes judgments, code makes decisions. "Is this spam?" is a decision: split it into judgments Jev can make at a glance (`scam`, `advertising`, `legit_sender`), facts code knows exactly (`list_mail`), and a rule in code that's unit-tested. The alternative, adding clauses to one question for every miss, is what TypeSafe calls prompt gymnastics. Precision is the metric that matters for spam, because flagged ham is the costly mistake. The trace in `misses.py` shows which judgment or fact decided each email.
- **Step 7:** real mail in the spam folder falls from 6–8 to 0–1 on train, but only from 6 to 2 on test. That's overfitting, measured, but the gain holds. Two test spams slip through with a faked `List-Unsubscribe` header: a fact can be wrong too, and the train set never showed it.

## Known limitations (be upfront if asked)

- **Small sets.** 100 emails per set, 20 per partition. One email is 0.01 accuracy overall and 0.05 on `hard_ham`. The accuracy gain from step 6 on test (+0.01) is within noise. The false-positive drop on test (6 to 2) is small in absolute terms.
- **The ~260-token overhead** is inferred from a single comparison of 10 single requests against 1 batched request, not from documentation.
- **The quality effects of batching** (neighbouring emails influencing each other, larger batches answering worse) are listed as risks. None were measured.
- **Jev only sees** From, Subject and the first 2000 characters of the body (`spam/message.py`). Code reads `List-Unsubscribe` and `List-Id` as the `list_mail` fact, which spammers can fake (step 7).
- **The corpus rewrote some addresses** to `spamassassin.taint.org` (e.g. `rhn-admin@rhn.spamassassin.taint.org`), which can make `legit_sender` misjudge a real company.
- **Step 6's question count:** 3 questions per email instead of 1, so a batch uses about 5.0k input and 600 output tokens, compared with 4.1k and 200 for the baseline.
- **The model is pinned to `jev-1.14.0`** (`spam/jev.py`). Aliases like `jev-latest` and `jev-preview` move when a new release ships, and the expected numbers would drift with them. Re-run the dry run before you bump it.

## How the data was prepared

- **Corpus:** the [SpamAssassin public corpus](https://spamassassin.apache.org/old/publiccorpus/). Only the latest release of each partition is used, because later releases fix and replace earlier ones (`latest_releases` in `spam/corpus.py`): `20030228_{easy_ham, easy_ham_2, hard_ham, spam}` and `20050311_spam_2`. That leaves 6045 emails (`spam_2/00471.df77…` was removed from both `spam_2` archives: its 7000-parameter `Content-Type` header trips ClamAV's `Heuristics.Limits.Exceeded.EmailMIMEArguments`, which corporate antivirus such as Cisco AMP flags and quarantines).
- **Splits:** `split.py` draws 20 emails per partition for each set with seed 42. The two sets are disjoint, and each has 60 ham and 40 spam. They're committed in `splits/`. Re-running `split.py` with another `PER_PARTITION` redraws **both** sets.
- **Output:** `solve.py` writes per-email scores to `out/<set>.jsonl`, which is gitignored.
