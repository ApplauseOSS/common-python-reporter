"""Tests for the utils module."""
import responses
from applause.common_python_reporter.auto_api import AutoApi, ApplauseConfig
from applause.common_python_reporter.email_helper import EmailHelper

class TestEmailHelper:
    """Tests for the parse_test_case_names function."""

    @responses.activate
    def test_email_parsing(self):
        """Test the parse_test_case_names function."""
        auto_api_mock = AutoApi(config=ApplauseConfig(
            api_key='test',
            product_id=123
        ))
        email_helper = EmailHelper(auto_api_mock)
        responses.add('GET', 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/email/get-address?emailPrefix=test', json={'email_address': 'test123@test.com'})
        with open('tests/data/test_email.eml') as f:
            email = f.read()
            responses.add('POST', 'https://prod-auto-api.cloud.applause.com:443/api/v1.0/email/download-email', body=email)
        inbox = email_helper.get_inbox('test')

        assert inbox.email_address == 'test123@test.com'

        email = inbox.getEmail()

        assert email is not None

        assert email['subject'] == 'The Subject Line'
        assert email['from'] == '"from@example.com" <from@example.com>'
        assert email['to'] == '"to@example.com" <to@example.com>'
        assert email.is_multipart()
        # Find the attachment
        attachments = [ part for part in email.get_payload() if part.get_content_disposition() == 'attachment']
        assert len(attachments) == 1
        attachment = attachments[0]
        assert attachment.get_filename() == 'cat.jpg'

        # To find the body, we need to find the multipart part that is not an attachment
        additional_parts = [ part for part in email.get_payload() if part.get_content_disposition() != 'attachment']
        assert len(additional_parts) == 1
        additional_part = additional_parts[0]
        assert additional_part.is_multipart()

        # Within that part, find the text/plain part, which contains the body as a plain string
        text_body_parts = [ part for part in additional_part.get_payload() if part.get_content_type() == 'text/plain']
        assert len(text_body_parts) == 1
        assert text_body_parts[0].get_payload() == 'This is the content'

