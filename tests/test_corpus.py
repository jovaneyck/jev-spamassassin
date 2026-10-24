from pathlib import Path

from spam.corpus import Email, load, split


def corpus(root: Path, partitions: dict[str, int]) -> Path:
    for name, count in partitions.items():
        (root / name).mkdir()
        (root / name / "cmds").write_text("mv 00001.abc 00001.def")
        for i in range(count):
            (root / name / f"{i:05}.{i:032x}").write_text("Subject: hi\n\nbody")
    return root


class TestLoad:
    def test_labels_every_message_by_its_partition(self, tmp_path):
        root = corpus(tmp_path, {"20030228_easy_ham": 1, "20030228_spam": 1})
        assert [(e.partition, e.is_spam) for e in load(root)] == [("easy_ham", False), ("spam", True)]

    def test_skips_the_cmds_file(self, tmp_path):
        root = corpus(tmp_path, {"20030228_hard_ham": 2})
        assert len(load(root)) == 2

    def test_ignores_releases_superseded_by_a_later_one(self, tmp_path):
        root = corpus(tmp_path, {"20021010_spam": 3, "20030228_spam": 1, "20030228_spam_2": 3, "20050311_spam_2": 1})
        assert [e.path.parent.name for e in load(root)] == ["20030228_spam", "20050311_spam_2"]


def emails(partition: str, count: int) -> list[Email]:
    return [Email(path=Path(f"{partition}/{i}"), partition=partition, is_spam=False) for i in range(count)]


class TestSplit:
    def test_takes_the_same_number_from_every_partition(self):
        train, test = split(emails("easy_ham", 10) + emails("spam", 10), per_partition=3)
        assert sorted(e.partition for e in train) == ["easy_ham"] * 3 + ["spam"] * 3
        assert sorted(e.partition for e in test) == ["easy_ham"] * 3 + ["spam"] * 3

    def test_train_and_test_never_share_a_message(self):
        train, test = split(emails("easy_ham", 10), per_partition=5)
        assert not set(train) & set(test)

    def test_is_reproducible(self):
        assert split(emails("easy_ham", 50), per_partition=5) == split(emails("easy_ham", 50), per_partition=5)
