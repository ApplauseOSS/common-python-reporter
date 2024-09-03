"""Utility functions that are used in the test case execution.

Typical usage example:

        test_case_name = "TestRail-123 Applause-456 Test Case Name"
        parsed_test_case = utils.parse_test_case_names(test_case_name)
        print(parsed_test_case.test_case_name) # "Test Case Name"
        print(parsed_test_case.test_rail_test_case_id) # 123
        print(parsed_test_case.applause_test_case_id) # 456
"""

from pydantic import BaseModel
from re import findall, subn, search
from typing import List, Optional


class TestCaseNameMatches(BaseModel):
    """Model used to store the test case name and the test case ids after parsing.

    Attributes
    ----------
        test_case_name: The name of the test case
        test_rail_test_case_id: The TestRail test case id
        applause_test_case_id: The Applause test case id

    """

    __test__ = False

    test_case_name: str
    test_rail_test_case_id: Optional[int] = None
    applause_test_case_id: Optional[int] = None


def remove_prefix(text: str, prefix: str) -> str:
    """Remove a prefix from a string if it exists.

    This function is a utility to allow for the removal of a prefix from a string if it exists.
    In Python 3.9, the removeprefix method was added to the str class to allow for this functionality.
    This function is a workaround for Python versions that do not have the removeprefix method.

    Args:
    ----
        text: The text to remove the prefix from
        prefix: The prefix to remove from the text

    """
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def parse_test_case_names(test_case_name: str) -> TestCaseNameMatches:
    """Parse a test case name to extract test case ids.

    Args:
    ----
        test_case_name: The name of the test case

    Returns:
    -------
        TestCaseNameMatches: A model containing the test case name and the test case ids

    """
    # Remove leading and trailing whitespace from the test case name that was provided
    test_case_name = test_case_name.strip()
    applause_test_case_ids = []
    test_rail_test_case_ids = []

    # Find all the Applause test case ids in the test case name
    if search(r"Applause-\d+", test_case_name):
        # Remove the "Applause-" prefix from matched test case ids
        applause_test_case_ids: List[str] = [remove_prefix(str(match), "Applause-") for match in findall(r"Applause-\d+", test_case_name)]
        # Strip the Applause test case ids from the test case name
        test_case_name = subn(r"Applause-\d+", "", test_case_name)[0].strip()

    # Find all the TestRail test case ids in the test case name
    if search(r"TestRail-\d+", test_case_name):
        # Remove the "TestRail-" prefix from matched test case ids
        test_rail_test_case_ids: List[str] = [remove_prefix(str(match), "TestRail-") for match in findall(r"TestRail-\d+", test_case_name)]
        # Strip the TestRail test case ids from the test case name
        test_case_name = subn(r"TestRail-\d+", "", test_case_name)[0].strip()

    # Warn if multiple test case ids are detected in the test case name
    if len(applause_test_case_ids) > 1:
        print("Multiple Applause case ids detected in testCase name")
    if len(test_rail_test_case_ids) > 1:
        print("Multiple TestRail case ids detected in testCase name")

    # Extract out the first applause test case id from the list of test case ids
    applause_test_case_id = int(applause_test_case_ids[0]) if len(applause_test_case_ids) > 0 else None
    # Extract out the first testail test case id from the list of test case ids
    test_rail_test_case_id = int(test_rail_test_case_ids[0]) if len(test_rail_test_case_ids) > 0 else None

    # Return the matches and cleaned test case name
    return TestCaseNameMatches(
        test_case_name=test_case_name,
        test_rail_test_case_id=test_rail_test_case_id,
        applause_test_case_id=applause_test_case_id,
    )
