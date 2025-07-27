# import csv

# def get_phone_number_from_email(csv_file_path, target_email):

#     address_book = {}

#     with open(csv_file_path, mode="r", newline="", encoding="utf-8") as file:
#         reader = csv.reader(file)
#         headers = next(reader)  # Skip header row
#         for row in reader:
#             email = row[4]  # Email csv index
#             phone = row[5]  # Telephone csv index
#             address_book[email] = phone

#     return address_book.get(target_email, "Email or phone number not found")

import csv
import phonenumbers


def get_phone_number_from_email(csv_file_path, target_email):
    address_book = {}

    with open(csv_file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip header row
        for row in reader:
            email = row[4]  # Email csv index
            phone = row[5]  # Telephone csv index
            address_book[email] = phone

    phone_number = address_book.get(target_email)
    if phone_number:
        country_code, local_number = parse_international_phone_number(phone_number)
        return country_code, local_number
    else:
        return "Email or phone number not found"

def parse_international_phone_number(phone_number):
    """
    Parses a phone number in international format using the phonenumbers library.
    Returns a tuple: (country_code, local_number_with_leading_zero_if_needed)
    """
    if not phone_number.startswith("+"):
        phone_number = "+" + phone_number

    try:
        parsed = phonenumbers.parse(phone_number, None)
        country_code = f"+{parsed.country_code}"
        national_number = str(parsed.national_number)

        # # Add leading zero if it's typical in the country
        # if phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL).startswith("0"):
        #     if not national_number.startswith("0"):
        #         national_number = "0" + national_number

        return country_code, national_number
    except phonenumbers.NumberParseException:
        return "Invalid", phone_number
    

print(parse_international_phone_number('4407368166834'))