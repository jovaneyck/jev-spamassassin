# 5. Measure the baseline (10 min)

[← Ten emails, one request](04-batching.md) · [Agenda](../README.md) · [Next: Improve the question →](06-improve.md)

## Read

`solve.py` classifies a set and prints:

| Metric | Meaning |
|---|---|
| `auc` | Chance that a random spam scores higher than a random ham. 1.0 means the ranking is perfect. |
| `accuracy` | Share of emails labelled correctly at threshold 0.5. |
| `precision` | Share of emails flagged as spam that really are spam. Low precision means real mail lands in the spam folder: **the costly mistake**. |
| `recall` | Share of the spam that got flagged. |

## Do

1. Run the solver on the train set:

   ```
   uv run solve.py train
   ```

2. **Write down** the five numbers (`auc`, `accuracy`, `precision`, `recall` and `hard_ham` accuracy) in a notes file or on paper. Step 6 overwrites this run, and you'll compare against these numbers in steps 6 and 7.

3. Create `misses.py` to list the ham that was flagged as spam:

   ```python
   import json
   from pathlib import Path

   from spam.message import summary

   for line in Path("out/train.jsonl").read_text().splitlines():
       row = json.loads(line)
       if not row["is_spam"] and row["spam"] >= 0.5:
           email = summary(Path(row["email"]).read_bytes())
           print(f"{row['spam']:.2f}  {email['from'][:40]:40}  {email['subject'][:60]}")
   ```

4. Run it:

   ```
   uv run misses.py
   ```

## ✅ Checkpoint

Your numbers should be close to these (Jev's answers vary a little from run to run):

| | auc | accuracy | precision | recall | hard_ham accuracy |
|---|---|---|---|---|---|
| Expected | 0.98 | 0.91 | 0.82 | 1.00 | 0.55 |

Every miss is a **newsletter or shop mail** that the recipient subscribed to: CNET, Amazon, Ryanair. The question asks about "commercial email", so Jev calls them spam.

[Next: Improve the question →](06-improve.md)
