from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Scored:
    partition: str
    is_spam: bool
    score: float


def auc(emails: list[Scored]) -> float:
    """Probability that a random spam outscores a random ham."""
    positives = [e.score for e in emails if e.is_spam]
    negatives = [e.score for e in emails if not e.is_spam]
    wins = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p, n in product(positives, negatives))
    return wins / (len(positives) * len(negatives))


@dataclass(frozen=True)
class Confusion:
    true_positives: int
    false_positives: int
    false_negatives: int
    true_negatives: int

    @property
    def accuracy(self) -> float:
        return (self.true_positives + self.true_negatives) / (
            self.true_positives + self.false_positives + self.false_negatives + self.true_negatives
        )

    @property
    def precision(self) -> float:
        """Share of flagged emails that are spam; ham in the spam folder is the costly mistake."""
        flagged = self.true_positives + self.false_positives
        return self.true_positives / flagged if flagged else 1.0

    @property
    def recall(self) -> float:
        spam = self.true_positives + self.false_negatives
        return self.true_positives / spam if spam else 1.0


def confusion(emails: list[Scored], threshold: float) -> Confusion:
    flagged = [e.score >= threshold for e in emails]
    count = lambda spam, flag: sum(e.is_spam == spam and f == flag for e, f in zip(emails, flagged))  # noqa: E731
    return Confusion(count(True, True), count(False, True), count(True, False), count(False, False))
