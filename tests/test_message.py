from spam.message import BODY_CHARS, summary

PLAIN = b"""From: Alice <alice@example.com>
Received: from relay.example.com
Subject: Lunch?

Want to grab lunch?
"""

HTML = b"""From: deals@shop.biz
Subject: WIN BIG
Content-Type: text/html

<html><body><p>Click <b>here</b></p></body></html>
"""

MULTIPART = b"""From: a@b.c
Subject: both
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="X"

--X
Content-Type: text/html

<p>html version</p>
--X
Content-Type: text/plain

plain version
--X--
"""


def test_keeps_sender_subject_and_body_but_drops_other_headers():
    assert summary(PLAIN) == {"from": "Alice <alice@example.com>", "subject": "Lunch?", "body": "Want to grab lunch?"}


def test_strips_tags_from_an_html_body():
    assert summary(HTML)["body"] == "Click here"


def test_prefers_the_plain_text_part():
    assert summary(MULTIPART)["body"] == "plain version"


def test_truncates_long_bodies():
    raw = b"Subject: long\n\n" + b"a" * (BODY_CHARS + 100)
    assert len(summary(raw)["body"]) == BODY_CHARS


def test_missing_headers_and_body_are_empty():
    assert summary(b"\n") == {"from": "", "subject": "", "body": ""}
