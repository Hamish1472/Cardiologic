import pytest
from unittest import mock
from functions.encryption_utils import generate_password, compress_pdf, zip_archive


def test_generate_password():
    password = generate_password()
    assert isinstance(password, str)
    assert len(password) == 16


@mock.patch("subprocess.run")
def test_compress_pdf_runs_7zip(mock_run):
    compress_pdf("file.pdf", "archive.7z", "secure123")

    # Check that subprocess.run was called correctly
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]  # get list of command-line args

    assert "file.pdf" in args
    assert "archive.7z" in args
    assert "-psecure123" in args
    assert "-mhe=on" in args


@mock.patch("shutil.make_archive")
def test_zip_archive_wraps_7z(mock_make_archive):
    zip_archive("folder/myfile.7z", "wrapped.zip")

    mock_make_archive.assert_called_once()
    args, kwargs = mock_make_archive.call_args

    # Positional args: base_name and format
    assert args[0] == "wrapped"
    assert args[1] == "zip"

    # Keyword args: root_dir and base_dir
    assert kwargs["root_dir"] == "folder"
    assert kwargs["base_dir"] == "myfile.7z"
