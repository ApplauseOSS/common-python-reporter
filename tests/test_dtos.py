"""This module is used to test the dtos module."""

from applause.common_python_reporter.dtos import (
    AssetType,
    TestResultStatus,
    TestRunCreateDto,
    TestRunCreateResponseDto,
    CreateTestCaseResultDto,
    CreateTestCaseResultResponseDto,
    TestResultProviderInfo,
    TestRailOptions,
    EmailAddressResponse,
    EmailFetchRequest,
)


class TestRunCreateDtoTests:
    """Tests the TestRunCreateDto class."""

    def test_tests(self):
        """Tests the tests property."""
        tests = ["test1", "test2", "test3"]
        dto = TestRunCreateDto(tests=tests)
        assert dto.tests == tests

    def test_serialization(self):
        """Tests the serialization of the object."""
        tests = ["test1", "test2", "test3"]
        dto = TestRunCreateDto(tests=tests)
        assert dto.model_dump(by_alias=True) == {"tests": tests}


class TestRunCreateResponseDtoTests:
    """Tests for the TestRunCreateResponseDto class."""

    def test_run_id(self):
        """Tests the run_id property."""
        run_id = 12345
        dto = TestRunCreateResponseDto(run_id=run_id)
        assert dto.run_id == run_id

    def test_serialization(self):
        """Tests the serialization of the object."""
        run_id = 12345
        dto = TestRunCreateResponseDto(run_id=run_id)
        assert dto.model_dump(by_alias=True) == {"runId": run_id}


class CreateTestCaseResultDtoTests:
    """Tests for the CreateTestCaseResultDto class."""

    def test_test_run_id(self):
        """Tests the test_run_id property."""
        test_run_id = 12345
        dto = CreateTestCaseResultDto(test_run_id=test_run_id)
        assert dto.test_run_id == test_run_id

    def test_test_case_name(self):
        """Tests the test_case_name property."""
        test_case_name = "Test Case 1"
        dto = CreateTestCaseResultDto(test_case_name=test_case_name)
        assert dto.test_case_name == test_case_name

    def test_serialization(self):
        """Tests the serialization of the object."""
        test_run_id = 12345
        dto = CreateTestCaseResultDto(test_run_id=test_run_id)
        assert dto.model_dump(by_alias=True) == {"testRunId": test_run_id}


class CreateTestCaseResultResponseDtoTests:
    """Tests for the CreateTestCaseResultResponseDto class."""

    def test_test_result_id(self):
        """Tests the test_result_id property."""
        test_result_id = 12345
        dto = CreateTestCaseResultResponseDto(test_result_id=test_result_id)
        assert dto.test_result_id == test_result_id

    def test_serialization(self):
        """Tests the serialization of the object."""
        test_result_id = 12345
        dto = CreateTestCaseResultResponseDto(test_result_id=test_result_id)
        assert dto.model_dump(by_alias=True) == {"testResultId": test_result_id}

class TestResultStatusTests:
    """Tests for the TestResultStatus class."""

    def test_enum_values(self):
        """Tests the values of the enum."""
        assert TestResultStatus.NOT_RUN.value == "NOT_RUN"
        assert TestResultStatus.IN_PROGRESS.value == "IN_PROGRESS"
        assert TestResultStatus.PASSED.value == "PASSED"
        assert TestResultStatus.FAILED.value == "FAILED"
        assert TestResultStatus.SKIPPED.value == "SKIPPED"
        assert TestResultStatus.CANCELED.value == "CANCELED"
        assert TestResultStatus.ERROR.value == "ERROR"


class TestResultProviderInfoTests:
    """Tests for the TestResultProviderInfo class."""

    def test_test_result_id(self):
        """Tests the test_result_id property."""
        test_result_id = 12345
        provider_url = "https://example.com"
        provider_session_id = "session123"
        info = TestResultProviderInfo(
            test_result_id=test_result_id,
            provider_url=provider_url,
            provider_session_id=provider_session_id,
        )
        assert info.test_result_id == test_result_id

    def test_provider_url(self):
        """Tests the provider_url property."""
        test_result_id = 12345
        provider_url = "https://example.com"
        provider_session_id = "session123"
        info = TestResultProviderInfo(
            test_result_id=test_result_id,
            provider_url=provider_url,
            provider_session_id=provider_session_id,
        )
        assert info.provider_url == provider_url

    def test_provider_session_id(self):
        """Tests the provider_session_id property."""
        test_result_id = 12345
        provider_url = "https://example.com"
        provider_session_id = "session123"
        info = TestResultProviderInfo(
            test_result_id=test_result_id,
            provider_url=provider_url,
            provider_session_id=provider_session_id,
        )
        assert info.provider_session_id == provider_session_id

    def test_serialization(self):
        """Tests the serialization of the object."""
        test_result_id = 12345
        provider_url = "https://example.com"
        provider_session_id = "session123"
        info = TestResultProviderInfo(
            test_result_id=test_result_id,
            provider_url=provider_url,
            provider_session_id=provider_session_id,
        )
        assert info.model_dump(by_alias=True) == {
            "testResultId": test_result_id,
            "providerUrl": provider_url,
            "providerSessionId": provider_session_id,
        }


