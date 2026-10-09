from collections import Counter
from typing import TypedDict
import re


class Chunk(TypedDict):
    chunk_id: str
    page: int
    text: str


def find_repeated_lines(
    pages: list[dict],
    min_occurrences: int = 3,
) -> set[str]:
    """
    Find lines that appear repeatedly across the document.
    """

    line_counts = Counter()

    for page in pages:
        lines = page["text"].splitlines()

        normalized_lines = {
            " ".join(line.split())
            for line in lines
            if line.strip()
        }

        line_counts.update(normalized_lines)

    return {
        line
        for line, count in line_counts.items()
        if count >= min_occurrences
    }


def clean_page_text(
    text: str,
    repeated_lines: set[str],
) -> str:
    """
    Remove repeated PDF artifacts and normalize whitespace.
    """

    cleaned_lines = []

    for line in text.splitlines():
        normalized_line = " ".join(line.split())

        if not normalized_line:
            continue

        if normalized_line in repeated_lines:
            continue

        cleaned_lines.append(normalized_line)

    return " ".join(cleaned_lines)


def split_into_sentences(text: str) -> list[str]:
    """
    Split text into sentences using a simple regex.

    This is intentionally a lightweight baseline rather than
    a full natural-language sentence tokenizer.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text,
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
) -> list[Chunk]:
    """
    Split pages into sentence-aware chunks.

    Sentences are combined until adding another sentence
    would exceed the target chunk size.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    repeated_lines = find_repeated_lines(pages)

    chunks = []

    for page in pages:
        page_number = page["page"]

        text = clean_page_text(
            page["text"],
            repeated_lines,
        )

        if not text:
            continue

        sentences = split_into_sentences(text)

        current_chunk = ""
        chunk_number = 0

        for sentence in sentences:

            # A single sentence is already larger than our
            # target size. Keep it intact rather than cutting
            # it in the middle.
            if len(sentence) > chunk_size:
                if current_chunk:
                    chunks.append(
                        {
                            "chunk_id": (
                                f"page_{page_number}_chunk_{chunk_number}"
                            ),
                            "page": page_number,
                            "text": current_chunk,
                        }
                    )

                    chunk_number += 1
                    current_chunk = ""

                chunks.append(
                    {
                        "chunk_id": (
                            f"page_{page_number}_chunk_{chunk_number}"
                        ),
                        "page": page_number,
                        "text": sentence,
                    }
                )

                chunk_number += 1
                continue

            if not current_chunk:
                current_chunk = sentence
                continue

            candidate = f"{current_chunk} {sentence}"

            if len(candidate) <= chunk_size:
                current_chunk = candidate
            else:
                chunks.append(
                    {
                        "chunk_id": (
                            f"page_{page_number}_chunk_{chunk_number}"
                        ),
                        "page": page_number,
                        "text": current_chunk,
                    }
                )

                chunk_number += 1
                current_chunk = sentence

        if current_chunk:
            chunks.append(
                {
                    "chunk_id": (
                        f"page_{page_number}_chunk_{chunk_number}"
                    ),
                    "page": page_number,
                    "text": current_chunk,
                }
            )

    return chunks
