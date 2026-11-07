from spam.decision import spam


def test_the_baseline_takes_jevs_spam_judgment_as_it_is():
    assert spam({"spam": 0.7}, {"list_mail": True}) == 0.7
