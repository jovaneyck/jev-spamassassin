# 1. Setup (10 min)

[← Agenda](../README.md) · [Next: Meet the data →](02-meet-the-data.md)

## Do

1. Install the dependencies:

   ```
   uv sync
   ```

2. Copy `.env.example` to `.env` and replace `<api_key_here>` with your key:

   ```
   API_KEY=apikey_...
   ```

3. Unpack the corpus:

   ```
   uv run extract.py
   ```

4. Say hello to Jev:

   ```
   uv run hello_jev.py
   ```

5. Run the unit tests:

   ```
   uv run pytest
   ```

## ✅ Checkpoint

- `extract.py` printed nine `dataset/...` folders.
- `hello_jev.py` printed an answer to `is_greeting` with a `noul` larger than 0.5.
- `pytest` printed `23 passed`.

If any of these failed, raise your hand before you continue.

## 🧠 Self-check

Answer each question for yourself before you open it.

<details>
<summary>`hello_jev.py` fails with an authentication error. What do you check first?</summary>

That `.env` sits in the repo root (next to `.env.example`) and that `<api_key_here>` was replaced with your `apikey_...` key.

</details>

<details>
<summary>Why does your API key go in `.env` and not in the code?</summary>

`.env` is gitignored, so the key never ends up in a commit.

</details>

<details>
<summary>Open `hello_jev.py`. What did it send to Jev, and what came back?</summary>

It sent a `state` (one sentence) and `questions` (one Noul named `is_greeting`, with instructions that point at `` `state` ``). It got back `answers`, keyed by question name: each Noul answer is a number between 0.0 (no) and 1.0 (yes).

</details>

<details>
<summary>You get a number between 0 and 1 back. What do you typically do with it?</summary>

Turn it into a decision with a threshold (in this workshop: 0.5 or higher means spam), or use it to rank items, most likely yes first. `solve.py` does both: accuracy, precision and recall use the threshold, and AUC uses the ranking.

</details>

[Next: Meet the data →](02-meet-the-data.md)
