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
- `hello_jev.py` printed an answer to `is_greeting` with a `noul` close to 1.
- `pytest` printed `23 passed`.

If any of these failed, raise your hand before you continue.

[Next: Meet the data →](02-meet-the-data.md)
