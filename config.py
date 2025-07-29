import os
from dotenv import load_dotenv

load_dotenv()

VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


INPUT_PDF_FOLDER = "input_pdfs"
OUTPUT_FOLDER = "output_archives"
SMS_SENDER_ID = "Cardiologic"
CSV_PATH = "data/ECG Consent - Sheet1(1).csv"
SUCCESSFUL_PDFS = "output_archives/sent/"
FAILED_PDFS = "output_archives/failed_to_send/"
FAILED_PDF_ENCRYPTIONS = "input_pdfs/failed_to_encrypt"


SEVEN_ZIP_PATH = "7z"  # or full path e.g., "C:/Program Files/7-Zip/7z.exe"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


HOSTNAME = "https://your-api-host.com"
OAUTH_URL = f"{HOSTNAME}/oauth/token"
LOGIN_URL = f"{HOSTNAME}/api/v1/user/login"
STUDIES_URL = f"{HOSTNAME}/api/v1/studies"
DOWNLOAD_URL_TEMPLATE = f"{HOSTNAME}/api/v1/studies/{{sid}}/download"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

POLL_INTERVAL = 60  # in seconds
SEEN_IDS_FILE = "seen_ids.json"
