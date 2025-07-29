import pytest
from unittest import mock
from functions.sms_utils import send_sms
from vonage_sms import SmsMessage

# Dummy input values
API_Key = "dummy_key"
API_Secret = "dummy_secret"
SMS_Recipient = "1234567890"
SMS_SENDER_ID = "MyApp"
Password = "securePASS123"
EMAIL_SENDER = "noreply@example.com"  # Match what's in your config


@mock.patch("functions.sms_utils.Vonage")  # Patch the Vonage class itself
@mock.patch(
    "functions.sms_utils.Auth"
)  # Patch the Auth class used to initialize Vonage
def test_send_sms_success(mock_auth, mock_vonage):
    mock_client_instance = mock.Mock()
    mock_vonage.return_value = mock_client_instance

    mock_sms = mock.Mock()
    mock_client_instance.sms = mock_sms

    send_sms(API_Key, API_Secret, SMS_Recipient, SMS_SENDER_ID, Password)

    # Check that Vonage(Auth(...)) was called correctly
    mock_auth.assert_called_once_with(api_key=API_Key, api_secret=API_Secret)
    mock_vonage.assert_called_once_with(mock_auth.return_value)

    # Check that sms.send was called once with a SmsMessage instance
    assert mock_sms.send.call_count == 1

    args, kwargs = mock_sms.send.call_args
    sent_message = args[0]
    assert isinstance(sent_message, SmsMessage)
    assert sent_message.to == SMS_Recipient
    assert sent_message.from_ == SMS_SENDER_ID
    assert Password in sent_message.text
    assert EMAIL_SENDER in sent_message.text
