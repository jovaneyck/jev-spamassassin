import asyncio
from collections.abc import Awaitable, Callable

from spam import jev

THRESHOLD = 0.5  # naive: not calibrated on the training set

Ask = Callable[[list[dict[str, str]]], Awaitable[list[float]]]


def groups[T](items: list[T], size: int) -> list[list[T]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


async def solve(ask: Ask, emails: list[dict[str, str]], gate: asyncio.Semaphore, size: int = jev.GROUP) -> list[float]:
    """Spam likelihood per email, asking `size` emails per Jev request."""

    async def ask_group(group: list[dict[str, str]]) -> list[float]:
        async with gate:
            return await ask(group)

    answers = await asyncio.gather(*(ask_group(g) for g in groups(emails, size)))
    return [score for scores in answers for score in scores]
