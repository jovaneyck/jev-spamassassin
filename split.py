"""Write the train and test sets as lists of corpus paths, so every run scores the same emails.

Run:
    uv run split.py     (once; writes splits/train.txt and splits/test.txt)
"""

from pathlib import Path

from spam.corpus import load, split

CORPUS = Path("dataset")
SPLITS = Path("splits")
PER_PARTITION = 20  # x 5 partitions = 100 emails per set, 10 Jev requests per run


def main() -> None:
    train, test = split(load(CORPUS), PER_PARTITION)
    SPLITS.mkdir(exist_ok=True)
    for name, emails in {"train": train, "test": test}.items():
        (SPLITS / f"{name}.txt").write_text("".join(f"{e.path.as_posix()}\n" for e in emails))
        print(f"{name}: {len(emails)} emails, {sum(e.is_spam for e in emails)} spam")


if __name__ == "__main__":
    main()
