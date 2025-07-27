from vonage import Auth, Vonage
from vonage_sms import SmsMessage, SmsResponse
from config import *


def send_sms(API_Key, API_Secret, SMS_Recipient, SMS_SENDER_ID, Password):
    client = Vonage(Auth(api_key=API_Key, api_secret=API_Secret))

    message = SmsMessage(
        to=SMS_Recipient,
        from_=SMS_SENDER_ID,
        text=f"Do Not Reply\n\nPassword to PDF: {Password}\n\nPlease check your spam folder for an email from {EMAIL_SENDER} if you have not received the PDF",
    )

    response: SmsResponse = client.sms.send(message)
    print(response)