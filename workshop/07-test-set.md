# 7. Check on the test set (5 min)

[← Improve the question](06-improve.md) · [Agenda](../README.md)

## Read

### Why a separate test set?

A spam filter is only useful on email it hasn't seen yet: tomorrow's inbox. You can't measure tomorrow's inbox, so you keep part of today's email aside and pretend it's tomorrow. That's the **test set**.

Think of an exam. If the students get the exam questions to practise with, a perfect score proves they memorised the answers, not that they understand the material. The **train set** is the practice questions: look at it, learn from it, tune on it. The test set is the exam: you take it once, at the end.

### Overfitting

In step 6 you read the train misses (CNET, Amazon, Ryanair) and wrote criteria about "newsletters or shop mail the recipient subscribed to". Those criteria capture a real pattern, but they were also shaped by those particular emails. Part of your train gain comes from **fitting the emails you looked at** rather than spam in general. That's **overfitting**: a change that looks better on the data you tuned on than it really is.

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

Your test numbers should be close to the **Test, criteria** row. You didn't run the baseline on test (that saves 10 requests), so the **Test, baseline** row comes from the facilitator's run:

| Set | accuracy | precision | hard_ham accuracy |
|---|---|---|---|
| Train, baseline | 0.91 | 0.82 | 0.55 |
| Train, criteria | 0.97 | 0.97 | 0.95 |
| Test, baseline (facilitator's run) | 0.93 | 0.85 | 0.70 |
| Test, criteria | 0.94 | 0.89 | 0.80 |

On train, accuracy went up by 0.06 and `hard_ham` went from 11 to 19 correct out of 20. On test, accuracy went up by 0.01 (one email) and `hard_ham` from 14 to 16 correct. The criteria probably still help, but most of the train gain didn't carry over: **that's overfitting, measured.** The test numbers are what you can honestly expect on new email.

## Takeaways

- **`state` holds the data, questions point into it.** Name things once and refer to them with backticks.
- **Batch to share the per-request overhead.** 10 emails per request used 37% fewer input tokens, at the price of the trade-offs listed in step 4.
- **Measure before you change anything**, then read the misses. They tell you what to change.
- **Criteria draw the line** between yes and no better than a one-line definition does.
- **Keep a test set you don't look at.** The train score tells you what you tuned for. The test score tells you what to expect on new email.

[Next: Exploring further →](08-exploring-further.md) · [← Back to the agenda](../README.md)
