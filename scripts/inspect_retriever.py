from app.retriever import Retriever


retriever = Retriever(
    embeddings_path="data/embeddings.npy",
    chunks_path="data/chunks.json",
)


query = "What are some uses of standardized tests?"

results = retriever.search(
    query,
    top_k=5,
)


for i, result in enumerate(results, start=1):

    print(f"\n--- Result {i} ---")

    print(
        "Distance:",
        result["distance"],
    )

    print(
        "Page:",
        result["chunk"]["page"],
    )

    print(
        result["chunk"]["text"]
    )

