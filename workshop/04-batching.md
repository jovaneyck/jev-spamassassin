# 4. Ten emails, one request (5 min)

[← Your first Jev call](03-first-jev-call.md) · [Agenda](../README.md) · [Next: Measure the baseline →](05-baseline.md)

## Read

One request per email costs 100 requests per set. Instead, the solver puts **10 emails in one request** and asks one question per email. Open `spam/jev.py`:

- `request` puts the emails in `state` under `e1` … `e10`.
- It asks one question per email, named `e1.spam` … `e10.spam`, and each one points at its own email: `` `emails.e3` ``.
- `read` collects the answers back in request order.
- `GROUP = 10` sets how many emails go into one request.

So one set of 100 emails costs **10 requests**.

## Do

1. Run the batching tests:

   ```
   uv run pytest tests/test_jev.py -v
   ```

2. Read the three test names and match each one to the bullets above.

## ✅ Checkpoint

`3 passed`. You can explain why the question for email 3 says `` `emails.e3` `` and not `` `email` ``.

[Next: Measure the baseline →](05-baseline.md)
