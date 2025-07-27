import shutil
from config import *
import functions.csv_utils, functions.email_utils, functions.encryption_utils, functions.sms_utils

if __name__ == '__main__':
    for filename in os.listdir(INPUT_PDF_FOLDER):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_PDF_FOLDER, filename)
            email_address = os.path.splitext(filename)[0]
            archive_name = f"{email_address}.7z"
            archive_path = os.path.join(OUTPUT_FOLDER, archive_name)
    
            # Generate password
            password = functions.encryption_utils.generate_password()
    
            # Compress and encrypt
            try:
                functions.encryption_utils.compress_pdf(pdf_path, archive_path, password)
                with open('password_log.txt', 'a') as file:
                    file.write(f"\n{filename} | {password}")
                print(f"Encrypted archive created: {archive_path}")
    
                # Wrap inside zip
                zip_name = f"{email_address}.zip"
                zip_path = os.path.join(OUTPUT_FOLDER, zip_name)
                functions.encryption_utils.zip_archive(archive_path, zip_path)
                print(f"ZIP archive created: {zip_path}")
    
                # Get Phone from Email
                phone_number = functions.csv_utils.get_phone_number_from_email(CSV_PATH, email_address)
    
                if phone_number == "Email or phone number not found":
                    print(f"Phone number not found for {email_address}, skipping SMS.")
                    body = f"Hello,\n\nPlease find your encrypted PDF archive attached.\nPhone number not found in our records. Please contact us for the password."
                else:
                    # Send Password via SMS
                    functions.sms_utils.send_sms(
                        VONAGE_API_KEY,
                        VONAGE_API_SECRET,
                        "44" + phone_number,
                        SMS_SENDER_ID,
                        password,
                    )
                    body = f"Hello,\n\nPlease find your encrypted PDF archive attached.\nPassword sent to provided contact number: {'*' * (len(phone_number) - 4) + phone_number[-4:]}"
    
                # Send ZIP via Email
                subject = "Encrypted PDF Archive"
                functions.email_utils.send_email(email_address, subject, body, zip_path)
                
                shutil.move(pdf_path, SUCCESSFUL_PDFS +"/")
                os.remove(archive_path)
    
            except Exception as e:
                print(f"Failed for {filename}: {e}")
                functions.email_utils.send_email(EMAIL_SENDER, "Failed PDF Pipeline", f"The pipeline failed for PDF: {filename} with exception: {e}", pdf_path)
                shutil.move(pdf_path, FAILED_PDFS + "/")