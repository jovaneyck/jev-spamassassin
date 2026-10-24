# 4. Ten emails, one request (5 min)

[← Your first Jev call](03-first-jev-call.md) · [Agenda](../README.md) · [Next: Measure the baseline →](05-baseline.md)

## Read

You pay for Jev per token, not per request. So why batch?

Every request carries a **fixed overhead** of about 260 input tokens: the framing Jev wraps around your `state` and `questions`. An email averages about 400 tokens, so asking about one email per request spends a big share of its tokens on that overhead. Put 10 emails in one request and you pay the overhead once instead of 10 times.

Measured on the first 10 train emails:

| | Input tokens | Output tokens |
|---|---|---|
| 10 requests, 1 email each | 6501 | 230 |
| 1 request, 10 emails | 4127 | 195 |

That's **37% fewer input tokens** for the same 10 answers.

Open `spam/jev.py` to see how it's done:

- `request` puts the emails in `state` under `e1` … `e10`.
- It asks one question per email, named `e1.spam` … `e10.spam`, and each one points at its own email: `` `emails.e3` ``.
- `read` collects the answers back in request order.
- `GROUP = 10` sets how many emails go into one request.

## Do

1. Run the batching tests:

   ```
   uv run pytest tests/test_jev.py -v
   ```

2. Read the three test names and match each one to the bullets above.

## ✅ Checkpoint

`3 passed`. You can explain why the question for email 3 says `` `emails.e3` `` and not `` `email` ``.

## Trade-offs

Batching isn't free:

- **The saving depends on the ratio.** Short emails, or a large context that every email shares (instructions, examples, reference images), make batching worth more. With long emails the overhead is small next to the email, and so is the saving.
- **Only `state` is shared.** Anything you attach to each question, such as instructions or criteria, is repeated once per email in the batch. To share it, put it in `state` once and refer to it by name.
- **Emails can influence each other.** A spammy neighbour might pull a borderline ham up. Bigger batches give more room for that.
- **Failures are coarser.** If a request fails or times out, you lose 10 answers instead of 1.
- **Bigger isn't always better.** Very large batches can hit output limits or lower answer quality.

### Optional: explore it yourself after the workshop

Every response reports its own token counts in `result.usage.input_tokens` and `result.usage.output_tokens`. Some experiments to try:

- Measure the overhead yourself: send the same emails one per request and then batched, and compare the totals.
- Run the train set with `GROUP` at 1, 5, 10 and 20, and plot tokens against accuracy. Where does quality start to drop?
- After step 6, move `CRITERIA` from the questions into `state`, refer to it from each question, and measure the tokens saved.
- Shuffle the train set so each email gets different neighbours, run it twice, and compare the answers to see how much the neighbours matter.

[Next: Measure the baseline →](05-baseline.md)
