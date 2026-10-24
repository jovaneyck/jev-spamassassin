"""Smoke test for the TypeSafe API.

Run:
    1. Put API_KEY=<your TypeSafe key> in .env
    2. uv run hello_jev.py
"""

import os

from dotenv import load_dotenv
from typesafe_sdk import Noul, TypeSafeClient

load_dotenv()

with TypeSafeClient(api_key=os.environ["API_KEY"]) as client:
    result = client.system_one(
        state="Hello there Jev, how are you doing today?",
        questions={"is_greeting": Noul(instructions="Does `state` contain a greeting targeted at Jev, the new decision model?")},
    )
    print(result.answers)
