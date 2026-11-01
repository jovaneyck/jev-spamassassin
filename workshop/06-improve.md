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

4. Run the train set again, write down the new numbers next to your baseline numbers from step 5, and compare them:

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

Precision went up a lot and recall dropped a little: a spam or two now slips through. For a spam filter, that's usually the right trade.

## 🧠 Self-check

Answer each question for yourself before you open it.

<details>
<summary>What do criteria give Jev that the one-line question didn't?</summary>

An explicit boundary: what counts as yes and what counts as no, including the case the question got wrong (subscribed commercial mail is a no).

</details>

<details>
<summary>`pytest` passes. Does that mean the filter got better?</summary>

No. The tests check that requests are built and answers read correctly. Only `solve.py` measures quality.

</details>

<details>
<summary>Why did recall drop a little?</summary>

The criteria narrow what counts as spam. A spam that looks like ordinary shop mail can now land on the "no" side.

</details>

<details>
<summary>Criteria sit in each question. What does that cost per batch, and how would you avoid it?</summary>

They're repeated 10 times per request. Put them in `state` once and refer to them by name from each question.

</details>

[Next: Check on the test set →](07-test-set.md)
