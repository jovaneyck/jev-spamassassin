<img src="img/sticker-00.svg" align="right" width="170" alt="Inbox archaeology. Est. 2002.">

# 00 Boot up (10 min)

[← Agenda](../README.md) · [Next: 01 Ask →](01-ask.md)

**TL;DR.** Install everything, say hello to Jev, then play *Spam or not?* against the room. Run `uv run hello_jev.py` and look for a number above 0.5.

Welcome to 2002. Your modem screams when it connects, and someone keeps emailing you about a free paysite. The SpamAssassin project collected thousands of these emails and labelled every one. You're going to dig through them.

## Driving with an agent?

Paste this:

```
I'm doing step 00 of the workshop in workshop/00-boot-up.md. Run the commands in its "Do" section one at a
time, except creating .env: I'll do that myself. Stop at the first failure and explain it to me. Then create
peek.py from "Meet the data" exactly as written. Don't run anything on the test set and don't tell me the
answers to the "Spam or not?" quiz.
```

## Do

1. Install the dependencies:

   ```
   uv sync
   ```

2. Copy `.env.example` to `.env`. This works in PowerShell and bash:

   ```
   cp .env.example .env
   ```

   Then open `.env` and replace `<api_key_here>` with the key Jo gave you:

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

## Meet the data

The corpus comes in five partitions:

| Partition    | Label | What's in it                                                            |
| ------------ | ----- | ----------------------------------------------------------------------- |
| `easy_ham`   | ham   | Personal mail and mailing-list chatter                                  |
| `easy_ham_2` | ham   | More of the same                                                        |
| `hard_ham`   | ham   | **The imposters.** Legit newsletters and shop mail that look like spam. |
| `spam`       | spam  | Real spam, 2002 vintage                                                 |
| `spam_2`     | spam  | More real spam                                                          |

`splits/train.txt` and `splits/test.txt` each list 100 emails, 20 from every partition, so 60 ham and 40 spam. The two sets don't share any emails.

- **Train** is your playground. You and your agent can look at it as much as you like.
- **Test** is a sealed envelope. You open it once, in step 05. Until then, don't look at it and don't let your agent peek either.

Create `peek.py`. Give it a piece of a path and it digs through the train set. One match prints the whole email. Several matches print a list of subjects.

```python
import sys
from pathlib import Path

from spam.message import summary

matches = [Path(line) for line in Path("splits/train.txt").read_text().splitlines() if sys.argv[1] in line]
for path in matches:
    email = summary(path.read_bytes())
    if len(matches) == 1:
        print(f"From:    {email['from']}\nSubject: {email['subject']}\n\n{email['body']}")
    else:
        print(f"{path.name[:5]}  {email['subject'][:70]}")
```

## Spam or not?

Five emails from the train set. Jo puts them on the big screen and the room votes with raised hands. On your own? Peek at each one and write down *spam* or *ham*.

```
uv run peek.py 00572
uv run peek.py 00895
uv run peek.py 00237
uv run peek.py 00408
uv run peek.py 00276
```

Keep your answers. In step 03 you'll find out whether Jev beats you.

<details>
<summary>Answers. Vote first.</summary>

| Email   | Label | Partition                                                                |
| ------- | ----- | ------------------------------------------------------------------------ |
| `00572` | ham   | `easy_ham`. Someone on a mailing list showing off scrambled spelling.    |
| `00895` | spam  | `spam_2`. A Lagos barrister needs a trustworthy stranger. Classic.       |
| `00237` | ham   | `hard_ham`. Jeff Bezos announcing Amazon's apparel store to a customer.  |
| `00408` | spam  | `spam_2`. A recruiting agency's "newsletter" that nobody signed up for.  |
| `00276` | spam  | `spam`. "Did I give you the money yet?" No. Nobody ever did.             |

</details>

## Spam hall of fame

This one runs all workshop long. List the subjects of the 40 train spams:

```
uv run peek.py spam
```

Found a gem? Post it on the hall-of-fame board Jo shares. Jo crowns the winner in step 05.

## Checkpoint

- `extract.py` printed nine `dataset` folders, each with a file count.
- `hello_jev.py` printed an answer to `is_greeting` with a `noul` above 0.5, something like `{'is_greeting': NoulAnswer(type='noul', noul=0.79)}`.
- `pytest` printed `27 passed`.
- You've voted on all five quiz emails.

If any of these failed, raise your hand before you continue.

🏅 **Badge unlocked: Hello, Jev.**

## Brain on

Answer for yourself, then open the answer.

<details>
<summary>Jev sends back a number between 0 and 1. What do you think it means, and what would you do with it?</summary>

0 means no, 1 means yes, and everything in between is how strongly Jev leans. To act on it, draw a line. In this workshop 0.5 or higher means spam. You can also sort by it and look at the most likely spam first.

</details>

<details>
<summary>Why are the imposters in <code>hard_ham</code> the interesting partition for a spam filter?</summary>

They're real mail that looks like spam. Those are the emails a filter is most likely to bin by mistake, and binning real mail is the expensive mistake.

</details>

### Deep cuts

<details>
<summary><code>hello_jev.py</code> fails with an authentication error. What do you check first?</summary>

That `.env` sits in the repo root next to `.env.example`, and that you replaced `<api_key_here>` with your `apikey_...` key.

</details>

<details>
<summary>Why does your API key go in <code>.env</code> and not in the code?</summary>

`.env` is gitignored, so the key never ends up in a commit.

</details>

<details>
<summary>Open <code>hello_jev.py</code>. What did it send to Jev, and what came back?</summary>

It sent a `state`, one sentence, and `questions`, one yes/no question named `is_greeting` whose instructions point at `` `state` ``. It got back `answers`, keyed by question name. Each yes/no answer is a number between 0.0 and 1.0.

</details>

<details>
<summary>Jev only sees the sender, the subject and the first 2000 characters of the body. What do you gain and what do you lose?</summary>

You gain smaller, cheaper requests. You lose every other header, including `List-Unsubscribe`, which newsletters you signed up for usually carry. Step 04 brings that header back, through code.

</details>

<details>
<summary>Why shouldn't you run Jev on the test set while you're still improving the filter?</summary>

Every test result you react to shapes your questions a little. After a few rounds the test score tells you how well you fitted those 100 emails, not how the filter does on email it has never seen. Step 05 goes into it.

</details>

[Next: 01 Ask →](01-ask.md)
