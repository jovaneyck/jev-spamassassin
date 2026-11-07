# 6. Split the decision (20 min)

[← Measure the baseline](05-baseline.md) · [Agenda](../README.md) · [Next: Check on the test set →](07-test-set.md)

## Read

The tempting fix for the misses in step 5 is to keep the one question and add rules to it: "...but not newsletters the recipient subscribed to". That works for a while. Each new miss then gets another clause, and the wording grows until it's tuned to the emails you looked at. TypeSafe calls this **prompt gymnastics**.

The alternative: **Jev makes judgments, code makes decisions.** Read [Don't call it a decision model](https://typesafe.ai/blog/dont-call-it-a-decision-model) (5 min) for how Jev is meant to be used, and how not to use it. In short:

- Ask Jev only small questions that a person could answer at a glance: **judgments**.
- Let code answer what it can answer exactly: **facts**.
- Combine both into the decision **in code**, where you can read it and test it.

"Is this spam?" is a decision. Here it splits into three judgments and one fact:

| Input | From | Question |
|---|---|---|
| `scam` | Jev | Is the email a scam? |
| `advertising` | Jev | Does it advertise a product or service? |
| `legit_sender` | Jev | Is it sent by a named, legitimate company or publication? |
| `list_mail` | code | Does it have a `List-Unsubscribe` or `List-Id` header? (`facts` in `spam/message.py`) |

and one rule: **spam is a scam, or an ad from a sender the recipient doesn't know.** A sender counts as known when it's a legitimate company, or when the mail comes through a mailing list.

The judgments are probabilities, so the rule combines them with the usual fuzzy-logic operators: `and` is `min`, `or` is `max` and `not p` is `1 - p`. With answers of exactly 0 and 1 that's plain boolean logic, and the result is still a score, so AUC keeps working.

## Do

1. In `spam/jev.py`, replace `questions` with:

   ```python
   def questions(email: str) -> dict[str, Noul]:
       """The judgments Jev makes about one email. `email` is that email's path in `state`."""
       return {
           "scam": Noul(
               instructions=f"Is `{email}` a scam?",
               criteria={
                   "true": "It pushes something dubious: miracle pills, get-rich-quick schemes, cheap software, "
                   "prizes, adult content, or asks for bank details.",
                   "false": "An honest message, even when it sells something.",
               },
           ),
           "advertising": Noul(instructions=f"Does `{email}` advertise a product or service?"),
           "legit_sender": Noul(instructions=f"Is `{email}` sent by a named, legitimate company or publication?"),
       }
   ```

2. Write the decision's tests first. Replace `tests/test_decision.py` with:

   ```python
   from spam.decision import spam


   def judged(scam=0.0, advertising=0.0, legit_sender=0.0):
       return {"scam": scam, "advertising": advertising, "legit_sender": legit_sender}


   def test_a_scam_is_spam_even_from_a_legitimate_sender_on_a_mailing_list():
       assert spam(judged(scam=1, legit_sender=1), {"list_mail": True}) == 1


   def test_an_ad_from_an_unknown_sender_is_spam():
       assert spam(judged(advertising=1), {"list_mail": False}) == 1


   def test_an_ad_from_a_legitimate_sender_is_not_spam():
       assert spam(judged(advertising=1, legit_sender=1), {"list_mail": False}) == 0


   def test_an_ad_through_a_mailing_list_is_not_spam():
       assert spam(judged(advertising=1), {"list_mail": True}) == 0


   def test_mail_that_neither_scams_nor_advertises_is_not_spam():
       assert spam(judged(), {"list_mail": False}) == 0


   def test_and_takes_the_lowest_or_takes_the_highest_and_not_flips():
       assert spam(judged(scam=0.2, advertising=0.9, legit_sender=0.3), {"list_mail": False}) == 0.7
   ```

3. Run them and watch them fail:

   ```
   uv run pytest tests/test_decision.py
   ```

4. Make them pass. In `spam/decision.py`, replace `spam` with:

   ```python
   def spam(judgments: dict[str, float], facts: dict[str, bool]) -> float:
       """A scam, or an ad from a sender the recipient doesn't know. and = min, or = max, not = 1 - p."""
       known_sender = 1.0 if facts["list_mail"] else judgments["legit_sender"]
       return max(judgments["scam"], min(judgments["advertising"], 1 - known_sender))
   ```

5. Check that everything is green:

   ```
   uv run pytest
   ```

6. Run the train set again, write down the new numbers next to your baseline numbers from step 5, and compare them:

   ```
   uv run solve.py train
   uv run misses.py
   ```

## ✅ Checkpoint

`32 passed`, and then:

| | auc | accuracy | precision | recall | hard_ham accuracy |
|---|---|---|---|---|---|
| Baseline (expected) | 0.98 | 0.92–0.94 | 0.83–0.87 | 1.00 | 0.60–0.70 |
| Split (expected) | 1.00 | 0.95–0.96 | 0.97–1.00 | 0.90–0.93 | 1.00 |

Every hard ham now stays in the inbox. At most one real email lands in the spam folder: a boingboing RSS item whose `legit_sender` lands on 0.50, a coin flip. A few spam emails slip through: business ads from senders that look legitimate.

`misses.py` now shows **why** each email ended up where it did. You can see which judgment or fact decided it, not just one number.

## 🧠 Self-check

Answer each question for yourself before you open it.

<details>
<summary>Why not fix the baseline by adding "except newsletters the recipient subscribed to" to the question?</summary>

Jev can't see a subscription. It can only guess from the text. And every new miss would add another clause, tuned to the emails you looked at. That's prompt gymnastics: it tends to break on new email and on the next model version.

</details>

<details>
<summary>Why is `list_mail` computed in code instead of asked to Jev?</summary>

Whether a header is there is an exact fact. Code answers it for free and never gets it wrong. Jev doesn't even see the headers (`summary` drops them).

</details>

<details>
<summary>Spammers can fake a `List-Unsubscribe` header. Does that break the rule?</summary>

Not for scams. A scam is spam whatever its headers, which is why `scam` sits outside the `list_mail` check. The train set has two scams posted to a mailing list, and both are still caught. For ads, yes: a faked header makes the sender count as known. Step 7 shows whether that happens on new email.

</details>

<details>
<summary>`pytest` passes. Does that mean the filter got better?</summary>

No. The tests check that the rule does what you meant. Only `solve.py` measures whether what you meant was a good idea.

</details>

<details>
<summary>A spam slips through as an ad from a "legitimate" sender. How would you fix it without rewording the questions?</summary>

Add a judgment or a fact, and a path in the rule that uses it. For example, ask whether the email is written to the recipient as an existing customer or subscriber. The existing judgments don't change: Jev answers each question on its own, so a new one can't disturb the ones you already measured.

</details>

[Next: Check on the test set →](07-test-set.md)
