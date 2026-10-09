from pathlib import Path

from app.chunker import chunk_pages
from app.pdf_processor import extract_pages


PDF_PATH = Path("data/textbook.pdf")


pages = extract_pages(PDF_PATH)

chunks = chunk_pages(
    pages,
    chunk_size=1000,
)

print(f"Pages: {len(pages)}")
print(f"Chunks: {len(chunks)}")

for chunk in chunks[:5]:
    print("=" * 80)
    print(f"ID: {chunk['chunk_id']}")
    print(f"Page: {chunk['page']}")
    print("=" * 80)
    print(chunk["text"])
    print()
