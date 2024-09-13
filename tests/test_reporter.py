import responses
from unittest.mock import patch, MagicMock
from applause.common_python_reporter.reporter import ApplauseReporter, ApplauseConfig, AutoApi
from applause.common_python_reporter.dtos import TestRunCreateResponseDto, AssetType, CreateTestCaseResultResponseDto, TestResultStatus


class TestApplauseReporter:

    @responses.activate
    def test_runner_start(self):
        # Test starting a test run
        create_run_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-run/create', json={"runId": 123})
        responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/test-runs/123/heartbeat', json={})
        reporter = ApplauseReporter(ApplauseConfig(api_key='test', product_id=123))
        assert create_run_call.call_count == 0
        run_id = reporter.runner_start(tests=["test1", "test2"])
        assert create_run_call.call_count == 1
        assert create_run_call.calls[0].request.body == b'{"tests": ["test1", "test2"], "productId": 123, "sdkVersion": "python:1.0.0", "itwTestCycleId": null}', "Create run request Body should be formatted properly"
        assert run_id == 123

    @responses.activate
    def test_start_test_case(self):
        # Test starting a test case
        create_run_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-run/create', json={"runId": 123})
        responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/test-runs/123/heartbeat', json={})
        create_result_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-result/create-result', json={"testResultId": 456})
        reporter = ApplauseReporter(ApplauseConfig(api_key='test', product_id=123))
        assert create_run_call.call_count == 0
        reporter.runner_start()
        assert create_run_call.call_count == 1
        assert create_result_call.call_count == 0
        result = reporter.start_test_case("test1", "Test Case 1")
        assert create_result_call.call_count == 1
        assert create_result_call.calls[0].request.body == b'{"testRunId": 123, "testCaseName": "Test Case 1", "providerSessionIds": [], "testCaseId": null, "itwTestCaseId": null}', "Create result request body should be formatted properly"
        assert result.test_result_id == 456

    @responses.activate
    def test_submit_test_case_result(self):
        # Test submitting a test case result
        create_run_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-run/create', json={"runId": 123})
        responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/test-runs/123/heartbeat', json={})
        create_result_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-result/create-result', json={"testResultId": 456})
        submit_result_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-result', json={})
        reporter = ApplauseReporter(ApplauseConfig(api_key='test', product_id=123))

        assert create_run_call.call_count == 0
        reporter.runner_start()
        assert create_run_call.call_count == 1
        assert create_result_call.call_count == 0
        reporter.start_test_case("test1", "Test Case 1")
        assert create_result_call.call_count == 1
        assert create_result_call.calls[0].request.body == b'{"testRunId": 123, "testCaseName": "Test Case 1", "providerSessionIds": [], "testCaseId": null, "itwTestCaseId": null}', "Create result request body should be formatted properly"
        assert submit_result_call.call_count == 0
        reporter.submit_test_case_result("test1", TestResultStatus.PASSED)
        assert submit_result_call.call_count == 1
        assert submit_result_call.calls[0].request.body == b'{"testResultId": 456, "status": "PASSED", "providerSessionGuids": [], "testRailCaseId": null, "itwCaseId": null, "failureReason": null}', "Submit result request body should be formatted properly"

    @responses.activate
    def test_runner_end(self):
        # Test ending a test run
        create_run_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-run/create', json={"runId": 123})
        responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/test-runs/123/heartbeat', json={})
        end_run_call = responses.add(responses.DELETE, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-run/123?endingStatus=COMPLETE', json={})
        reporter = ApplauseReporter(ApplauseConfig(api_key='test', product_id=123))
        provider_info_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-result/provider-info', json={})

        assert create_run_call.call_count == 0
        reporter.runner_start(tests=["test1", "test2"])
        assert create_run_call.call_count == 1
        assert create_run_call.calls[0].request.body == b'{"tests": ["test1", "test2"], "productId": 123, "sdkVersion": "python:1.0.0", "itwTestCycleId": null}', "Create run request Body should be formatted properly"
        assert end_run_call.call_count == 0
        assert provider_info_call.call_count == 0
        reporter.runner_end()
        assert end_run_call.call_count == 1
        assert provider_info_call.call_count == 1

    @responses.activate
    def test_attach_test_case_asset(self):
        # Test attaching an asset to a test case
        create_run_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-run/create', json={"runId": 123})
        create_result_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-result/create-result', json={"testResultId": 123})
        responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/test-runs/123/heartbeat', json={})
        upload_asset_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-result/123/upload', json={})
        reporter = ApplauseReporter(ApplauseConfig(api_key='test', product_id=123))

        assert create_run_call.call_count == 0
        reporter.runner_start()
        assert create_run_call.call_count == 1

        assert create_result_call.call_count == 0
        reporter.start_test_case("test1", "Test Case 1")
        assert create_result_call.call_count == 1
        assert create_result_call.calls[0].request.body == b'{"testRunId": 123, "testCaseName": "Test Case 1", "providerSessionIds": [], "testCaseId": null, "itwTestCaseId": null}', "Create result request body should be formatted properly"

        
        assert upload_asset_call.call_count == 0
        reporter.attach_test_case_asset("test1", "asset.png", "123456", AssetType.SCREENSHOT, b"...")
        assert upload_asset_call.call_count == 1

    @responses.activate
    def test_submit_test_case_result_applause_test_case_id(self):
        # Test submitting a test case result
        create_run_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-run/create', json={"runId": 123})
        responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/test-runs/123/heartbeat', json={})
        create_result_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-result/create-result', json={"testResultId": 456})
        submit_result_call = responses.add(responses.POST, 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/test-result', json={})
        reporter = ApplauseReporter(ApplauseConfig(api_key='test', product_id=123))

        assert create_run_call.call_count == 0
        reporter.runner_start()
        assert create_run_call.call_count == 1
        assert create_result_call.call_count == 0
        reporter.start_test_case("test1", "Test Case 1")
        assert create_result_call.call_count == 1
        assert create_result_call.calls[0].request.body == b'{"testRunId": 123, "testCaseName": "Test Case 1", "providerSessionIds": [], "testCaseId": null, "itwTestCaseId": null}', "Create result request body should be formatted properly"
        assert submit_result_call.call_count == 0
        reporter.submit_test_case_result("test1", TestResultStatus.PASSED, applause_test_case_id="123")
        assert submit_result_call.call_count == 1
        print(submit_result_call.calls[0].request.body)
        assert submit_result_call.calls[0].request.body == b'{"testResultId": 456, "status": "PASSED", "providerSessionGuids": [], "testRailCaseId": null, "itwCaseId": "123", "failureReason": null}', "Submit result request body should be formatted properly"