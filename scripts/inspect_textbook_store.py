from app.textbook_store import TextbookStore


store = TextbookStore()

book_id, book_dir = store.create_textbook(
    "data/textbook.pdf"
)

print("Book ID:")
print(book_id)

print("\nBook directory:")
print(book_dir)

print("\nAvailable textbooks:")

for textbook in store.list_textbooks():
    print("-", textbook)
