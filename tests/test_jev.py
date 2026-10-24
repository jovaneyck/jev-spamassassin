from types import SimpleNamespace

from spam.jev import read, request

EMAILS = [{"from": "a", "subject": "s1", "body": "b1"}, {"from": "b", "subject": "s2", "body": "b2"}]


def test_every_email_is_in_state_under_its_own_key():
    state, _ = request(EMAILS)
    assert state == {"emails": {"e1": EMAILS[0], "e2": EMAILS[1]}}


def test_every_email_gets_a_spam_question_pointed_at_it():
    _, questions = request(EMAILS)
    assert sorted(questions) == ["e1.spam", "e2.spam"]
    assert "`emails.e2`" in questions["e2.spam"].instructions


def test_read_returns_each_emails_spam_likelihood_in_request_order():
    def noul(value):
        return SimpleNamespace(type="noul", noul=value)

    result = SimpleNamespace(answers={"e2.spam": noul(0.9), "e1.spam": noul(0.2)})
    assert read(result, 2) == [0.2, 0.9]
