"""The SpamAssassin public corpus (dataset/<release>_<partition>/), labelled by partition."""

import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

SPAM = {"spam", "spam_2"}
SEED = 42


@dataclass(frozen=True)
class Email:
    path: Path
    partition: str  # easy_ham, easy_ham_2, hard_ham, spam or spam_2
    is_spam: bool


def latest_releases(root: Path) -> dict[str, Path]:
    """Later releases of a partition fix and replace earlier ones, e.g. 20050311_spam_2 replaces 20030228_spam_2."""
    folders = sorted(p for p in root.iterdir() if p.is_dir())
    return {folder.name.split("_", 1)[1]: folder for folder in folders}


def load(root: Path) -> list[Email]:
    return [
        Email(path=path, partition=partition, is_spam=partition in SPAM)
        for partition, folder in sorted(latest_releases(root).items())
        for path in sorted(folder.iterdir())
        if path.name != "cmds"
    ]


def split(emails: list[Email], per_partition: int, seed: int = SEED) -> tuple[list[Email], list[Email]]:
    """Disjoint train and test sets, each with `per_partition` random messages from every partition."""
    partitions: dict[str, list[Email]] = defaultdict(list)
    for email in emails:
        partitions[email.partition].append(email)
    rng = random.Random(seed)
    picks = {name: rng.sample(members, 2 * per_partition) for name, members in sorted(partitions.items())}
    return (
        [e for picked in picks.values() for e in picked[:per_partition]],
        [e for picked in picks.values() for e in picked[per_partition:]],
    )
