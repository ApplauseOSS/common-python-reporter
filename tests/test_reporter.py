import pytest
from unittest.mock import patch, MagicMock
from applause.common_python_reporter.reporter import ApplauseReporter, ApplauseConfig, AutoApi
from applause.common_python_reporter.dtos import TestRunCreateResponseDto, AssetType, CreateTestCaseResultResponseDto, TestResultStatus

class TestApplauseReporter:
    @pytest.fixture
    def reporter(self):
        with patch('applause.common_python_reporter.auto_api.AutoApi') as auto_api_mock:
            """Returns a mock AutoApi object"""
            auto_api_mock.start_test_run = MagicMock(return_value=TestRunCreateResponseDto(run_id=123))
            auto_api_mock.end_test_run = MagicMock()
            auto_api_mock.start_test_case = MagicMock(return_value = CreateTestCaseResultResponseDto(test_result_id=456))
            auto_api_mock.submit_test_case_result = MagicMock()
            auto_api_mock.get_provider_session_links = MagicMock(return_value = [])
            auto_api_mock.send_sdk_heartbeat.return_value = MagicMock()
            auto_api_mock.upload_asset.return_value = MagicMock()
            reporter = ApplauseReporter(ApplauseConfig(
                api_key="api-key",
                product_id=123
            ))
            reporter.auto_api = auto_api_mock
            reporter.initializer.auto_api = auto_api_mock
            yield reporter

    def test_runner_start(self, reporter: ApplauseReporter):
        # Test starting a test run
        run_id = reporter.runner_start(tests=["test1", "test2"])
        assert run_id == 123

    def test_start_test_case(self, reporter: ApplauseReporter):
        # Test starting a test case
        reporter.runner_start()
        result = reporter.start_test_case("test1", "Test Case 1")
        assert result.test_result_id == 456

    def test_submit_test_case_result(self, reporter: ApplauseReporter):
        # Test submitting a test case result
        reporter.runner_start()
        reporter.start_test_case("test1", "Test Case 1")
        reporter.submit_test_case_result("test1", TestResultStatus.PASSED)

    def test_runner_end(self, reporter: ApplauseReporter):
        # Test ending a test run
        reporter.runner_start(tests=["test1", "test2"])
        reporter.runner_end()

    def test_attach_test_case_asset(self, reporter: ApplauseReporter):
        # Test attaching an asset to a test case
        reporter.runner_start()
        reporter.start_test_case("test1", "Test Case 1")
        reporter.attach_test_case_asset("test1", "asset.png", "123456", AssetType.SCREENSHOT, b"...")