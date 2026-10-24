import pytest

from spam.metrics import Scored, auc, confusion


def scored(is_spam: bool, score: float, partition: str = "spam") -> Scored:
    return Scored(partition=partition, is_spam=is_spam, score=score)


class TestAuc:
    def test_perfect_separation_is_one(self):
        assert auc([scored(True, 0.9), scored(False, 0.1)]) == 1.0

    def test_inverted_separation_is_zero(self):
        assert auc([scored(True, 0.1), scored(False, 0.9)]) == 0.0

    def test_ties_count_half(self):
        assert auc([scored(True, 0.5), scored(False, 0.5)]) == 0.5


class TestConfusion:
    EMAILS = [scored(True, 0.9), scored(True, 0.2), scored(False, 0.7), scored(False, 0.1), scored(False, 0.0)]

    def test_counts_spam_at_or_above_the_threshold(self):
        c = confusion(self.EMAILS, threshold=0.7)
        assert (c.true_positives, c.false_positives, c.false_negatives, c.true_negatives) == (1, 1, 1, 2)

    def test_rates(self):
        c = confusion(self.EMAILS, threshold=0.7)
        assert c.accuracy == pytest.approx(3 / 5)
        assert c.precision == pytest.approx(1 / 2)
        assert c.recall == pytest.approx(1 / 2)

    def test_no_spam_flagged_has_full_precision(self):
        assert confusion([scored(True, 0.1)], threshold=0.5).precision == 1.0

    def test_no_spam_present_has_full_recall(self):
        assert confusion([scored(False, 0.1)], threshold=0.5).recall == 1.0
