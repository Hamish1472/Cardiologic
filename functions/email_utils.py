from email.message import EmailMessage
from config import *
import mimetypes
import smtplib

def send_email(recipient, subject, body, attachment_path):
    """Send an email with attachment."""
    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    # Attach file
    ctype, encoding = mimetypes.guess_type(attachment_path)
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