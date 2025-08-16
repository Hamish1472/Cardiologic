import requests
import time
import os
import json
import logging
from datetime import datetime
import subprocess
from config import *


os.makedirs(INPUT_PDF_FOLDER, exist_ok=True)

os.makedirs("logs", exist_ok=True)
log_filename = f"logs/client_{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.info("#" * 100)


# === Helper Functions ===
def tokens():
    response = requests.post(
        OAUTH_URL,
        data={
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "username": QT_USERNAME,
            "password": QT_PASSWORD,
        },
    )
    response.raise_for_status()
    return response.json()


def refresh_token(refresh_token):
    response = requests.get(
        OAUTH_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )
    response.raise_for_status()
    return response.json()


# def upload_pdf():
#     with open("test_pdf_store/ECG_report.pdf", "rb") as file:
#         response = requests.get(
#             HOSTNAME + "/api/v1/pdf-upload",
#             data={
#                 "MRN": "hamish1472@gmail.com",
#                 "client_id": CLIENT_ID,
#                 "client_secret": CLIENT_SECRET,
#             },
#             files={"file": ("test_pdf_store/ECG_report.pdf", file, "application/pdf")},
#         )
#     response.raise_for_status()
#     return response.json()


def all_studies():
    offset = 0
    limit = 1000
    all_data = []  # collect everything here

    while True:
        response = requests.get(
            STUDIES_URL,
            headers={"Authorization": f"Bearer {tokens()['access_token']}"},
            params={
                "order_by": "studies.recorded_at",
                "order_by_direction": "DESC",
                "offset": offset,
                "limit": limit,
            },
        )
        response.raise_for_status()
        data = response.json()

        # extend studies list
        all_data.extend(data["studies"])

        # pagination check
        last_page = data["last_page"]
        current_page = data["current_page"]

        if current_page == last_page:
            break
        else:
            offset += limit

    return {"studies": all_data}


def get_study(sid):
    response = requests.get(
        STUDY_STATUS_URL.format(sid=sid),
        headers={"Authorization": f"Bearer {tokens()['access_token']}"},
    )
    response.raise_for_status()
    return response.json()


def get_pdf(sid, email):
    response = requests.get(
        PDF_URL.format(sid=sid),
        headers={"Authorization": f"Bearer {tokens()['access_token']}"},
    )
    response.raise_for_status()

    file_path = os.path.join(INPUT_PDF_FOLDER, f"{email}.pdf")
    with open(file_path, "wb") as f:
        f.write(response.content)
    logging.info(f"Downloaded report {sid} to {file_path}")

    return


def load_seen_ids():
    if os.path.exists(SEEN_IDS_FILE):
        with open(SEEN_IDS_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen_ids(seen_ids):
    with open(SEEN_IDS_FILE, "w") as f:
        json.dump(list(seen_ids), f)


def main():
    logging.info("Starting ECG report polling service...")

    seen_ids = load_seen_ids()

    try:

        while True:
            try:
                studies = all_studies()
                for study in studies["studies"]:
                    sid = study.get("sid")
                    status = study.get("status")
                    if sid and status in [3, 4, 5, 6] and sid not in seen_ids:
                        logging.info(f"New report detected: {sid}")
                        get_pdf(sid, study["patient_ie_mrn"])
                        try:
                            subprocess.run(
                                [
                                    "python",
                                    "core.py",
                                ],
                                check=True,
                            )
                        except subprocess.CalledProcessError as e:
                            logging.error(f"Failed for sid: {sid} : {e}")
                        seen_ids.add(sid)
                        save_seen_ids(seen_ids)
            except Exception as e:
                logging.error(f"Error fetching or processing studies: {e}")

            logging.info(
                f"No new reports detected, checking again in : {POLL_INTERVAL}s"
            )
            time.sleep(POLL_INTERVAL)
    except Exception as e:
        logging.error(f"Startup error: {e}")


if __name__ == "__main__":
    main()
