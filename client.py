import requests
import time
import os
import json
import logging
from config import *


os.makedirs(INPUT_PDF_FOLDER, exist_ok=True)


# === Helper Functions ===
def get_oauth_token():
    response = requests.post(
        OAUTH_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )
    response.raise_for_status()
    return response.json()["access_token"]


def user_login(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        LOGIN_URL, json={"username": USERNAME, "password": PASSWORD}, headers=headers
    )
    response.raise_for_status()
    return response.json()["access_token"]


def get_studies(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "limit": 50,
        "order_by": "studies.recorded_at",
        "order_by_direction": "DESC",
    }
    response = requests.get(STUDIES_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def download_pdf(sid, access_token):
    url = DOWNLOAD_URL_TEMPLATE.format(sid=sid)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    file_path = os.path.join(INPUT_PDF_FOLDER, f"{sid}.pdf")
    with open(file_path, "wb") as f:
        f.write(response.content)
    logging.info(f"Downloaded report {sid} to {file_path}")


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
        client_token = get_oauth_token()
        access_token = user_login(client_token)

        while True:
            try:
                studies = get_studies(access_token)
                for study in studies:
                    sid = study.get("sid")
                    if sid and sid not in seen_ids:
                        logging.info(f"New report detected: {sid}")
                        download_pdf(sid, access_token)
                        seen_ids.add(sid)
                        save_seen_ids(seen_ids)
            except Exception as e:
                logging.error(f"Error fetching or processing studies: {e}")

            time.sleep(POLL_INTERVAL)
    except Exception as e:
        logging.error(f"Startup error: {e}")


if __name__ == "__main__":
    main()
