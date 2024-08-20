"""Tests for the utils module."""

import pytest
from applause.common_python_reporter.utils import parse_test_case_names, TestCaseNameMatches

class TestParseTestCaseNames:
    """Tests for the parse_test_case_names function."""

    @pytest.mark.parametrize(
        "test_case_name,expected_tr_id,expected_applause_id,expected_clean_name",
        [
            ("Applause-123 TestRail-456 Test Case", 456, 123, "Test Case"),
            ("Applause-123 Test Case TestRail-456", 456, 123, "Test Case"),
            ("Applause-123 Test Case", None, 123, "Test Case"),
            ("TestRail-456 Test Case", 456, None, "Test Case"),
            ("Test Case", None, None, "Test Case"),
        ],
    )
    def test_parse_test_case_names(
        self,
        test_case_name: str,
        expected_tr_id: int,
        expected_applause_id: int,
        expected_clean_name: str,
    ):
        """Test the parse_test_case_names function."""
        expected_result = TestCaseNameMatches(
            test_case_name=expected_clean_name,
            test_rail_test_case_id=expected_tr_id,
            applause_test_case_id=expected_applause_id,
        )
        assert parse_test_case_names(test_case_name) == expected_result
