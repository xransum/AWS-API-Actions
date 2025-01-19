import importlib

import pytest


def test_import_package() -> None:
    """Test import of the package."""
    try:
        importlib.import_module("aws_api_actions")

    except ImportError:
        pytest.fail("Failed to import the package.")
