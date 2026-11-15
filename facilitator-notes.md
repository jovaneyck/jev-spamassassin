# Facilitator notes

Workshop entry point: [README.md](README.md). Attendees don't need this file.

The poster promises a loud, slightly eccentric hour: *Jo! meets Jev.* The workshop pages carry that voice, and the room should too. Vote out loud, cheer the first friendly fire that disappears, hand out the boa.

## Before the workshop

- **Do a dry run** on a clean clone, following the pages exactly as written, from `uv sync` to `uv run misses.py test`. Expect the [numbers below](#expected-numbers).
- **API keys.** Hand out one key per attendee, or a shared key with enough rate limit. See [Budget](#budget). Keys look like `apikey_...` and go in `.env`, copied from `.env.example`. `.env` is gitignored.
- **Ask attendees to install [uv](https://docs.astral.sh/uv/getting-started/installation/) and run `uv sync` beforehand.** Setup is the step most likely to overrun.
- **The corpus ships in the repo** as nine `*.tar.bz2` archives, about 13 MB. `extract.py` unpacks them into `dataset/`, which is gitignored.
- **Set up two shared boards**, on Miro, in a chat channel or on a whiteboard. One is the *spam hall of fame*, open from step 00 to 05. The other is the *leaderboard* for step 05. Have the links ready to paste.
- **Bring prizes.** One for the hall-of-fame winner, one for the leaderboard. A pink feather boa fits the poster.

## Timing: 60 minutes

| #   | Step    | Time | What you do                                                                                                   | Watch out for                                                                                         |
| --- | ------- | ---- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 00  | Boot up | 10   | Pitch Jev in 3 minutes while `uv sync` and `extract.py` run. See [Opening](#opening-pitch-jev). Then run the *Spam or not?* vote on the big screen. Share the hall-of-fame link. | uv not installed, `.env` missing or in the wrong folder. `cp .env.example .env` works in PowerShell too. |
| 01  | Ask     | 10   | Ask the room to guess the Ryanair score before they run it. Collect the best silly question.                  | The Windows console may show `£` as `?` or `�`. That's the console's encoding, not a bug.             |
| 02  | Batch   | 5    | A reading step. Keep it moving.                                                                               | Point early finishers to the hall of fame.                                                            |
| 03  | Measure | 10   | Ask for a show of hands: who beat Jev at the quiz?                                                            | Make sure attendees **write down** their numbers, because step 04 overwrites `out/train.jsonl`.        |
| 04  | Improve | 20   | 15 minutes of building, then 5 minutes of *Spam your neighbour*.                                              | Most errors are copy-paste errors. Make sure attendees see the decision tests fail before they paste `spam`. Cut the red-team round short if the room is behind. |
| 05  | Test    | 5    | Read the leaderboard, crown both winners, then go round the room: one sentence each.                          | Tight. Take a minute from step 04 if needed. Don't skip the closing round.                             |

Every step ends with **Brain on**: one or two questions with collapsed answers, plus **Deep cuts** for the curious. When the room is ahead of schedule, ask one out loud.

## Opening: pitch Jev

Attendees who skip this treat Jev like a chat LLM and get lost in step 01. Cover, in 3 minutes:

- **What it is.** An API that answers typed questions about data you give it. Not a chat model. See the [jev introduction](https://docs.typesafe.ai/introduction).
- **`state` and `questions`.** `state` is the data, questions point into it by name between backticks.
- **Noul.** A yes/no question answered as a number from 0.0 to 1.0. Other question types exist.
- **Jev judges, code decides.** Plant it here, step 04 cashes it in. Avoid calling Jev a "decision model". The poster does, and [the blog post](https://typesafe.ai/blog/dont-call-it-a-decision-model) explains why that's a trap.
- **Model and SDK.** `jev-1.14.0` through `typesafe_sdk`, and the [skill](.agents/skills/typesafe-ai/SKILL.md) for coding agents, since Jev isn't in their training data.

## The games

### Spam or not? (step 00, settled in step 03)

Show each email with `uv run peek.py <id>` on the big screen. The room votes spam or ham by raising hands. Don't reveal the answers until everyone has voted.

| Email   | Label | Partition  | What it is                                                             |
| ------- | ----- | ---------- | ---------------------------------------------------------------------- |
| `00572` | ham   | `easy_ham` | FoRK mailing list thread about scrambled spelling. Looks like gibberish. |
| `00895` | spam  | `spam_2`   | A Lagos barrister and the late General Abacha's money.                 |
| `00237` | ham   | `hard_ham` | Jeff Bezos announcing Amazon's apparel store. Easy to mistake for spam. |
| `00408` | spam  | `spam_2`   | A recruiting agency "newsletter" from an Irish IT recruiter.           |
| `00276` | spam  | `spam`     | "Did I give you the money yet?" A work-from-home pitch.                |

In step 03, `quiz.py` shows Jev's answers. The baseline gets the three spams right and usually bins Jeff Bezos, but only just, at about 0.53. After step 04, Jev gets Bezos right and misses `00408`: a business ad from a sender that looks legitimate, the exact kind of spam the new rule lets through. Point that out. It's a nice way into step 05.

### Spam hall of fame (step 00 to 05)

`uv run peek.py spam` lists the subjects of the 40 train spams. Attendees post favourites on the board. Pick a winner in step 05. Some contenders to get the room going: "Grow Up And Be A Man!", "New Improved Weight Loss, Now With Bonus Fat Absorbers!", "we find yuo the lowest mortgage".

### Spam your neighbour (end of step 04)

Attendees write a spam email in `my_spam.eml`, send it to their neighbour, and the neighbour runs it through their own filter with `uv run judge.py their_spam.eml`. The neighbour also referees. The email has to really be spam.

- **The intended discovery** is the cheat code. A plain ad with a faked `List-Unsubscribe` header gets through, because the rule treats mailing-list senders as known. The collapsed hint in step 04 gives it away for anyone stuck. Step 05 then shows real 2002 spammers doing the same in the test set.
- **File encoding matters on Windows.** PowerShell's `>` writes UTF-16, which `judge.py` refuses with a `UnicodeDecodeError`. Tell attendees to create the file in their editor. `judge.py` reads with `utf-8-sig`, so a UTF-8 BOM is fine; without that, the headers would silently vanish and the cheat code would stop working.
- **Scams don't get through** this way. `scam` sits outside the `list_mail` check. If someone's scam lands in an inbox, put it on the big screen. That's a real hole in the questions.
- Each `judge.py` run is one Jev request.

### Leaderboard (step 05)

Attendees post their test `precision` and `friendly fire`. Everyone ran the same code, so the spread is Jev's run-to-run wobble on 100 emails. Say so out loud when you crown the winner. It's the small-sets lesson in one sentence.

## Closing round

Everyone answers in one sentence, round the room:

- What surprised you?
- Where would you use Jev in your own work?

Collect open questions and follow up afterwards.

## Budget

Per attendee, following steps 00 to 05:

| Step                        | Requests | Input tokens (approx.)                                          |
| --------------------------- | -------- | --------------------------------------------------------------- |
| 00 `hello_jev.py`           | 1        | small                                                           |
| 01 `first_call.py`          | 1        | ~1k                                                             |
| 01 `silly.py`               | 1–3      | ~1k each                                                        |
| 03 `solve.py train`         | 10       | ~41k                                                            |
| 04 `solve.py train`         | 10       | ~50k: 3 questions per email, `scam` criteria repeated per email |
| 04 `judge.py`, red team     | 3–6      | ~0.5k each                                                      |
| 05 `solve.py test`          | 10       | ~41k                                                            |
| **Total**                   | **~40**  | **~140k**                                                       |

Token counts are extrapolated from one measured batch of 10 train emails, 4127 input tokens. `solve.py` sends up to 8 requests in parallel (`CONCURRENCY` in `solve.py`), so a room of 20 on one shared key can send 160 requests at once. Check the rate limit beforehand.

The side quests are open-ended. The agent hill-climbing prompt caps itself at 20 train runs, which is 200 requests or about 1M input tokens per attendee.

## Expected numbers

Jev's answers vary from run to run. Two identical train runs differed by about 0.01 accuracy, one email.

| Run                | auc  | accuracy  | precision | recall    | hard_ham  | friendly fire |
| ------------------ | ---- | --------- | --------- | --------- | --------- | ------------- |
| Train, step 03     | 0.98–0.99 | 0.92–0.94 | 0.83–0.87 | 1.00      | 0.60–0.70 | 6–8           |
| Train, step 04     | 1.00      | 0.95–0.96 | 0.97–1.00 | 0.90–0.93 | 1.00      | 0–1           |
| Test, step 03 code | 0.98      | 0.94      | 0.87      | 1.00      | 0.70      | 6             |
| Test, step 04      | 0.99      | 0.95–0.96 | 0.95      | 0.93–0.95 | 0.90      | 2             |

Measured on `jev-1.14.0`, pinned in `spam/jev.py`, on 2026-11-07 and again in the 2026-11-15 dry run. Train runs were repeated two or three times; test runs once per dry run.

- **Step 00.** `hello_jev.py` scores about 0.75–0.79.
- **Step 01.** The Ryanair hard-ham email scores about 0.93–0.96 spam. `silly.py` on the barrister: passive-aggressive about 0.07, shouting 0.29, mum would fall for it 0.46, pirate 0.13.
- **Step 03 misses.** 6–8 hard-ham newsletters and shop mails, from CNET, Amazon, Ryanair, DayTips, dELiA*s and All Things New England.
- **Step 04 misses.** Usually one ham, a boingboing RSS item from `easy_ham` with `legit_sender` about 0.46–0.50, and 3–4 spam business ads from senders that look legitimate, quiz email `00408` among them.
- **Step 04 red team.** The example `my_spam.eml` scores 0.99. A plain ad from an unknown sender scores about 0.7. The same ad with a `List-Unsubscribe` header scores about 0.07 and lands in the inbox. A scam with that header still scores 0.99.
- **Step 05 misses.** 2 hard ham (Red Hat Network, Buy4Now) and 2–3 spam, one or two of them with a faked `List-Unsubscribe` header.

## Points to land

- **Step 01.** `state` is what Jev looks at, questions point into it by name. The 0.95 on a legit email sets up step 04. The silly questions show Jev isn't a spam model.
- **Step 02.** Billing is per token, not per request. Batching shares a fixed per-request cover charge of about 260 input tokens, derived from one measurement. Only `state` is shared. Jev repeats per-question criteria for every email in a batch.
- **Step 03.** Read the misses before you change anything. They all share one pattern. Friendly fire is the expensive mistake.
- **Step 04.** Jev judges, code decides. "Is this spam?" is a decision. Split it into judgments Jev can make at a glance (`scam`, `advertising`, `legit_sender`), facts code knows exactly (`list_mail`), and a rule in code with unit tests. The alternative, a new clause for every miss, is what TypeSafe calls prompt gymnastics and the pages call prompt yoga. The trace in `misses.py` shows which judgment or fact decided each email.
- **Step 05.** Friendly fire falls from 6–8 to 0–1 on train, but only from 6 to 2 on test. That's overfitting, measured, and the gain still holds. Two test spams slip through with a faked `List-Unsubscribe` header in some runs, one in others. A fact can lie too, and the train set never showed it. The red-team round found it first.

## Known limitations (be upfront if asked)

- **Small sets.** 100 emails per set, 20 per partition. One email is 0.01 accuracy overall and 0.05 on `hard_ham`. The accuracy gain from step 04 on test, +0.01, is within noise. The friendly-fire drop on test, 6 to 2, is small in absolute terms.
- **The ~260-token cover charge** is inferred from a single comparison of 10 single requests against 1 batched request, not from documentation.
- **The quality effects of batching**, neighbouring emails influencing each other and larger batches answering worse, are listed as risks. None were measured.
- **Jev only sees** From, Subject and the first 2000 characters of the body (`spam/message.py`). Code reads `List-Unsubscribe` and `List-Id` as the `list_mail` fact, which spammers can fake.
- **The corpus rewrote some addresses** to `spamassassin.taint.org`, for example `rhn-admin@rhn.spamassassin.taint.org`, which can make `legit_sender` misjudge a real company.
- **Step 04's question count.** 3 questions per email instead of 1, so a batch uses about 5.0k input and 600 output tokens, compared with 4.1k and 200 for step 03.
- **The model is pinned to `jev-1.14.0`** in `spam/jev.py`. Aliases like `jev-latest` and `jev-preview` move when a new release ships, and the expected numbers would drift with them. Re-run the dry run before you bump it.
- **`spam/__init__.py` makes `print` replace characters the terminal can't encode.** Without it, scripts crash on Windows when a coding agent pipes their output, because old spam is full of odd characters.

## References

- [typesafe.ai](https://typesafe.ai/)
- [jev introduction](https://docs.typesafe.ai/introduction)
- [Don't call it a decision model](https://typesafe.ai/blog/dont-call-it-a-decision-model): judgments vs. decisions, the idea step 04 is built on
- [Models and aliases](https://docs.typesafe.ai/go/models.md)

## How the data was prepared

- **Corpus.** The [SpamAssassin public corpus](https://spamassassin.apache.org/old/publiccorpus/). Only the latest release of each partition is used, because later releases fix and replace earlier ones (`latest_releases` in `spam/corpus.py`): `20030228_{easy_ham, easy_ham_2, hard_ham, spam}` and `20050311_spam_2`. That leaves 6045 emails. `spam_2/00471.df77…` is gone from both `spam_2` archives. Its 7000-parameter `Content-Type` header trips ClamAV's `Heuristics.Limits.Exceeded.EmailMIMEArguments`, which corporate antivirus such as Cisco AMP flags and quarantines.
- **Splits.** `split.py` draws 20 emails per partition for each set with seed 42. The two sets are disjoint, and each has 60 ham and 40 spam. They're committed in `splits/`. Re-running `split.py` with another `PER_PARTITION` redraws **both** sets, and the quiz IDs in steps 00 and 03 may no longer be in train.
- **Output.** `solve.py` writes per-email scores to `out/<set>.jsonl`, which is gitignored.
