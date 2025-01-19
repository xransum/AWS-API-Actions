"""Custom exception classes for the aws_api_actions package.

This module defines custom exceptions that are raised during various stages
of the aws_api_actions pipeline, including scraping, parsing, and outputting data.

Custom exceptions are used to handle specific errors in the workflow, making it
easier to identify the source of issues and manage error handling effectively.

Exceptions:
    - ScrapingError: Raised when there is an error during the web scraping process.
    - ParsingError: Raised when there is an error during the data parsing process.
    - OutputError: Raised when there is an error during the output generation
        (e.g., saving to file).

Usage example:
    raise ScrapingError("Failed to scrape the service URLs.")
"""


class ScrapingError(Exception):
    """Exception raised for errors in the scraping process."""

    def __init__(self, message: str) -> None:
        """Initialize the ScrapingError with the specified error message."""
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return the string representation of the exception."""
        return f"ScrapingError: {self.message}"


class ParsingError(Exception):
    """Exception raised for errors in the parsing process."""

    def __init__(self, message: str) -> None:
        """Initialize the ParsingError with the specified error message."""
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Initialize the ParsingError with the specified error message."""
        return f"ParsingError: {self.message}"


class OutputError(Exception):
    """Exception raised for errors in the output process."""

    def __init__(self, message: str) -> None:
        """Initialize the OutputError with the specified error message."""
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Initialize the OutputError with the specified error message."""
        return f"OutputError: {self.message}"
