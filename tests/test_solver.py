import asyncio

from spam.solver import groups, solve


def test_groups_split_emails_into_requests_of_at_most_size():
    assert groups([1, 2, 3, 4, 5], size=2) == [[1, 2], [3, 4], [5]]


def test_solve_asks_each_group_and_keeps_email_order():
    asked = []

    async def ask(group):
        asked.append(group)
        return [len(email["body"]) / 10 for email in group]

    emails = [{"body": "x" * n} for n in range(5)]
    scores = asyncio.run(solve(ask, emails, asyncio.Semaphore(2), size=2))
    assert scores == [0.0, 0.1, 0.2, 0.3, 0.4]
    assert len(asked) == 3
