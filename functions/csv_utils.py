import csv
import phonenumbers


def get_phone_number_from_email(csv_file_path, target_email):
    """
    Looks up a phone number by email from a CSV file.
    Uses the headers to find the correct columns dynamically.
    """
    with open(csv_file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row.get("Email")
            phone = row.get("Phone")

            if (
                email
                and phone
                and email.strip().lower() == target_email.strip().lower()
            ):
                return parse_international_phone_number(phone)

    return "Email or phone number not found"


def parse_international_phone_number(phone_number):
    """
    Parses and formats a phone number in international format using the phonenumbers library.
    Returns a string in E.164 format like +447368166834.
    """
    if not phone_number.startswith("+"):
        phone_number = "+" + phone_number

    try:
        parsed = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed):
            formatted = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164
            )
            return formatted
        else:
            return "Invalid"
    except phonenumbers.NumberParseException:
        return "Invalid"
