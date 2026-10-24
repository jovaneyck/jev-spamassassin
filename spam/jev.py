"""Several emails in one Jev request: each gets a spam question pointed at it."""

from typesafe_sdk import AsyncTypeSafeClient, Noul

MODEL = "jev-preview"
GROUP = 10  # emails per request


def keys(count: int) -> list[str]:
    return [f"e{i}" for i in range(1, count + 1)]


def request(emails: list[dict[str, str]]) -> tuple[dict, dict]:
    state = {"emails": dict(zip(keys(len(emails)), emails))}
    questions = {
        f"{key}.spam": Noul(instructions=f"Is `emails.{key}` spam: unsolicited bulk or commercial email?")
        for key in keys(len(emails))
    }
    return state, questions


def read(result, count: int) -> list[float]:
    """Spam likelihood per email, in request order."""
    return [result.answers[f"{key}.spam"].noul for key in keys(count)]


async def ask(client: AsyncTypeSafeClient, emails: list[dict[str, str]]) -> list[float]:
    state, questions = request(emails)
    return read(await client.system_one(state=state, questions=questions, model=MODEL), len(emails))
