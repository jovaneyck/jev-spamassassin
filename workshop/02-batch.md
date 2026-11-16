<img src="img/sticker-02.svg" align="right" width="170" alt="Cover charge paid once.">

# 02 Batch (5 min)

[← 01 Ask](01-ask.md) · [Agenda](../README.md) · [Next: 03 Measure →](03-measure.md)

**TL;DR.** Ten emails in one request cost about as much as six sent one by one. The batching trade-off. 

## Read

Jev bills per token, not per request. So why bother with batching?

Every request has a cover charge of about 260 input tokens. That's the framing Jev wraps around your `state` and `questions`. An average email is about 400 tokens. Send one email per request and you pay the cover charge every single time. Put 10 emails in one request and you pay it once.

The receipt, measured on the first 10 train emails:

|                           | Input tokens | Output tokens |
| ------------------------- | ------------ | ------------- |
| 10 requests, 1 email each | 6501         | 230           |
| 1 request, 10 emails      | 4127         | 195           |

That's **37% fewer input tokens** for the same 10 answers.

Open `spam/jev.py` to see how it works:

- `request` puts the emails in `state` under `e1` … `e10`.
- It asks every question from `questions` once per email, named `e1.spam` … `e10.spam`. Each one points at its own email: `` `emails.e3` ``.
- `read` collects each email's answers by name, in request order.
- `GROUP = 10` sets how many emails share one request.

## Driving with an agent?

Paste this:

```
I'm doing step 02 of the workshop in workshop/02-batch.md. Run the batching tests it mentions. Then walk me
through request() and read() in spam/jev.py using a batch of two emails as the example. Don't change any code.
```

## Do

1. Run the batching tests:

   ```
   uv run pytest tests/test_jev.py -v
   ```

2. Match each of the three test names to the bullet it checks.

## Checkpoint

`3 passed`. You can explain why the question for email 3 says `` `emails.e3` `` and not `` `email` ``.

🏅 **Badge unlocked: Token miser.**

## The small print

Batching isn't free:

- **The saving depends on the ratio.** Short emails make batching worth more. So does a big chunk of context that every email shares, like instructions, examples or reference images. With long emails the cover charge is small next to the email, and so is the saving.
- **Only `state` is shared.** Anything attached to a question, like instructions or criteria, gets repeated once per email in the batch. To share it, put it in `state` once and point at it by name.
- **Emails can rub off on each other.** A spammy email might drag a borderline neighbour in the same request up. Bigger batches give them more room to do that.
- **Failures get bigger.** If a request times out, you lose 10 answers instead of 1.
- **Bigger isn't always better.** Huge batches can hit output limits or get sloppier answers.

Want to measure any of this yourself? The [side quests](side-quests.md#batching-experiments) have experiments.

Done early? Go hunt for the [spam hall of fame](00-boot-up.md#spam-hall-of-fame).

## Brain on

<details>
<summary>Billing is per token, not per request. So where does batching save money?</summary>

Every request carries a cover charge of about 260 input tokens. Ten emails in one request pay it once instead of ten times.

</details>

<details>
<summary>Why does the question for email 3 say <code>`emails.e3`</code> and not <code>`email`</code>?</summary>

`state` now holds ten emails under `emails`, keyed `e1` … `e10`. Each question has to point at its own email.

</details>

### Deep cuts

<details>
<summary>When is batching worth the least?</summary>

With long emails, where the cover charge is small next to the email. And anything attached per question, like instructions or criteria, is repeated per email, so batching doesn't share it.

</details>

<details>
<summary>A batched request times out. What do you lose?</summary>

All 10 answers in it, not just one.

</details>

[Next: 03 Measure →](03-measure.md)
