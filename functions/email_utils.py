from email.message import EmailMessage
from config import *
import mimetypes
import smtplib

MAX_ATTACHMENT_SIZE_MB = 25
MAX_ATTACHMENT_SIZE = MAX_ATTACHMENT_SIZE_MB * 1024 * 1024


def send_email(recipient, subject, body, attachment_path=None):
    """Send an email with attachment."""

    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    # Check attachment size before proceeding
    if attachment_path:
        attachment_size = os.path.getsize(attachment_path)
        if attachment_size > MAX_ATTACHMENT_SIZE:
            raise ValueError(
                f"Attachment too large ({attachment_size / (1024 * 1024):.2f} MB). "
                f"Maximum allowed size is {MAX_ATTACHMENT_SIZE_MB} MB."
            )

        # Attach file
        ctype, encoding = mimetypes.guess_type(attachment_path)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        with open(attachment_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype=maintype,
                subtype=subtype,
                filename=os.path.basename(attachment_path),
            )

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"Email sent to {recipient}")
