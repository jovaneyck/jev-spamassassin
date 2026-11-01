# 3. Your first Jev call (10 min)

[← Meet the data](02-meet-the-data.md) · [Agenda](../README.md) · [Next: Ten emails, one request →](04-batching.md)

## Read

A Jev request has two parts:

- **`state`**: what Jev looks at. Here that's one email.
- **`questions`**: what you ask about it. A **Noul** is a yes/no question. Its answer is decimal number between 0.0 (no) and 1.0 (yes). Jev supports different kinds of questions which might be interesting to look at later in the workshop.

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

The last line is a number close to **0.95**: Jev is preeeetty sure it's spam.

But this email is from `hard_ham`: Ryanair travel insurance, sent to a customer who signed up for it. Keep it in mind for step 6.

## 🧠 Self-check

Answer each question for yourself before you open it.

<details>
<summary>What goes in `state` and what goes in `questions`?</summary>

`state` holds the data Jev looks at (the email). `questions` holds what you ask about it (here one Noul).

</details>

<details>
<summary>How does the question know which email to look at?</summary>

It names a key in `state` between backticks: `` `email` ``.

</details>

<details>
<summary>Jev answered 0.95. Does that mean 95 out of 100 emails like this one are spam?</summary>

Not necessarily. 0.95 means Jev leans strongly towards yes. Whether 95% of emails scored 0.95 really are spam is something you have to measure on labelled data. This email scored 0.95 and is ham: a confident answer can still be wrong, because Jev answers the question as you asked it.

</details>

<details>
<summary>In practice, what would you do with emails scored 0.95, 0.55 and 0.05?</summary>

Pick a threshold and act on it: with 0.5, the first two go to the spam folder and the last one to the inbox. The 0.55 sits close to the line, so a small change in wording or a rerun can flip it. You could send borderline scores to a "maybe spam" folder, or move the threshold up to protect real mail. Where to put the line depends on which mistake costs more (step 5).

</details>

<details>
<summary>Why did Jev call a legitimate Ryanair email spam?</summary>

The question defines spam as "unsolicited bulk **or commercial** email". A subscribed travel-insurance mail is commercial, so by the question's own definition it qualifies. The question is the problem, not Jev.

</details>

[Next: Ten emails, one request →](04-batching.md)
