import pytest
from utils.file_extract import extract_text_from_txt, extract_resume_text


def test_extract_text_from_txt_decodes_correctly():
    raw_bytes = "Hello, this is a resume.".encode("utf-8")
    result = extract_text_from_txt(raw_bytes)
    assert result == "Hello, this is a resume."


def test_extract_text_from_txt_strips_whitespace():
    raw_bytes = "   Padded text.   \n".encode("utf-8")
    result = extract_text_from_txt(raw_bytes)
    assert result == "Padded text."


def test_extract_resume_text_dispatches_txt_correctly():
    raw_bytes = "Plain text resume.".encode("utf-8")
    result = extract_resume_text("resume.txt", raw_bytes)
    assert result == "Plain text resume."


def test_extract_resume_text_raises_on_unsupported_format():
    with pytest.raises(ValueError, match="Unsupported file type"):
        extract_resume_text("resume.xyz", b"irrelevant content")


def test_extract_resume_text_is_case_insensitive_on_extension():
    raw_bytes = "Resume text.".encode("utf-8")
    result = extract_resume_text("resume.TXT", raw_bytes)
    assert result == "Resume text."