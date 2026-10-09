from pathlib import Path

from app.pdf_processor import extract_pages


PDF_PATH = Path("data/textbook.pdf")


pages = extract_pages(PDF_PATH)

print(f"Number of pages: {len(pages)}")

for page in pages[:3]:
    print("=" * 80)
    print(f"PAGE {page['page']}")
    print("=" * 80)
    print(page["text"][:1000])
    print()
