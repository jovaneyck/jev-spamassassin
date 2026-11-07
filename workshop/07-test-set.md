# 7. Check on the test set (5 min)

[← Split the decision](06-improve.md) · [Agenda](../README.md)

## Read

### Why a separate test set?

A spam filter is only useful on email it hasn't seen yet: tomorrow's inbox. You can't measure tomorrow's inbox, so you keep part of today's email aside and pretend it's tomorrow. That's the **test set**.

Think of an exam. If the students get the exam questions to practise with, a perfect score proves they memorised the answers, not that they understand the material. The **train set** is the practice questions: look at it, learn from it, tune on it. The test set is the exam: you take it once, at the end.

### Overfitting

In step 6 you split the decision into judgments, a fact and a rule. The questions and the rule were chosen by reading the train misses (CNET, Amazon, Ryanair). They capture a real pattern, but they were also shaped by those particular emails. Part of your train gain comes from **fitting the emails you looked at** rather than spam in general. That's **overfitting**: a change that looks better on the data you tuned on than it really is.

The train score can't show you overfitting, because it's measured on the very emails you tuned on. Only emails you never looked at can, so that's what you'll run now.

Two rules follow from this:

- **Tune on train, check on test.** Every time you change something because of a test result, some of the test set leaks into your filter, and the test score becomes as optimistic as the train score.
- **Small sets are noisy.** With 100 test emails, one email is worth 0.01 accuracy, and `hard_ham` has only 20 emails, so one email is worth 0.05 there. Don't read much into differences of one or two emails.

## Do

1. Run the test set once:

   ```
   uv run solve.py test
   ```

2. Compare it with the train numbers you wrote down in steps 5 and 6.

## ✅ Checkpoint

Your test numbers should be close to the **Test, split** row. You didn't run the baseline on test (that saves 10 requests), so the **Test, baseline** row comes from the facilitator's run:

| Set | accuracy | precision | hard_ham accuracy | real mail in the spam folder |
|---|---|---|---|---|
| Train, baseline | 0.92–0.94 | 0.83–0.87 | 0.60–0.70 | 6–8 |
| Train, split | 0.95–0.96 | 0.97–1.00 | 1.00 | 0–1 |
| Test, baseline (facilitator's run) | 0.94 | 0.87 | 0.70 | 6 |
| Test, split | 0.95 | 0.95 | 0.90 | 2 |

The costly mistake dropped on test too: from 6 real emails in the spam folder to 2. That gain is bigger than the noise. It's smaller than on train, though, where it went from 6–8 to 0–1: **that's overfitting, measured.** Accuracy went up by only 0.01 on test, because a few more spam emails now slip through. The test numbers are what you can honestly expect on new email.

Look at what slips through on test. Two of the spam ads carry a `List-Unsubscribe` header, so the rule treats their sender as known. That's the weakness the step 6 self-check asked about, and the train set never showed it. Because the decision is code, you can see exactly which fact let them through.

## Takeaways

- **`state` holds the data, questions point into it.** Name things once and refer to them with backticks.
- **Batch to share the per-request overhead.** 10 emails per request used 37% fewer input tokens, at the price of the trade-offs listed in step 4.
- **Measure before you change anything**, then read the misses. They tell you what to change.
- **Jev makes judgments, code makes decisions.** Small questions plus facts plus a tested rule beat one big question. And when an email goes wrong, the trace shows why.
- **Keep a test set you don't look at.** The train score tells you what you tuned for. The test score tells you what to expect on new email.

## 🧠 Self-check

Answer each question for yourself before you open it.

<details>
<summary>Real mail in the spam folder fell from 6–8 to 0–1 on train, but only from 6 to 2 on test. Why the difference?</summary>

The questions and the rule were chosen after reading the train misses, so part of the train gain is fitting those specific emails: overfitting.

</details>

<details>
<summary>Test accuracy went up by 0.01. Is that proof that splitting the decision helps?</summary>

No. That's one email, well within the run-to-run noise. The fall in false positives (6 to 2) is the more convincing number, and it's the one that matters for a spam filter.

</details>

<details>
<summary>You spot the faked `List-Unsubscribe` headers in the test misses, change the rule and run test again. What went wrong?</summary>

The test set leaked into your tuning. Its score is now as optimistic as the train score, and you need fresh emails for an honest number.

</details>

<details>
<summary>The baseline scored higher on test (0.94) than on train (0.92). Does that matter?</summary>

No. They're different emails, and on 100 emails that's two emails' difference. Small sets are noisy.

</details>

[Next: Exploring further →](08-exploring-further.md) · [← Back to the agenda](../README.md)