class TestRailOptionsTests:
    """Test the TestRailOptions class."""

    def test_serialization(self):
        """Tests the serialization of the object."""
        project_id = 12345
        suite_id = 67890
        plan_name = "Test Plan"
        run_name = "Test Run"
        add_all_tests_to_plan = True
        override_test_rail_run_uniqueness = False
        options = TestRailOptions(
            project_id=project_id,
            suite_id=suite_id,
            plan_name=plan_name,
            run_name=run_name,
            add_all_tests_to_plan=add_all_tests_to_plan,
            override_test_rail_run_uniqueness=override_test_rail_run_uniqueness,
        )
        assert options.model_dump(by_alias=True) == {
            "projectId": project_id,
            "suiteId": suite_id,
            "planName": plan_name,
            "runName": run_name,
            "addAllTestsToPlan": add_all_tests_to_plan,
            "overrideTestRailRunUniqueness": override_test_rail_run_uniqueness,
        }


class EmailAddressResponseTests:
    """Test the EmailAddressResponse class."""

    def test_email_address(self):
        """Tests the email_address property."""
        email_address = "test@example.com"
        response = EmailAddressResponse(email_address=email_address)
        assert response.email_address == email_address

    def test_serialization(self):
        """Tests the serialization of the object."""
        email_address = "test@example.com"
        response = EmailAddressResponse(email_address=email_address)
        assert response.model_dump(by_alias=True) == {"emailAddress": email_address}


class EmailFetchRequestTests:
    """Tests the EmailFetchRequest class."""

    def test_email_address(self):
        """Tests the email_address property."""
        email_address = "test@example.com"
        request = EmailFetchRequest(email_address=email_address)
        assert request.email_address == email_address

    def test_serialization(self):
        """Tests the serialization of the object."""
        email_address = "test@example.com"
        request = EmailFetchRequest(email_address=email_address)
        assert request.model_dump(by_alias=True) == {"emailAddress": email_address}


class AssetTypeTests:
    """Tests the AssetType class."""

    def test_enum_values(self):
        """Tests the values of the enum."""
        assert AssetType.SCREENSHOT.value == "SCREENSHOT"
        assert AssetType.FAILURE_SCREENSHOT.value == "FAILURE_SCREENSHOT"
        assert AssetType.VIDEO.value == "VIDEO"
        assert AssetType.NETWORK_HAR.value == "NETWORK_HAR"
        assert AssetType.VITALS_LOG.value == "VITALS_LOG"
        assert AssetType.CONSOLE_LOG.value == "CONSOLE_LOG"
        assert AssetType.NETWORK_LOG.value == "NETWORK_LOG"
        assert AssetType.DEVICE_LOG.value == "DEVICE_LOG"
        assert AssetType.SELENIUM_LOG.value == "SELENIUM_LOG"
        assert AssetType.SELENIUM_LOG_JSON.value == "SELENIUM_LOG_JSON"
        assert AssetType.BROWSER_LOG.value == "BROWSER_LOG"
        assert AssetType.FRAMEWORK_LOG.value == "FRAMEWORK_LOG"
        assert AssetType.EMAIL.value == "EMAIL"
        assert AssetType.PAGE_SOURCE.value == "PAGE_SOURCE"
        assert AssetType.CODE_BUNDLE.value == "CODE_BUNDLE"
        assert AssetType.RESULTS_ZIP.value == "RESULTS_ZIP"
        assert AssetType.SESSION_DETAILS.value == "SESSION_DETAILS"
        assert AssetType.DEVICE_DETAILS.value == "DEVICE_DETAILS"
        assert AssetType.UNKNOWN.value == "UNKNOWN"
