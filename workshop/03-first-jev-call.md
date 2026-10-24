# 3. Your first Jev call (10 min)

[← Meet the data](02-meet-the-data.md) · [Agenda](../README.md) · [Next: Ten emails, one request →](04-batching.md)

## Read

A Jev request has two parts:

- **`state`**: what Jev looks at. Here that's one email.
- **`questions`**: what you ask about it. A **Noul** is a yes/no question. Its answer is a number between 0 (no) and 1 (yes).

A question refers to things in `state` by name, between backticks: `` `email` ``.

## Do

1. Create `first_call.py`:

   ```python
   import os
   from pathlib import Path

   from dotenv import load_dotenv
   from typesafe_sdk import Noul, TypeSafeClient

   from spam.message import summary

   load_dotenv()

   email = summary(Path("dataset/20030228_hard_ham/00177.81236553338cae51575b54c6a07426f9").read_bytes())
   print(email)

   with TypeSafeClient(api_key=os.environ["API_KEY"], timeout=60) as client:
       result = client.system_one(
           state={"email": email},
           questions={"spam": Noul(instructions="Is `email` spam: unsolicited bulk or commercial email?")},
           model="jev-preview",
       )
       print(result.answers["spam"].noul)
   ```

2. Run it:

   ```
   uv run first_call.py
   ```

## ✅ Checkpoint

The last line is a number close to **0.95**: Jev is sure it's spam.

But this email is from `hard_ham`: Ryanair travel insurance, sent to a customer who signed up for it. Keep it in mind for step 6.

[Next: Ten emails, one request →](04-batching.md)
