import os
import sys

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import pytest


CDEK_CLIENT_ID = os.getenv("CDEK_CLIENT_ID")
CDEK_CLIENT_SECRET = os.getenv("CDEK_CLIENT_SECRET")
CDEK_TEST_MODE = os.getenv("CDEK_TEST_MODE")


def main() -> int:
    os.environ["CDEK_CLIENT_ID"] = CDEK_CLIENT_ID
    os.environ["CDEK_CLIENT_SECRET"] = CDEK_CLIENT_SECRET
    os.environ["CDEK_TEST_MODE"] = CDEK_TEST_MODE

    return pytest.main(
        [
            "-s",
            "tests/test_location.py",
            "tests/test_office.py",
            "tests/test_calculator.py",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
