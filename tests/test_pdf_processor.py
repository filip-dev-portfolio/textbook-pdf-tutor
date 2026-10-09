from pathlib import Path

from app.pdf_processor import extract_pages


PDF_PATH = Path("data/textbook.pdf")


def test_pdf_extraction():
    pages = extract_pages(PDF_PATH)

    assert len(pages) > 0

    for page in pages:
        assert "page" in page
        assert "text" in page
        assert isinstance(page["page"], int)
        assert isinstance(page["text"], str)
