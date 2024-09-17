"""HTTP Client for interacting with the Applause Public API.

This module contains the PublicApi class which allows for interactions with the Applause Public API.

Typical usage example:
config = ApplauseConfig(...)
public_api = PublicApi(config)
public_api.submit_result(123, TestRunAutoResultDto(...))
# Submit additional results as needed
"""

import requests
from .config import ApplauseConfig
from .dtos import to_camel
from .errors import ApplauseClientError
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Optional


class TestRunAutoResultStatus(str, Enum):
    """Enumeration of valid statuses of a test result in the Applause Public API.

    Values:
        PASSED: The test result passed
        FAILED: The test result failed
        SKIPPED: The test result was skipped
        CANCLED: The test result was canceled
        ERROR: The test result had an error
    """

    PASSED = ("PASSED",)
    FAILED = ("FAILED",)
    SKIPPED = ("SKIPPED",)
    CANCLED = ("CANCLED",)
    ERROR = "ERROR"


class SessionDetailsValue(BaseModel):
    """Domain model for the value of a session details object.

    Attributes
    ----------
        deviceName: The name of the device
        orientation: The orientation of the device
        platformName: The name of the platform
        platformVersion: The version of the platform
        browserName: The name of the browser
        browserVersion: The version of the browser

    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    deviceName: Optional[str] = None
    orientation: Optional[str] = None
    platformName: Optional[str] = None
    platformVersion: Optional[str] = None
    browserName: Optional[str] = None
    browserVersion: Optional[str] = None


class SessionDetails(BaseModel):
    """A nested value for storing session details.

    Attributes
    ----------
        value: The value of the session details

    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    value: SessionDetailsValue


class TestRunAutoResultDto(BaseModel):
    """A domain model used to submit an automated test run result.

    Attributes
    ----------
        testCycleId: The id of the test cycle
        status: The status of the test run
        failureReason (optional): The reason for the failure
        sessionDetailsJson (optional): The session details
        startTime (optional): The start time of the test run
        endTime (optional): The end time of the test run

    """

    __test__ = False
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    testCycleId: int
    status: TestRunAutoResultStatus
    failureReason: Optional[str] = None
    sessionDetailsJson: Optional[SessionDetails] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None


class PublicApi:
    """HTTP Client for interacting with the Applause Public API.

    Attributes
    ----------
        config: The configuration for the client

    """

    def __init__(self, config: ApplauseConfig):
        """Initialize the PublicApi object.

        Args:
        ----
            config (ApplauseConfig): The configuration for the client

        """
        self.config = config
        pass

    def submit_result(self, test_case_id: int, info: TestRunAutoResultDto) -> None:
        """Submit a test result to the Applause Public API.

        Args:
        ----
            test_case_id (int): The id of the test case
            info (TestRunAutoResultDto): The test result information

        """
        headers = {"X-Api-Key": self.config.api_key, "Content-Type": "application/json"}
        try:
            response = requests.post(
                f"{self.config.auto_api_base_url}v2/test-case-results/{test_case_id}/submit",
                json=info,
                headers=headers,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise ApplauseClientError(response) from e
