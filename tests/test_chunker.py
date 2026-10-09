from app.chunker import (
    chunk_pages,
    clean_page_text,
    find_repeated_lines,
    split_into_sentences,
)


def test_find_repeated_lines():
    pages = [
        {
            "page": 1,
            "text": "Header\nFirst page content\nFooter",
        },
        {
            "page": 2,
            "text": "Header\nSecond page content\nFooter",
        },
        {
            "page": 3,
            "text": "Header\nThird page content\nFooter",
        },
    ]

    repeated = find_repeated_lines(
        pages,
        min_occurrences=3,
    )

    assert "Header" in repeated
    assert "Footer" in repeated


def test_clean_page_text():
    text = """Header
This is useful content.
Footer"""

    cleaned = clean_page_text(
        text,
        {"Header", "Footer"},
    )

    assert cleaned == "This is useful content."


def test_split_into_sentences():
    text = "This is sentence one. This is sentence two!"

    sentences = split_into_sentences(text)

    assert sentences == [
        "This is sentence one.",
        "This is sentence two!",
    ]


def test_chunk_pages():
    pages = [
        {
            "page": 1,
            "text": (
                "This is the first sentence. "
                "This is the second sentence. "
                "This is the third sentence."
            ),
        }
    ]

    chunks = chunk_pages(
        pages,
        chunk_size=50,
    )

    assert len(chunks) == 3

    assert chunks[0]["text"] == "This is the first sentence."
    assert chunks[1]["text"] == "This is the second sentence."
    assert chunks[2]["text"] == "This is the third sentence."

    assert chunks[0]["page"] == 1
    assert chunks[0]["chunk_id"] == "page_1_chunk_0"
    assert chunks[1]["chunk_id"] == "page_1_chunk_1"
    assert chunks[2]["chunk_id"] == "page_1_chunk_2"
