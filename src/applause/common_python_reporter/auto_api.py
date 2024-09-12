"""HTTP Client for interacting with the Applause Automation API.

Typical usage example:

    # Configure the AutoApi Client
    config = ApplauseConfig(api_key="your_api_key", product_id=12345, test_rail_options=None, applause_test_cycle_id=None)
    auto_api = AutoApi(config)

    # Start a Test Run
    tr_id = auto_api.start_test_run(TestRunCreateDto(tests=["test1", "test2"])).test_run_id

    # Submit Test Case Results
    test_case = auto_api.start_test_case(CreateTestCaseResultDto(test_run_id=tr_id, test_case_name="test1", provider_session_ids=[]))
    auto_api.submit_test_case_result(SubmitTestCaseResultDto(test_result_id=test_case.test_result_id, status=TestResultStatus.PASSED, provider_session_ids=[]))
    # Repeat for other test cases

    # End the Test Run
    auto_api.end_test_run(tr_id)

"""

import requests
from .dtos import (
    TestRunCreateDto,
    TestRunCreateResponseDto,
    CreateTestCaseResultDto,
    CreateTestCaseResultResponseDto,
    SubmitTestCaseResultDto,
    TestResultProviderInfo,
    EmailAddressResponse,
    EmailFetchRequest,
    AssetType,
)
from .config import ApplauseConfig
from typing import List
from email import message_from_bytes
from email.message import Message
from .version import __version__


