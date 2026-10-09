from pathlib import Path

import pymupdf


def extract_pages(pdf_path: str | Path) -> list[dict]:
    """
    Extract text from a PDF while preserving page numbers.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        A list of dictionaries containing page number and extracted text.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pages = []

    with pymupdf.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            pages.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

    return pages
