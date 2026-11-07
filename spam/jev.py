"""Several emails in one Jev request: every email gets the same judgments, each pointed at that email."""

from typesafe_sdk import AsyncTypeSafeClient, Noul

MODEL = "jev-1.14.0"
GROUP = 10  # emails per request


def questions(email: str) -> dict[str, Noul]:
    """The judgments Jev makes about one email. `email` is that email's path in `state`."""
    return {"spam": Noul(instructions=f"Is `{email}` spam: unsolicited bulk or commercial email?")}


def keys(count: int) -> list[str]:
    return [f"e{i}" for i in range(1, count + 1)]


def request(emails: list[dict[str, str]]) -> tuple[dict, dict]:
    state = {"emails": dict(zip(keys(len(emails)), emails))}
    asked = {
        f"{key}.{name}": question
        for key in keys(len(emails))
        for name, question in questions(f"emails.{key}").items()
    }
    return state, asked


def read(result, count: int) -> list[dict[str, float]]:
    """Each email's judgments by name, in request order."""
    return [
        {name.removeprefix(f"{key}."): answer.noul for name, answer in result.answers.items() if name.startswith(f"{key}.")}
        for key in keys(count)
    ]


async def ask(client: AsyncTypeSafeClient, emails: list[dict[str, str]]) -> list[dict[str, float]]:
    state, asked = request(emails)
    return read(await client.system_one(state=state, questions=asked, model=MODEL), len(emails))
