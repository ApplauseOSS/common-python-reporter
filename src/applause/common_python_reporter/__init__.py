"""A shared package for interacting with the Applause Automation Services.

Includes modules for interacting with the Applause Public API, Applause Automation API, and other utilities for testing.
This

Modules:
- auto_api: Module for interacting with the Applause Automation API.
- config: Configuration settings for the package.
- dtos: Data Transfer Objects for the Applause Automation API.
- email_helper: Helper for generating email inboxes for testing purposes.
- public_api: Module for interacting with the Applause Public API.
- reporter: A Module for easily managing the interactions with the Applause Automation API services.
            without keeping track of state or returned ids.
- utils: Utility functions for the package.
- version: Version of the package.
"""

from .config import ApplauseConfig
from .reporter import ApplauseReporter

__all__ = [ApplauseReporter, ApplauseConfig]
