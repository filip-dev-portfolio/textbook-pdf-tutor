from app.retriever import Retriever
from app.llm import LocalLLM


class RAG:

    def __init__(
        self,
        retriever: Retriever,
        llm: LocalLLM,
    ):
        self.retriever = retriever
        self.llm = llm

    def answer(
        self,
        question: str,
        top_k: int = 5,
    ) -> dict:

        results = self.retriever.search(
            question,
            top_k=top_k,
        )

        context_parts = []

        for i, result in enumerate(results, start=1):

            chunk = result["chunk"]

            context_parts.append(
                f"[SOURCE {i} | Page {chunk['page']}]\n"
                f"{chunk['text']}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
    You are a helpful textbook tutor.

    Answer the user's question using ONLY the provided
    textbook context.

    IMPORTANT RULES:

    1. Do not use outside knowledge.
    2. Do not invent facts.
    3. Every factual claim should be supported by one
    or more of the provided sources.
    4. Cite the source immediately after the claim using
    [SOURCE N].
    5. If the context does not contain enough information,
    say so.
    6. Do not cite a source unless it actually supports
    the claim.

    TEXTBOOK CONTEXT:

    {context}

    QUESTION:

    {question}

    Provide a clear and concise answer with citations.
    """

        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "sources": results,
        }