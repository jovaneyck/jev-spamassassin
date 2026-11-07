"""Classify every email of a set as spam or ham and score the result.

Run:
    1. Put API_KEY=<your TypeSafe key> in .env
    2. uv run split.py               (once)
    3. uv run solve.py [train|test]  (default: train; climb on train, check on test)
    Answers are written to out/<set>.jsonl.
"""

import asyncio
import json
import os
import sys
from collections import defaultdict
from functools import partial
from pathlib import Path

from dotenv import load_dotenv
from typesafe_sdk import AsyncTypeSafeClient

from spam import decision, jev
from spam.corpus import SPAM
from spam.message import facts, summary
from spam.metrics import Scored, auc, confusion
from spam.solver import THRESHOLD, solve

SPLITS = Path("splits")
OUT = Path("out")
CONCURRENCY = 8


def partition(path: Path) -> str:
    return path.parent.name.split("_", 1)[1]


def report(scored: list[Scored]) -> None:
    c = confusion(scored, THRESHOLD)
    print(f"{len(scored)} emails  auc={auc(scored):.3f}  accuracy={c.accuracy:.3f}  "
          f"precision={c.precision:.3f}  recall={c.recall:.3f}  (threshold {THRESHOLD})")
    by_partition: dict[str, list[Scored]] = defaultdict(list)
    for s in scored:
        by_partition[s.partition].append(s)
    for name, members in sorted(by_partition.items()):
        print(f"  {name:11} accuracy={confusion(members, THRESHOLD).accuracy:.3f}")


async def main(name: str) -> None:
    paths = [Path(line) for line in (SPLITS / f"{name}.txt").read_text().splitlines()]
    raws = [p.read_bytes() for p in paths]
    known = [facts(raw) for raw in raws]
    async with AsyncTypeSafeClient(api_key=os.environ["API_KEY"], timeout=60) as client:
        judged = await solve(partial(jev.ask, client), [summary(raw) for raw in raws], asyncio.Semaphore(CONCURRENCY))
    scored = [Scored(partition(p), partition(p) in SPAM, decision.spam(j, f)) for p, j, f in zip(paths, judged, known)]
    OUT.mkdir(exist_ok=True)
    rows = [{"email": p.as_posix(), "partition": s.partition, "is_spam": s.is_spam, "spam": s.score, "judgments": j, "facts": f}
            for p, s, j, f in zip(paths, scored, judged, known)]
    (OUT / f"{name}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    report(scored)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "train"))
