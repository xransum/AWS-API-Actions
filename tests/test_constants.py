"""Test for constants."""

import re

from aws_api_actions.constants import USER_AGENT


def test_user_agent() -> None:
    """Test the USER_AGENT constant."""
    # A bit unnecessary, since the user agent can be anything, but
    # we're testing it for the sake of testing.
    assert (
        re.match(
            r"[a-zA-Z0-9\-_.]+(\/[a-zA-Z0-9\-_.]+)?" "(\s\([^\)]+\))*",
            USER_AGENT,
        )
        is not None
    )
