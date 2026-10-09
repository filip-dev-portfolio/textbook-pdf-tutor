from app.retriever import Retriever
from app.llm import LocalLLM
from app.rag import RAG


retriever = Retriever(
    embeddings_path="data/embeddings.npy",
    chunks_path="data/chunks.json",
)

llm = LocalLLM()

rag = RAG(
    retriever=retriever,
    llm=llm,
)


question = "What are some uses of standardized tests?"

result = rag.answer(
    question,
    top_k=5,
)


print("\n====================")
print("ANSWER")
print("====================\n")

print(result["answer"])


print("\n====================")
print("SOURCES")
print("====================\n")

for i, source in enumerate(
    result["sources"],
    start=1,
):
    chunk = source["chunk"]

    print(
        f"[SOURCE {i}] "
        f"Page {chunk['page']} "
        f"(distance={source['distance']:.4f})"
    )
