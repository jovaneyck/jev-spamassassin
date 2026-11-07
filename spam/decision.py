"""Code makes the decision: combine Jev's judgments with the facts code knows into one spam score."""


def spam(judgments: dict[str, float], facts: dict[str, bool]) -> float:
    return judgments["spam"]
