from pathlib import Path

from app.chunker import chunk_pages
from app.embeddings import EmbeddingModel
from app.pdf_processor import extract_pages
from app.vector_store import VectorStore


def process_pdf(
    pdf_path: str | Path,
    output_dir: str | Path,
) -> None:
    """
    Process a PDF into chunks and embeddings.

    The output directory belongs to one textbook.
    """

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Extracting PDF...")

    pages = extract_pages(pdf_path)

    print(
        f"Extracted {len(pages)} pages."
    )

    print("Chunking...")

    chunks = chunk_pages(pages)

    print(
        f"Created {len(chunks)} chunks."
    )

    print("Loading embedding model...")

    embedding_model = EmbeddingModel()

    print("Generating embeddings...")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedding_model.embed_texts(
        texts
    )

    print(
        "Generated embeddings with shape "
        f"{tuple(embeddings.shape)}"
    )

    store = VectorStore(
        embeddings_path=output_dir / "embeddings.npy",
        chunks_path=output_dir / "chunks.json",
    )

    store.save(
        embeddings=embeddings,
        chunks=chunks,
    )

    print("Vector data saved.")
