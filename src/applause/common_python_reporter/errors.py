"""Custom exceptions for the Applause client.

The `ApplauseClientError` class is a base exception that captures errors related to the Applause client.
It takes a `requests.Response` object as an argument and extracts the error message from the response.
"""

import requests


class ApplauseClientError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, response: requests.Response):
        """Initialize the ApplauseClientError object.

        Args:
        ----
            response (requests.Response): The response object from the HTTP request.

        """
        message = response.json()["message"]
        if message is None:
            message = response.text
        self.message = message
        super().__init__(self.message)
