"""Data Transfer Objects for the Applause Automation API.

Strongly typed objects for interacting with the Applause Automation API.
We utilize Pydantic to define the structure of the objects and enforce type safety.
humps.camel is used to convert the field names to camel case for http transfer.

"""

from enum import Enum
from humps.camel import case as camelize
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


def to_camel(field_name: str) -> str:
    """Convert a field name to camel case."""
    return camelize(field_name)


class TestRunCreateDto(BaseModel):
    """Domain model for creating a test run.

    Attributes
    ----------
        tests: List of test names to be included in the test

    """

    __test__ = False
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    tests: Optional[List[str]] = None


class TestRunCreateResponseDto(BaseModel):
    """Domain model for the response of a test run creation request.

    Attributes
    ----------
        run_id: The id of the created test run

    """

    __test__ = False
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    run_id: int


class CreateTestCaseResultDto(BaseModel):
    """Domain model for creating a test case result.

    Attributes
    ----------
        test_run_id: The id of the test run
        test_case_name: The name of the test case
        provider_session_ids: List of provider session ids
        test_case_id: The test case id
        itw_test_case_id: The itw test case id

    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    test_run_id: int
    test_case_name: str
    provider_session_ids: List[str]
    test_case_id: Optional[str] = None
    itw_test_case_id: Optional[str] = None


class CreateTestCaseResultResponseDto(BaseModel):
    """Domain model for the response of a test case result creation request.

    Attributes
    ----------
        test_result_id: The id of the created test case result

    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    test_result_id: int


class TestResultStatus(str, Enum):
    """Enumeration of allowed test result statuses.

    Values:
        NOT_RUN: The test has not been run
        IN_PROGRESS: The test is in progress
        PASSED: The test has passed
        FAILED: The test has failed
        SKIPPED: The test has been skipped
        CANCELED: The test has been canceled
        ERROR: The test has encountered an error
    """

    __test__ = False
    model_config = ConfigDict(use_enum_values=True)
    NOT_RUN = "NOT_RUN"
    IN_PROGRESS = "IN_PROGRESS"
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    CANCELED = "CANCELED"
    ERROR = "ERROR"


class TestResultProviderInfo(BaseModel):
    """Domain model for the provider information of a test result.

    Attributes
    ----------
        test_result_id: The id of the test result
        provider_url: The url of the provider
        provider_session_id: The id of the provider session

    """

    __test__ = False
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    test_result_id: int
    provider_url: Optional[str] = None
    provider_session_id: Optional[str] = None


class TestRailOptions(BaseModel):
    """Configuration Options for a TestRail Connection.

    Attributes
    ----------
        project_id: The id of the project
        suite_id: The id of the suite
        plan_name: The name of the plan
        run_name: The name of the run
        add_all_tests_to_plan (optional): Flag to add all tests to the plan
        override_test_rail_run_uniqueness (optional): Flag to override test rail run uniqueness check

    """

    __test__ = False
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    project_id: int
    suite_id: int
    plan_name: str
    run_name: str
    add_all_tests_to_plan: Optional[bool] = None
    override_test_rail_run_uniqueness: Optional[bool] = None


class EmailAddressResponse(BaseModel):
    """Domain model for the response of an email address request.

    Attributes
    ----------
        email_address: The generated email address

    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    email_address: str


class EmailFetchRequest(BaseModel):
    """Domain model for an email fetch request.

    Attributes
    ----------
        email_address: The email address for fetch the content from.

    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    email_address: str


class SubmitTestCaseResultDto(BaseModel):
    """Domain model for submitting a test case result.

    Attributes
    ----------
        test_result_id: The id of the test result
        status: The status of the test result
        provider_session_guids: List of provider session guids
        test_rail_case_id: The test rail case id
        itw_case_id: The itw case id
        failure_reason: The reason for failure

    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    test_result_id: int
    status: TestResultStatus
    provider_session_guids: List[str]
    test_rail_case_id: Optional[str] = None
    itw_case_id: Optional[str] = None
    failure_reason: Optional[str] = None


class AssetType(str, Enum):
    """Enumeration of allowed asset types.

    Values:
        SCREENSHOT: A screenshot asset
        FAILURE_SCREENSHOT: A screenshot asset for a failure
        VIDEO: A video asset
        NETWORK_HAR: A network HAR asset
        VITALS_LOG: A vitals log asset
        CONSOLE_LOG: A console log asset
        NETWORK_LOG: A network log asset
        DEVICE_LOG: A device log asset
        SELENIUM_LOG_JSON: A selenium log JSON asset
        BROWSER_LOG: A browser log asset
        FRAMEWORK_LOG: A framework log asset
        EMAIL: An email asset
        PAGE_SOURCE: A page source asset
        UNKNOWN: An unknown asset
    """

    model_config = ConfigDict(use_enum_values=True)

    SCREENSHOT = "SCREENSHOT"
    FAILURE_SCREENSHOT = "FAILURE_SCREENSHOT"
    VIDEO = "VIDEO"
    NETWORK_HAR = "NETWORK_HAR"
    VITALS_LOG = "VITALS_LOG"
    CONSOLE_LOG = "CONSOLE_LOG"
    NETWORK_LOG = "NETWORK_LOG"
    DEVICE_LOG = "DEVICE_LOG"
    SELENIUM_LOG_JSON = "SELENIUM_LOG_JSON"
    BROWSER_LOG = "BROWSER_LOG"
    FRAMEWORK_LOG = "FRAMEWORK_LOG"
    EMAIL = "EMAIL"
    PAGE_SOURCE = "PAGE_SOURCE"
    UNKNOWN = "UNKNOWN"
