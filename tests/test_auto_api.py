from applause.common_python_reporter.dtos import (
    TestRunCreateDto,
    TestRunCreateResponseDto,
    CreateTestCaseResultDto,
    CreateTestCaseResultResponseDto,
    SubmitTestCaseResultDto,
    TestResultStatus,
    EmailFetchRequest,
    AssetType,
)
from applause.common_python_reporter.auto_api import AutoApi
import pytest
from unittest.mock import Mock


class TestAutoApi:
    """Tests for the AutoApi class."""

    @pytest.fixture
    def auto_api(self):
        """Returns a mock AutoApi object"""
        auto_api_mock = Mock(spec=AutoApi)
        auto_api_mock.start_test_run.return_value = TestRunCreateResponseDto(run_id=123)
        auto_api_mock.end_test_run.return_value = None
        auto_api_mock.start_test_case.return_value = CreateTestCaseResultResponseDto(test_result_id=456)
        auto_api_mock.submit_test_case_result.return_value = None
        auto_api_mock.get_provider_session_links.return_value = ["link1", "link2"]
        auto_api_mock.send_sdk_heartbeat.return_value = None
        auto_api_mock.get_email_address.return_value = "test@example.com"
        auto_api_mock.get_email_content.return_value = "Email content"
        auto_api_mock.upload_asset.return_value = None
        return auto_api_mock

    def test_start_test_run(self, auto_api: AutoApi):
        """Tests the start_test_run method"""
        params = TestRunCreateDto(tests=["test1", "test2"])
        test_run = auto_api.start_test_run(params)
        assert test_run.run_id == 123

    def test_end_test_run(self, auto_api: AutoApi):
        """Tests the end_test_run method"""
        test_run_id = 123
        auto_api.end_test_run(test_run_id)

    def test_start_test_case(self, auto_api: AutoApi):
        """Tests the start_test_case method"""
        params = CreateTestCaseResultDto(test_run_id=123, test_case_name="test1", provider_session_ids=[])
        test_case_result = auto_api.start_test_case(params)
        assert test_case_result.test_result_id == 456

    def test_submit_test_case_result(self, auto_api: AutoApi):
        """Tests the submit_test_case_result method"""
        params = SubmitTestCaseResultDto(
            test_result_id=123,
            status=TestResultStatus.PASSED,
            provider_session_guids=[],
        )
        auto_api.submit_test_case_result(params)

    def test_get_provider_session_links(self, auto_api: AutoApi):
        """Tests the get_provider_session_links method"""
        result_ids = [123, 456]
        provider_session_links = auto_api.get_provider_session_links(result_ids)
        assert len(provider_session_links) == len(result_ids)

    def test_send_sdk_heartbeat(self, auto_api: AutoApi):
        """Tests the send_sdk_heartbeat method"""
        test_run_id = 123
        auto_api.send_sdk_heartbeat(test_run_id)

    def test_get_email_address(self, auto_api: AutoApi):
        """Tests the get_email_address method"""
        email_prefix = "test"
        email_address = auto_api.get_email_address(email_prefix)
        assert email_address == "test@example.com"

    def test_get_email_content(self, auto_api: AutoApi):
        """Tests the get_email_content method"""
        request = EmailFetchRequest(email_address="test@example.com")
        email_content = auto_api.get_email_content(request)
        assert email_content == "Email content"

    def test_upload_asset(self, auto_api: AutoApi):
        """Tests the upload_asset method"""
        result_id = 123
        file = b"file_content"
        asset_name = "asset_name"
        provider_session_guid = "provider_session_guid"
        asset_type = AssetType.SCREENSHOT
        auto_api.upload_asset(result_id, file, asset_name, provider_session_guid, asset_type)
