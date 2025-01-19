"""Init file for the aws_api_actions package."""

import os

from aws_api_actions.logger import setup_logging


VERBOSE = os.environ.get("VERBOSE", "false").lower() == "true"
COLOR = os.environ.get("COLOR", "true").lower() == "true"


setup_logging(color=COLOR, verbose=VERBOSE)
