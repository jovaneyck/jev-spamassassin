# 8. Exploring further (after the workshop)

[← Check on the test set](07-test-set.md) · [Agenda](../README.md)

In step 6 you made one change and measured it. **Hill-climbing** is doing that over and over: make one small change, measure it on train, keep it if it helps, revert it if it doesn't.

## Hill-climbing by hand

1. **Measure the noise first.** Run `uv run solve.py train` twice without changing anything. The difference between the two runs is your noise floor. On 100 emails one email is worth 0.01 accuracy, and identical runs already differ by about 0.01, so ignore any gain smaller than 0.02–0.03.
2. **Change one thing at a time.** If you change two things and the score moves, you don't know which one did it.
3. **Read the misses** (`uv run misses.py`) before you pick the next change. Guessing is more expensive than looking.
4. **Keep a log.** Write every experiment, its numbers and your verdict in `hillclimb.md`. Failed experiments are the most useful part of that log: they stop you from trying the same thing twice.
5. **Watch the cost.** Each train run costs 10 requests. Look at `result.usage` (see [step 4](04-batching.md)) whenever a change adds tokens.
6. **Touch the test set only at the end**, once. Every look at it makes it less of a test.

### Ideas to climb with

- Pick the threshold that maximises accuracy on train instead of using 0.5.
- Ask the question in three different wordings and average the answers.
- Show Jev a few labelled train emails as examples in `state`.
- Send headers like `List-Unsubscribe` along with the email: subscribed newsletters usually have them.
- Move `CRITERIA` out of the questions and into `state`, so a batch doesn't repeat it 10 times.
- Try `GROUP` at 5 and 20 and compare tokens against accuracy.

### Watch out for overfitting

With 100 emails you'll fit train quickly. Step 7 already showed it: +0.06 accuracy on train, +0.01 on test. To climb on more emails, raise `PER_PARTITION` in `split.py` and run `uv run split.py` again. That redraws **both** sets, so do it before you've looked at the new test set.

## Let Claude climb for you

Hill-climbing is a loop with a clear metric, which makes it a good job for a coding agent. Start Claude Code in this folder and give it a prompt with firm rules:

```
Hill-climb the spam filter in this repo on the train set.

Loop:
1. Run `uv run solve.py train` twice to measure the noise floor.
2. Read the misses in out/train.jsonl and pick ONE change to spam/jev.py or spam/message.py.
3. Keep `uv run pytest` green: write or adapt tests for every change.
4. Run `uv run solve.py train`. Keep the change only if it beats the best score by more than the noise floor.
   Otherwise revert it.
5. Log the experiment, its numbers and your verdict in hillclimb.md, then go back to step 2.

Rules:
- Never run `solve.py test` and never read splits/test.txt or out/test.jsonl.
- Optimise accuracy, but never let precision drop below its baseline.
- Stop after 20 train runs (200 Jev requests) or 3 experiments in a row without a gain.
- Commit every kept change with git, so I can review the climb step by step.
```

Then review the result yourself:

- **Read `hillclimb.md`.** Do the kept changes make sense, or did Claude fit a handful of train emails? A rule that names a specific sender is a red flag.
- **Run the test set once** (`uv run solve.py test`) and compare it with your step-7 numbers.
- **Enforce the rules yourself.** A rule in a prompt is a request, not a guarantee. To be sure Claude can't peek, move `splits/test.txt` out of the folder before you start and put it back when it's done.

[← Back to the agenda](../README.md)
