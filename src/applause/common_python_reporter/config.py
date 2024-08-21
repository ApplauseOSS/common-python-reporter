"""Configuration Classes uses as parameters to interact with the Applause Services.

Typical usage example:

config = ApplauseConfig(
    api_key="api_key",
    product_id=123,
    test_rail_options=TestRailOptions(
        base_url="https://testrail.example.com/",
        user="user",
        password="password",
        project_id=123,
    ),
    applause_test_cycle_id=123,
)
auto_api = AutoApi(config)
public_api = PublicApi(config)
"""

from pydantic import BaseModel, Field
from typing import Optional
from .dtos import TestRailOptions


class ApplauseConfig(BaseModel):
    """Configuration used to generate Applause Clients.

    Attributes
    ----------
        auto_api_base_url: The base url for the auto api client
        public_api_base_url: The base url for the public api client
        api_key: The api key for the client
        product_id: The id of the product
        test_rail_options: The test rail options
        applause_test_cycle_id: The id of the test cycle

    """

    auto_api_base_url: str = Field(default="https://prod-auto-api.cloud.applause.com:443/")
    public_api_base_url: str = Field(default="https://prod-public-api.cloud.applause.com:443/")
    api_key: str
    product_id: int
    test_rail_options: Optional[TestRailOptions] = None
    applause_test_cycle_id: Optional[int] = None
