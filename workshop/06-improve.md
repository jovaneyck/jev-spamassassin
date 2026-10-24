# 6. Improve the question (15 min)

[← Measure the baseline](05-baseline.md) · [Agenda](../README.md) · [Next: Check on the test set →](07-test-set.md)

## Read

A Noul can take **criteria**: a description of what counts as yes (`true`) and what counts as no (`false`). Instead of a one-line definition, you tell Jev where the line is, using what you saw in step 5.

## Do

1. In `spam/jev.py`, add `CRITERIA` right below `GROUP`:

   ```python
   GROUP = 10  # emails per request
   CRITERIA = {
       "true": "Unsolicited bulk email the recipient never asked for: scams, get-rich-quick offers, pills, adult content.",
       "false": "Personal mail, mailing-list discussion, and newsletters or shop mail the recipient subscribed to, "
       "even when they advertise products.",
   }
   ```

2. In `request`, replace the question:

   ```python
   f"{key}.spam": Noul(instructions=f"Is `emails.{key}` spam: unsolicited bulk or commercial email?")
   ```

   with:

   ```python
   f"{key}.spam": Noul(instructions=f"Is `emails.{key}` spam?", criteria=CRITERIA)
   ```

3. Check that you didn't break anything:

   ```
   uv run pytest
   ```

4. Run the train set again and add the numbers to your table:

   ```
   uv run solve.py train
   uv run misses.py
   ```

## ✅ Checkpoint

`23 passed`, and then:

| | auc | accuracy | precision | recall | hard_ham accuracy |
|---|---|---|---|---|---|
| Baseline (expected) | 0.98 | 0.91 | 0.82 | 1.00 | 0.55 |
| Criteria (expected) | 1.00 | 0.97 | 0.97 | 0.96 | 0.95 |
| **Yours** | | | | | |

Precision went up a lot and recall dropped a little: a spam or two now slips through. For a spam filter, that's usually the right trade.

[Next: Check on the test set →](07-test-set.md)
