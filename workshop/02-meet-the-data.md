# 2. Meet the data (5 min)

[← Setup](01-setup.md) · [Agenda](../README.md) · [Next: Your first Jev call →](03-first-jev-call.md)

## Read

The corpus has five partitions:

| Partition | Label | What's in it |
|---|---|---|
| `easy_ham` | ham | Personal mail and mailing-list discussion |
| `easy_ham_2` | ham | The same, collected later |
| `hard_ham` | ham | Legitimate mail that **looks** like spam: newsletters, shop mail |
| `spam` | spam | Spam |
| `spam_2` | spam | Spam, collected later |

`splits/train.txt` and `splits/test.txt` each list 100 emails: 20 from every partition, so 60 ham and 40 spam. The two sets don't overlap.

- **Train** is your playground. Look at it as much as you like.
- **Test** is for the final check in step 7. Don't look at it before then.

## Do

1. Create `peek.py`:

   ```python
   import sys
   from pathlib import Path

   from spam.message import summary

   for line in Path("splits/train.txt").read_text().splitlines():
       if sys.argv[1] in line:
           print(summary(Path(line).read_bytes()))
           break
   ```

2. Look at the first email of three partitions:

   ```
   uv run peek.py easy_ham/
   uv run peek.py hard_ham/
   uv run peek.py _spam/
   ```

## ✅ Checkpoint

You've seen three emails, each with only `from`, `subject` and `body`. Jev never sees the other headers, and it only gets the first 2000 characters of the body, which keeps requests cheap.

Can you tell which one is the hard ham without looking at the partition name?

## 🧠 Self-check

Answer each question for yourself before you open it.

<details>
<summary>Why is `hard_ham` the interesting partition for a spam filter?</summary>

It's legitimate mail that looks like spam (newsletters, shop mail). Those are the emails a filter is most likely to flag by mistake.

</details>

<details>
<summary>Jev only sees `from`, `subject` and the first 2000 characters of the body. What's gained and what's lost?</summary>

Gained: smaller, cheaper requests. Lost: every other header, including signals like `List-Unsubscribe` that subscribed newsletters usually carry.

</details>

<details>
<summary>Why shouldn't you run Jev on the test set while you're still building and improving the classifier?</summary>

Every test result you react to shapes your questions and criteria a little. After a few rounds, the test score tells you how well you fitted those 100 emails, not how the filter does on email it has never seen. Step 7 covers this.

</details>

[Next: Your first Jev call →](03-first-jev-call.md)
