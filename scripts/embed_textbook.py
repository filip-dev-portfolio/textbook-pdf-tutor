from pathlib import Path

from app.pdf_processor import extract_pages
from app.chunker import chunk_pages
from app.embeddings import EmbeddingModel
from app.vector_store import VectorStore


PDF_PATH = Path("data/textbook.pdf")

EMBEDDINGS_PATH = Path("data/embeddings.npy")
CHUNKS_PATH = Path("data/chunks.json")


def main():
    print("Extracting PDF...")

    pages = extract_pages(PDF_PATH)

    print(f"Pages: {len(pages)}")

    print("Creating chunks...")

    chunks = chunk_pages(pages)

    print(f"Chunks: {len(chunks)}")

    print("\nLoading embedding model...")

    model = EmbeddingModel()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print("Generating embeddings...")

    embeddings = model.embed_texts(texts)

    print(f"Embedding shape: {embeddings.shape}")
    print(f"Embedding device: {embeddings.device}")

    print("\nSaving vector store...")

    store = VectorStore(
        embeddings_path=EMBEDDINGS_PATH,
        chunks_path=CHUNKS_PATH,
    )

    store.save(
        embeddings=embeddings,
        chunks=chunks,
    )

    print("Saved successfully.")

    print(f"Embeddings: {EMBEDDINGS_PATH}")
    print(f"Chunks: {CHUNKS_PATH}")


if __name__ == "__main__":
    main()
