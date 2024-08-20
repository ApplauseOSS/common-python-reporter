"""Provides classes to report the results to an Applause Automation test run without managing ids or state.

This module handles typical flow of reporting the results of a test run. When using the raw
AutoApi HTTP Client, the user has to manage the ids of the test run, test cases, and test case
results and pass them into the correct hooks. This module abstracts that away and provides a
simpler interface to report the results of a test run.

Typical usage example:
    ApplauseReporter = ApplauseReporter(config)
    run_id = ApplauseReporter.runner_start(tests=["test1", "test2"])
    ApplauseReporter.start_test_case("test1", "test1")
    ApplauseReporter.submit_test_case_result("test1", TestResultStatus.PASSED)
"""

from .auto_api import AutoApi
from .config import ApplauseConfig
from .dtos import (
    TestRunCreateDto,
    CreateTestCaseResultDto,
    CreateTestCaseResultResponseDto,
    TestResultStatus,
    SubmitTestCaseResultDto,
    AssetType,
)
from .heartbeat import HeartbeatService
import json
from .utils import parse_test_case_names
from typing import List, Optional


class RunReporter:
    """Handles reporting results of a test run.

    Attributes
    ----------
        test_run_id (int): The id of the test run
        auto_api (AutoApi): The auto api client
        result_map (Dict[str, int]): A map of test case ids to test case result ids
        heartbeat_service (HeartbeatService): The heartbeat service

    """

    def __init__(self, test_run_id: int, auto_api: AutoApi, heartbeat_service: HeartbeatService):
        """Initialize the RunReporter object.

        Args:
        ----
            test_run_id (int): The id of the test run
            auto_api (AutoApi): The auto api client
            heartbeat_service (HeartbeatService): The heartbeat service

        """
        self.auto_api = auto_api
        self.test_run_id = test_run_id
        self.hearbeat_service = heartbeat_service
        self.result_map = {}

    def start_test_case(
        self, id: str, test_case_name: str, provider_session_ids: Optional[List[str]] = None, testrail_test_case_id: Optional[str] = None, itw_test_case_id: Optional[str] = None
    ) -> CreateTestCaseResultResponseDto:
        """Start a test case.

        Args:
        ----
            id (str): The id of the test case
            test_case_name (str): The name of the test case
            provider_session_ids (Optional[List[str]], optional): The list of provider session ids. Defaults to None.
            testrail_test_case_id (Optional[str], optional): The test rail case id. Defaults to None.
            itw_test_case_id (Optional[str], optional): The itw test case id. Defaults to None.

        """
        parsed_test_case = parse_test_case_names(test_case_name)
        body = CreateTestCaseResultDto(
            test_case_name=parsed_test_case.test_case_name,
            test_run_id=self.test_run_id,
            itw_test_case_id=itw_test_case_id if itw_test_case_id is not None else parsed_test_case.itw_test_case_id,
            test_case_id=testrail_test_case_id if testrail_test_case_id is not None else parsed_test_case.test_case_id,
            provider_session_ids=provider_session_ids if provider_session_ids is not None else [],
        )
        result = self.auto_api.start_test_case(params=body)
        self.result_map[id] = result.test_result_id
        return result

    def submit_test_case_result(
        self,
        id: str,
        status: TestResultStatus,
        provider_session_guids: Optional[List[str]] = None,
        test_rail_case_id: Optional[str] = None,
        applause_test_case_id: Optional[str] = None,
        failure_reason: Optional[str] = None,
    ):
        """Submit a test case result.

        Args:
        ----
            id (str): The id of the test case
            status (TestResultStatus): The status of the test case
            provider_session_guids (Optional[List[str]], optional): The list of provider session guids. Defaults to None.
            test_rail_case_id (Optional[str], optional): The test rail case id. Defaults to None.
            applause_test_case_id (Optional[str], optional): The itw test case id. Defaults to None.
            failure_reason (Optional[str], optional): The reason for the failure. Defaults to None.

        Raises:
        ------
            ValueError: If the test case result id is not found

        """
        result_id = self.result_map[id]
        if result_id is None:
            raise ValueError("Test case result id not found")
        body = SubmitTestCaseResultDto(
            test_result_id=result_id,
            status=status,
            provider_session_guids=provider_session_guids if provider_session_guids is not None else [],
            failure_reason=failure_reason,
            itw_test_case_id=applause_test_case_id,
            test_rail_case_id=test_rail_case_id,
            test_case_id=failure_reason,
        )
        self.auto_api.submit_test_case_result(params=body)

    def attach_test_case_asset(self, id: str, asset_name: str, provider_session_guid: str, assetType: AssetType, asset: bytes):
        """Attach an asset to a test case.

        Args:
        ----
            id (str): The id of the test case
            asset_name (str): The name of the asset
            provider_session_guid (str): The provider session guid
            assetType (AssetType): The type of the asset
            asset (bytes): The asset to attach

        Raises:
        ------
            ValueError: If the test case result id is not found

        """
        result_id = self.result_map[id]
        if result_id is None:
            raise ValueError("Test case result id not found")
        self.auto_api.upload_asset(result_id=result_id, file=asset, asset_name=asset_name, provider_session_guid=provider_session_guid, asset_type=assetType)

    def end_run(self):
        """End the test run and print the provider session links.

        Raises
        ------
            ValueError: If the test run id is not found

        """
        self.hearbeat_service.stop()
        self.auto_api.end_test_run(test_run_id=self.test_run_id)
        links = self.auto_api.get_provider_session_links(list(self.result_map.values()))
        if len(links) > 0:
            print("Provider session links:")
            for link in links:
                print(link)
        with open("provider_session_links.txt", "w") as f:
            f.write(json.dumps(links))


