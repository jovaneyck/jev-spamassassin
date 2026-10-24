# 7. Check on the test set (5 min)

[← Improve the question](06-improve.md) · [Agenda](../README.md)

## Read

You wrote the criteria **after looking at the train misses**. Does the improvement hold on emails you've never seen?

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

The criteria still help on test, but the gain is much smaller than on train. Part of the train gain was **fitting the emails you looked at**. That's why you climb on train and only check on test. Once you start tuning on test, it stops being a test.

## Takeaways

- **`state` holds the data, questions point into it.** Name things once and refer to them with backticks.
- **Batch to share the per-request overhead.** 10 emails per request used 37% fewer input tokens, at the price of the trade-offs listed in step 4.
- **Measure before you change anything**, then read the misses. They tell you what to change.
- **Criteria draw the line** between yes and no better than a one-line definition does.
- **Keep a test set you don't look at.**

[Next: Exploring further →](08-exploring-further.md) · [← Back to the agenda](../README.md)
