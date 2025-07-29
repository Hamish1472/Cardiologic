import shutil
from config import *
import functions.csv_utils, functions.email_utils, functions.encryption_utils, functions.sms_utils
import logging
from datetime import datetime

# Configure logging
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/main_{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":

    # Ensure output folders exist
    os.makedirs(SUCCESSFUL_PDFS, exist_ok=True)
    os.makedirs(FAILED_PDFS, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_FOLDER, "tmp"), exist_ok=True)

    for filename in os.listdir(INPUT_PDF_FOLDER):
        if filename.endswith(".pdf"):
            logging.info(f"Starting processing for: {filename}")

            # Set paths and email
            pdf_path = os.path.join(INPUT_PDF_FOLDER, filename)
            email_address = os.path.splitext(filename)[0]
            archive_name = f"{email_address}.7z"
            archive_path = os.path.join(OUTPUT_FOLDER, "tmp", archive_name)

            # Generate password
            password = functions.encryption_utils.generate_password()
            pdf_was_encrypted = False

            try:
                # Get Phone from Email
                phone_number = functions.csv_utils.get_phone_number_from_email(
                    CSV_PATH, email_address
                )

                # Compress and encrypt
                functions.encryption_utils.compress_pdf(
                    pdf_path, archive_path, password
                )
                pdf_was_encrypted = True
                with open("password_log.txt", "a") as file:
                    file.write(f"\n{filename} | {password}")
                logging.info(f"Encrypted archive created: {archive_path}")

                # Wrap inside zip
                zip_name = f"{email_address}.zip"
                zip_path = os.path.join(OUTPUT_FOLDER, "tmp", zip_name)
                functions.encryption_utils.zip_archive(archive_path, zip_path)
                logging.info(f"ZIP archive created: {zip_path}")

                base_body = (
                    "Hello,\n\nPlease find your encrypted PDF archive attached.\n"
                )

                subject = "Encrypted PDF Archive"

                # Determine SMS / password info
                if phone_number == "Email or phone number not found":
                    logging.warning(
                        f"Phone number not found for {email_address}, skipping SMS."
                    )
                    password_info = "Phone number not found in our records. Please contact us for the password."
                else:
                    password_info = (
                        f"Password sent to provided contact number: {phone_number}"
                    )

                # Now finalize body before sending the email
                full_body = base_body + password_info

                # Attempt to send the email
                functions.email_utils.send_email(
                    email_address, subject, full_body, zip_path
                )

                # Only send SMS if email succeeded and phone number was found
                if phone_number != "Email or phone number not found":
                    # functions.sms_utils.send_sms(
                    #     VONAGE_API_KEY,
                    #     VONAGE_API_SECRET,
                    #     phone_number,
                    #     SMS_SENDER_ID,
                    #     password,
                    # )
                    logging.info(
                        f"SMS sent successfully with password.\nRecipient: {phone_number}\nFilename: {archive_name}"
                    )

                shutil.move(zip_path, SUCCESSFUL_PDFS)

            except Exception as e:
                logging.error(f"Failed for {filename}: {e}", exc_info=True)
                functions.email_utils.send_email(
                    EMAIL_SENDER,
                    "Failed PDF Pipeline",
                    f"The pipeline failed for PDF: {filename} with exception: \n\n{e}",
                )
                if pdf_was_encrypted:
                    shutil.move(zip_path, FAILED_PDFS)
                else:
                    shutil.move(pdf_path, FAILED_PDF_ENCRYPTIONS)

            os.remove(pdf_path)
            logging.info(f"Finished processing for: {filename}")

    shutil.rmtree(os.path.join(OUTPUT_FOLDER, "tmp"))
