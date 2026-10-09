from app.ingestion import process_pdf
from app.textbook_store import TextbookStore


store = TextbookStore()

book_id, book_dir = store.create_textbook(
    "data/psych.pdf"
)

print(
    f"\nTextbook ID: {book_id}"
)

print(
    f"Textbook directory: {book_dir}"
)

process_pdf(
    pdf_path=book_dir / "textbook.pdf",
    output_dir=book_dir,
)