class AutoApi:
    """HTTP Client for interacting with the Applause Automation API.

    Attributes
    ----------
        config (ApplauseConfig): The configuration for the AutoApi.
        api_version (str): The version of the Automation API being used.

    """

    def __init__(self, config: ApplauseConfig):
        """Initialize the AutoApi Client with the provided configuration.

        Args:
        ----
            config (ApplauseConfig): The configuration for the AutoApi.

        """
        self.config = config
        self.api_version = __version__
        pass

    def start_test_run(self, params: TestRunCreateDto) -> TestRunCreateResponseDto:
        """Start a test run with the provided parameters.

        This HTTP Call initializes a new TestRun with the provided parameters. It will also setup
        placeholders for the test results that will be submitted later, if the tests are provided here.
        If the testRailOptions are provided in the configuration, test rail reporting will be enabled
        for all test cases in the test run. The applause_test_cycle_id enables the test run to be associated
        with a specific Applause test cycle.

        Args:
        ----
            params (TestRunCreateDto): The parameters for the test run.

        Returns:
        -------
            TestRunCreateResponseDto: The response of the test run creation request.

        """
        headers = {"X-Api-Key": self.config.api_key, "Content-Type": "application/json"}
        # Dump the model to a dictionary and add the productId and sdkVersion
        request_params = params.model_dump(by_alias=True)
        request_params["productId"] = self.config.product_id
        request_params["sdkVersion"] = f"python:{self.api_version}"

        # If testRailOptions is not None, add the testRailReportingEnabled flag and the additional testRailOptions
        if self.config.test_rail_options is not None:
            request_params["testRailReportingEnabled"] = True
            request_params["addAllTestsToPlan"] = self.config.test_rail_options.add_all_tests_to_plan
            request_params["testRailProjectId"] = self.config.test_rail_options.project_id
            request_params["testRailSuiteId"] = self.config.test_rail_options.suite_id
            request_params["testRailPlanName"] = self.config.test_rail_options.plan_name
            request_params["testRailRunName"] = self.config.test_rail_options.run_name
            request_params["overrideTestRailRunNameUniqueness"] = self.config.test_rail_options.override_test_rail_run_uniqueness

        # Post the request to Auto API
        response = requests.post(
            f"{self.config.auto_api_base_url}api/v1.0/test-run/create",
            json=request_params,
            headers=headers,
        )
        return TestRunCreateResponseDto.model_validate(response.json())

    def end_test_run(self, test_run_id: int) -> None:
        """End a test run with the provided test run ID.

        This HTTP Call ends the test run with the provided test run ID. The endingStatus parameter is always set to COMPLETE
        in this case. This will finalize the test run and make the results available for fetching.

        Args:
        ----
            test_run_id (int): The ID of the test run to end.

        """
        headers = {"X-Api-Key": self.config.api_key}
        requests.delete(
            f"{self.config.auto_api_base_url}api/v1.0/test-run/{test_run_id}?endingStatus=COMPLETE",
            headers=headers,
        )

    def start_test_case(self, params: CreateTestCaseResultDto) -> CreateTestCaseResultResponseDto:
        """Start a test case with the provided parameters.

        This HTTP Call initializes a new test case result with the provided parameters. This will make
        the test result as IN_PROGRESS if the test case was provided in the create_test_run call. Otherwise,
        it will set up a new test result in the IN_PROGRESS status. The providerSessionIds are used to
        associate the test case with the provider sessions that were used to execute the test case.
        The itwTestCaseId and testRailCaseId are used to associate the test case with the respective test case
        IDs in the Applause and TestRail systems. The failureReason is used in the case of a skip or failure to provide
        a reason for the result.

        Args:
        ----
            params (CreateTestCaseResultDto): The parameters for the test case.

        Returns:
        -------
            CreateTestCaseResultResponseDto: The response of the test case creation request.

        """
        headers = {"X-Api-Key": self.config.api_key, "Content-Type": "application/json"}
        request_params = params.model_dump(by_alias=True)
        response = requests.post(
            f"{self.config.auto_api_base_url}api/v1.0/test-result/create-result",
            json=request_params,
            headers=headers,
        )
        return CreateTestCaseResultResponseDto.model_validate(response.json())

    def submit_test_case_result(self, params: SubmitTestCaseResultDto) -> None:
        """Submit a test case result with the provided parameters.

        This HTTP Call submits a test case result with the provided parameters. This call can only be made if the test
        result has previously been marked IN_PROGRESS by the start_test_case call. The status parameter is used to
        set the status of the test case result.

        Args:
        ----
            params (SubmitTestCaseResultDto): The parameters for the test case result.

        """
        headers = {"X-Api-Key": self.config.api_key, "Content-Type": "application/json"}
        request_params = params.model_dump(by_alias=True)
        requests.post(
            f"{self.config.auto_api_base_url}api/v1.0/test-result",
            json=request_params,
            headers=headers,
        )

    def get_provider_session_links(self, result_ids: List[int]) -> List[TestResultProviderInfo]:
        """Fetch the provider session links for the provided result IDs.

        This HTTP Call fetches the provider session links for the provided result IDs. This can be used to
        get the links to the provider sessions that were used to execute the test cases.

        Args:
        ----
            result_ids (List[int]): The list of result IDs to fetch provider session links for. These result ids
            should be from the same test run, and are returned by the start_test_case method.

        """
        headers = {"X-Api-Key": self.config.api_key}
        response = requests.post(
            f"{self.config.auto_api_base_url}api/v1.0/test-result/provider-info",
            json=result_ids,
            headers=headers,
        )
        print(response.text)
        return [TestResultProviderInfo.model_validate(result) for result in response.json()]

    def send_sdk_heartbeat(self, test_run_id: int) -> None:
        """Send an SDK heartbeat for the provided test run ID.

        This HTTP Call sends an SDK heartbeat for the provided test run ID. This can be used to keep the test run
        alive and prevent it from being marked as inactive.

        Args:
        ----
            test_run_id (int): The ID of the test run to send the SDK heartbeat for

        """
        headers = {"X-Api-Key": self.config.api_key}
        requests.post(
            f"{self.config.auto_api_base_url}api/v2.0/sdk-heartbeat",
            json={"testRunId": test_run_id},
            headers=headers,
        )

    def get_email_address(self, email_prefix: str) -> EmailAddressResponse:
        """Generate an email address with the provided email prefix.

        This HTTP Call generates an email address with the provided email prefix. This email address can be used
        to receive emails that are sent to the generated email address.

        Args:
        ----
            email_prefix (str): The email prefix to generate the email address with.

        """
        headers = {"X-Api-Key": self.config.api_key}
        response = requests.get(
            f"{self.config.auto_api_base_url}api/v1.0/email/get-address?prefix={email_prefix}",
            headers=headers,
        )
        return EmailAddressResponse.model_validate(response.json())

    def get_email_content(self, request: EmailFetchRequest) -> Message:
        """Fetch the email content for the provided email address.

        This HTTP Call fetches the email content for the provided email address. This can be used to get the
        contents of the email that was sent to the generated email address.

        Args:
        ----
            request (EmailFetchRequest): The request for fetching the email content.

        """
        headers = {"X-Api-Key": self.config.api_key}
        response = requests.post(
            f"{self.config.auto_api_base_url}api/v1.0/email/download-email",
            json=request.model_dump(by_alias=True),
            headers=headers,
        )
        return message_from_bytes(response.content)

    def upload_asset(
        self,
        result_id: int,
        file: bytes,
        asset_name: str,
        provider_session_guid: str,
        asset_type: AssetType,
    ) -> None:
        """Upload an asset for the provided test result ID.

        This HTTP Call uploads an asset for the provided test result ID. This can be used to attach screenshots
        or other assets to the test results.

        Args:
        ----
            result_id (int): The ID of the test result to upload the asset for.
            file (bytes): The file to upload as the asset.
            asset_name (str): The name of the asset.
            provider_session_guid (str): The provider session GUID for the asset.
            asset_type (AssetType): The type of the asset.

        """
        headers = {"X-Api-Key": self.config.api_key}
        requests.post(
            f"{self.config.auto_api_base_url}api/v1.0/test-result/{result_id}/upload",
            headers=headers,
            files={"file": (asset_name, file, "application/octet-stream")},
            data={
                "providerSessionGuid": provider_session_guid,
                "assetType": asset_type.value,
                "assetName": asset_name,
            },
        )
