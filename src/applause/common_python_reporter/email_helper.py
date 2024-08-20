"""Helper classes for generating email inboxes and fetching email content.

Typical usage example:

auto_api = AutoApi(config)
email_helper = EmailHelper(auto_api)
inbox = email_helper.get_inbox("test")
email = inbox.getEmail()
# Perform assertions on the email content
"""

from .auto_api import AutoApi
from .dtos import EmailFetchRequest
from email.message import Message


class Inbox:
    """An email inbox to fetch email messages from.

    Attributes
    ----------
        email_address (str): The email address of the inbox.
        auto_api (AutoApi): An instance of the AutoApi class.

    """

    def __init__(self, email_address: str, auto_api: AutoApi):
        """Initialize the Inbox object.

        Args:
        ----
            email_address (str): The email address of the inbox.
            auto_api (AutoApi): An instance of the AutoApi class.

        """
        self.auto_api = auto_api
        self.email_address = email_address

    def getEmail(self) -> Message:
        """Fetch the latest email from the Inbox.

        Returns
        -------
            Message: The email message content.

        """
        return self.auto_api.get_email_content(EmailFetchRequest(email_address=self.email_address))


class EmailHelper:
    """A helper class for generating email inboxes for testing purposes.

    Attributes
    ----------
        auto_api (AutoApi): An instance of the AutoApi class.

    """

    def __init__(self, auto_api: AutoApi):
        """Initialize the EmailHelper object.

        Args:
        ----
            auto_api (AutoApi): An instance of the AutoApi class.

        """
        self.auto_api = auto_api

    def get_inbox(self, prefix: str) -> Inbox:
        """Generate an inbox with the provided email prefix.

        Args:
        ----
            prefix (str): A prefix to be used when generating the email address of the inbox.

        """
        res = self.auto_api.get_email_address(prefix)
        return Inbox(email_address=res.email_address, auto_api=self.auto_api)
