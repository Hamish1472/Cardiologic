import pytest
from functions.csv_utils import get_phone_number_from_email


def create_test_csv(tmp_path, rows):
    file_path = tmp_path / "test.csv"
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        f.write("Name,Age,Address,Zip,Email,Phone\n")  # Header
        for row in rows:
            f.write(",".join(row) + "\n")
    return file_path

def test_phone_number_found(tmp_path):
    rows = [
        ["Alice", "30", "123 Street", "12345", "alice@example.com", "555-1234"],
        ["Bob", "25", "456 Ave", "54321", "bob@example.com", "555-5678"],
    ]
    test_csv = create_test_csv(tmp_path, rows)
    result = get_phone_number_from_email(test_csv, "bob@example.com")
    assert result == "555-5678"

def test_phone_number_not_found(tmp_path):
    rows = [
        ["Alice", "30", "123 Street", "12345", "alice@example.com", "555-1234"],
    ]
    test_csv = create_test_csv(tmp_path, rows)
    result = get_phone_number_from_email(test_csv, "charlie@example.com")
    assert result == "Email or phone number not found"

def test_empty_csv(tmp_path):
    test_csv = tmp_path / "empty.csv"
    test_csv.write_text("Name,Age,Address,Zip,Email,Phone\n")  # Only header
    result = get_phone_number_from_email(test_csv, "someone@example.com")
    assert result == "Email or phone number not found"
