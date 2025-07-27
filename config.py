import os
from dotenv import load_dotenv

load_dotenv()

VONAGE_API_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


INPUT_PDF_FOLDER = "./input_pdfs"
OUTPUT_FOLDER = "./output_archives"
SMS_SENDER_ID = "Cardiologic"
CSV_PATH = "./Consent.csv"
SUCCESSFUL_PDFS = "./sent_pdfs"
FAILED_PDFS = "./failed_pdfs"

SEVEN_ZIP_PATH = "7z" # or full path e.g., "C:/Program Files/7-Zip/7z.exe"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
