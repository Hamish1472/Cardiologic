import pytest
from unittest import mock
from functions.email_utils import send_email, MAX_ATTACHMENT_SIZE_MB
import os

# Example recipient, subject, and body
RECIPIENT = "test@example.com"
SUBJECT = "Test Subject"
BODY = "This is a test email body."


@mock.patch("smtplib.SMTP")
def test_send_email_without_attachment(mock_smtp):
    send_email(RECIPIENT, SUBJECT, BODY)

    instance = mock_smtp.return_value.__enter__.return_value
    instance.starttls.assert_called_once()
    instance.login.assert_called_once()
    instance.send_message.assert_called_once()


@mock.patch("smtplib.SMTP")
@mock.patch("os.path.getsize", return_value=1 * 1024 * 1024)  # 1 MB
@mock.patch("builtins.open", new_callable=mock.mock_open, read_data=b"file content")
def test_send_email_with_small_attachment(mock_open, mock_getsize, mock_smtp):
    send_email(RECIPIENT, SUBJECT, BODY, attachment_path="dummy.txt")

    instance = mock_smtp.return_value.__enter__.return_value
    instance.send_message.assert_called_once()
    mock_getsize.assert_called_once_with("dummy.txt")
    mock_open.assert_called_once_with("dummy.txt", "rb")


@mock.patch("os.path.getsize", return_value=(MAX_ATTACHMENT_SIZE_MB + 1) * 1024 * 1024)
def test_send_email_attachment_too_large(mock_getsize):
    with pytest.raises(ValueError, match="Attachment too large"):
        send_email(RECIPIENT, SUBJECT, BODY, attachment_path="bigfile.txt")