class RunInitializer:
    """Start a test run. It is used to create a RunReporter object.

    Attributes
    ----------
        config (ApplauseConfig): The configuration for the client
        auto_api (AutoApi): The auto api client

    """

    def __init__(self, auto_api: AutoApi):
        """Initialize the RunInitializer object.

        Args:
        ----
            auto_api (AutoApi): The auto api client

        """
        self.auto_api = auto_api

    def start_run(self, tests: Optional[List[str]]) -> RunReporter:
        """Start a test run and returns a RunReporter object.

        Args:
        ----
        tests (Optional[List[str]], optional): The list of test case names to run. Defaults to None.

        """
        response = self.auto_api.start_test_run(params=TestRunCreateDto(tests=[parse_test_case_names(test).test_case_name for test in tests]))
        heartbeat_service = HeartbeatService(self.auto_api, response.run_id)
        heartbeat_service.start()
        return RunReporter(response.run_id, self.auto_api, heartbeat_service)


class ApplauseReporter:
    """Report the results of the test run.

    Attributes
    ----------
        config (ApplauseConfig): The configuration for the client
        auto_api (AutoApi): The auto api client
        initializer (RunInitializer): The initializer object
        reporter (Optional[RunReporter]): The reporter object

    """

    def __init__(self, config: ApplauseConfig):
        """Initialize the ApplauseReporter object."""
        self.config = config
        self.auto_api = AutoApi(config)
        self.initializer = RunInitializer(self.auto_api)
        self.reporter = None

    def runner_start(self, tests: Optional[List[str]]) -> int:
        """Initialize a test run.

        Args:
        ----
        tests (Optional[List[str]], optional): The list of test case names to run. Defaults to None.

        """
        if self.reporter is not None:
            raise ValueError("Cannot start a run - run already started or run already finished")
        self.reporter = self.initializer.start_run(tests)
        return self.reporter.test_run_id

    def start_test_case(
        self, id: str, test_case_name: str, provider_session_ids: Optional[List[str]] = None, testrail_test_case_id: Optional[str] = None, itw_test_case_id: Optional[str] = None
    ) -> CreateTestCaseResultResponseDto:
        """Start a test case.

        Args:
        ----
            id (str): The id of the test case
            test_case_name (str): The name of the test case
            provider_session_ids (Optional[List[str]], optional): The list of provider session ids. Defaults to None.
            testrail_test_case_id (Optional[str], optional): The test rail case id. Defaults to None.
            itw_test_case_id (Optional[str], optional): The itw test case id. Defaults to None.

        Raises:
        ------
            ValueError: If the run was never initialized

        """
        if self.reporter is None:
            raise ValueError("Cannot start a test case for a run that was never initialized")
        return self.reporter.start_test_case(
            id, test_case_name, provider_session_ids=provider_session_ids, testrail_test_case_id=testrail_test_case_id, itw_test_case_id=itw_test_case_id
        )

    def submit_test_case_result(
        self,
        id: str,
        status: TestResultStatus,
        provider_session_guids: Optional[List[str]] = None,
        test_rail_case_id: Optional[str] = None,
        applause_test_case_id: Optional[str] = None,
        failure_reason: Optional[str] = None,
    ):
        """Submit a test case result.

        Args:
        ----
            id (str): The id of the test case
            status (TestResultStatus): The status of the test case
            provider_session_guids (Optional[List[str]], optional): The list of provider session guids. Defaults to None.
            test_rail_case_id (Optional[str], optional): The test rail case id. Defaults to None.
            applause_test_case_id (Optional[str], optional): The itw test case id. Defaults to None.
            failure_reason (Optional[str], optional): The reason for the failure. Defaults to None.

        Raises:
        ------
            ValueError: If the run was never initialized

        """
        if self.reporter is None:
            raise ValueError("Cannot submit a test case result for a run that was never initialized")
        self.reporter.submit_test_case_result(
            id,
            status,
            applause_test_case_id=applause_test_case_id,
            test_rail_case_id=test_rail_case_id,
            provider_session_guids=provider_session_guids,
            failure_reason=failure_reason,
        )

    def runner_end(self):
        """End the test run and print the provider session links.

        Raises
        ------
            ValueError: If the run was never initialized

        """
        if self.reporter is None:
            raise ValueError("Cannot end a run that was never initialized")
        self.reporter.end_run()
        self.reporter = None

    def attach_test_case_asset(self, id: str, asset_name: str, provider_session_guid: str, assetType: AssetType, asset: bytes):
        """Attach an asset to a test case.

        Args:
        ----
            id (str): The id of the test case
            asset_name (str): The name of the asset
            provider_session_guid (str): The provider session guid
            assetType (AssetType): The type of the asset
            asset (bytes): The asset to attach

        Raises:
        ------
            ValueError: If the run was never initialized

        """
        if self.reporter is None:
            raise ValueError("Cannot attach an asset for a run that was never initialized")
        self.reporter.attach_test_case_asset(id, asset_name, provider_session_guid, assetType, asset)
