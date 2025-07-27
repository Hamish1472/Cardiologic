import pytest
import csv
from functions.csv_utils import (
    get_phone_number_from_email,
    parse_international_phone_number,
)


def test_parse_international_phone_number_valid():
    assert parse_international_phone_number("+4407368166834") == "+447368166834"
    assert parse_international_phone_number("447368166834") == "+447368166834"
    assert parse_international_phone_number("+15555555555") == "+15555555555"


def test_parse_international_phone_number_invalid():
    assert parse_international_phone_number("12345") == "Invalid"
    assert parse_international_phone_number("") == "Invalid"


def test_get_phone_number_from_email(tmp_path):
    # Create a mock CSV file
    csv_file = tmp_path / "contacts.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["First", "Last", "Company", "Title", "Email", "Phone"])
        writer.writerow(
            ["John", "Doe", "TestCorp", "Manager", "john@example.com", "+4407368166834"]
        )
        writer.writerow(
            [
                "Jane",
                "Smith",
                "TestCorp",
                "Engineer",
                "jane@example.com",
                "+15555555555",
            ]
        )

    # Valid email
    result = get_phone_number_from_email(str(csv_file), "john@example.com")
    assert result == "+447368166834"

    result = get_phone_number_from_email(str(csv_file), "jane@example.com")
    assert result == "+15555555555"

    # Invalid email
    result = get_phone_number_from_email(str(csv_file), "nobody@example.com")
    assert result == "Email or phone number not found"
