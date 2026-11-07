from types import SimpleNamespace

from spam.jev import questions, read, request

EMAILS = [{"from": "a", "subject": "s1", "body": "b1"}, {"from": "b", "subject": "s2", "body": "b2"}]


def test_every_email_is_in_state_under_its_own_key():
    state, _ = request(EMAILS)
    assert state == {"emails": {"e1": EMAILS[0], "e2": EMAILS[1]}}


def test_every_email_gets_every_question_pointed_at_it():
    _, asked = request(EMAILS)
    assert sorted(asked) == sorted(f"{key}.{name}" for key in ("e1", "e2") for name in questions("email"))
    assert all("`emails.e2`" in question.instructions for name, question in asked.items() if name.startswith("e2."))


def test_read_returns_each_emails_judgments_in_request_order():
    def noul(value):
        return SimpleNamespace(type="noul", noul=value)

    result = SimpleNamespace(answers={"e2.spam": noul(0.9), "e1.spam": noul(0.2), "e1.scam": noul(0.1)})
    assert read(result, 2) == [{"spam": 0.2, "scam": 0.1}, {"spam": 0.9}]
