"""A raw email reduced to what Jev reads: sender, subject and the start of the body."""

import html
import re
from email import message_from_bytes, policy

BODY_CHARS = 2000  # most of the cost is body text


def text(message) -> str:
    part = message.get_body(preferencelist=("plain", "html"))
    if part is None:
        return ""
    try:
        content = part.get_content()
    except (LookupError, ValueError):  # unknown charsets and broken encodings are common in old spam
        content = part.get_payload(decode=True).decode("latin-1")
    if part.get_content_subtype() == "html":
        content = html.unescape(re.sub(r"<[^>]+>", "", content))
    return " ".join(content.split())


def summary(raw: bytes) -> dict[str, str]:
    message = message_from_bytes(raw, policy=policy.default)
    return {
        "from": str(message.get("from", "")),
        "subject": str(message.get("subject", "")),
        "body": text(message)[:BODY_CHARS],
    }
