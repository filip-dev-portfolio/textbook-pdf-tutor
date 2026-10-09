from pathlib import Path
import hashlib

import streamlit as st

from app.llm import LocalLLM
from app.rag import RAG
from app.retriever import Retriever
from app.textbook_store import TextbookStore
from app.ingestion import process_pdf


# --------------------------------------------------
# Streamlit configuration
# --------------------------------------------------

st.set_page_config(
    page_title="PDF Tutor",
    page_icon="📚",
    layout="wide",
)


# --------------------------------------------------
# RAG loader
# --------------------------------------------------

@st.cache_resource
def load_rag(book_dir: str) -> RAG:
    """
    Load and cache the RAG pipeline for a textbook.
    """

    book_dir = Path(book_dir)

    retriever = Retriever(
        embeddings_path=book_dir / "embeddings.npy",
        chunks_path=book_dir / "chunks.json",
    )

    llm = LocalLLM()

    return RAG(
        retriever=retriever,
        llm=llm,
    )


# --------------------------------------------------
# File hashing
# --------------------------------------------------

def get_file_hash(file_bytes: bytes) -> str:
    """
    Generate a SHA-256 hash to identify PDF contents.
    """

    return hashlib.sha256(file_bytes).hexdigest()


# --------------------------------------------------
# Initialize session state
# --------------------------------------------------

if "upload_version" not in st.session_state:
    st.session_state["upload_version"] = 0

if "uploaded_file_hash" not in st.session_state:
    st.session_state["uploaded_file_hash"] = None

if "active_book_id" not in st.session_state:
    st.session_state["active_book_id"] = None

if "active_book_dir" not in st.session_state:
    st.session_state["active_book_dir"] = None


# --------------------------------------------------
# App
# --------------------------------------------------

st.title("📚 PDF Tutor")

st.write("Ask questions about your textbook.")


# --------------------------------------------------
# Textbook store
# --------------------------------------------------

store = TextbookStore()


# --------------------------------------------------
# Choose textbook source
# --------------------------------------------------

st.subheader("Textbook")

source = st.radio(
    "Choose textbook source",
    options=[
        "Existing textbook",
        "Upload new textbook",
    ],
    horizontal=True,
)


# ==================================================
# EXISTING TEXTBOOK
# ==================================================

if source == "Existing textbook":

    available_books = store.list_textbooks()

    if not available_books:
        st.warning(
            "No textbooks are available. Please upload a PDF."
        )
        st.stop()

    # Keep the current selection if it still exists.
    current_book = st.session_state["active_book_id"]

    default_index = (
        available_books.index(current_book)
        if current_book in available_books
        else 0
    )

    selected_book = st.selectbox(
        "Select a textbook",
        options=available_books,
        index=default_index,
    )

    book_dir = store.get_textbook_dir(selected_book)

    st.session_state["active_book_id"] = selected_book
    st.session_state["active_book_dir"] = str(book_dir)


# ==================================================
# UPLOAD NEW TEXTBOOK
# ==================================================

else:

    upload_key = (
        f"textbook_upload_{st.session_state['upload_version']}"
    )

    uploaded_file = st.file_uploader(
        "Upload a textbook PDF",
        type=["pdf"],
        key=upload_key,
    )

    if uploaded_file is None:
        st.info(
            "Upload a PDF to create or load a textbook."
        )
        st.stop()

    pdf_bytes = uploaded_file.getvalue()
    file_hash = get_file_hash(pdf_bytes)

    previous_hash = st.session_state["uploaded_file_hash"]

    # --------------------------------------------------
    # DEBUG: upload state
    # --------------------------------------------------

    st.write("DEBUG: Filename:", uploaded_file.name)
    st.write("DEBUG: Current hash:", file_hash)
    st.write("DEBUG: Previous hash:", previous_hash)

    # --------------------------------------------------
    # Process a new PDF
    # --------------------------------------------------

    if file_hash != previous_hash:

        st.write("DEBUG: New file detected")

        try:
            with st.spinner("Processing textbook..."):

                book_id, book_dir = store.create_textbook_from_bytes(
                    filename=uploaded_file.name,
                    pdf_bytes=pdf_bytes,
                )

                process_pdf(
                    pdf_path=book_dir / "textbook.pdf",
                    output_dir=book_dir,
                )

            # Update state only after processing succeeds.
            st.session_state["uploaded_file_hash"] = file_hash
            st.session_state["active_book_id"] = book_id
            st.session_state["active_book_dir"] = str(book_dir)

            st.success(f"Loaded textbook: {book_id}")

            # Give the next upload a fresh widget key.
            st.session_state["upload_version"] += 1

            # Rerun to refresh the uploader widget.
            st.rerun()

        except Exception as exc:
            st.error(
                f"Textbook processing failed: {exc}"
            )
            st.exception(exc)
            st.stop()

    else:

        st.write("DEBUG: File hash matches previous upload")

        # Restore the active textbook only if its state exists.
        active_book_id = st.session_state["active_book_id"]
        active_book_dir = st.session_state["active_book_dir"]

        if active_book_id is None or active_book_dir is None:
            st.error(
                "The uploaded file matches the previous upload, "
                "but no active textbook is stored in the session."
            )
            st.stop()

        book_dir = Path(active_book_dir)


# --------------------------------------------------
# Validate active textbook
# --------------------------------------------------

active_book_id = st.session_state["active_book_id"]
active_book_dir = st.session_state["active_book_dir"]

if not active_book_id or not active_book_dir:
    st.warning("No textbook is currently active.")
    st.stop()

if not Path(active_book_dir).exists():
    st.error(f"Textbook directory not found: {active_book_dir}")
    st.stop()


# --------------------------------------------------
# Active textbook
# --------------------------------------------------

st.info(f"📖 Active textbook: **{active_book_id}**")


# --------------------------------------------------
# Load RAG
# --------------------------------------------------

try:
    rag = load_rag(active_book_dir)
except Exception as exc:
    st.error(f"Could not load the RAG pipeline: {exc}")
    st.exception(exc)
    st.stop()


# --------------------------------------------------
# Question
# --------------------------------------------------

question = st.text_input(
    "Ask a question",
    placeholder="What are some uses of standardized tests?",
)


# --------------------------------------------------
# Retrieval settings
# --------------------------------------------------

top_k = st.slider(
    "Number of retrieved chunks",
    min_value=1,
    max_value=10,
    value=5,
)


# --------------------------------------------------
# Ask
# --------------------------------------------------

if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Thinking..."):
                result = rag.answer(
                    question,
                    top_k=top_k,
                )

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Sources")

            for i, source in enumerate(
                result["sources"],
                start=1,
            ):
                chunk = source["chunk"]

                st.write(
                    f"**[SOURCE {i}]** "
                    f"Page {chunk['page']} "
                    f"(distance: {source['distance']:.4f})"
                )

        except Exception as exc:
            st.error(f"Question answering failed: {exc}")
            st.exception(exc)