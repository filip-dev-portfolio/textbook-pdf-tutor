from pathlib import Path

import faiss
import numpy as np

from app.embeddings import EmbeddingModel
from app.vector_store import VectorStore


class Retriever:

    def __init__(
        self,
        embeddings_path: str | Path,
        chunks_path: str | Path,
    ):
        self.store = VectorStore(
            embeddings_path=embeddings_path,
            chunks_path=chunks_path,
        )

        self.store.load()

        self.embeddings = self.store.embeddings
        self.chunks = self.store.chunks

        dimension = self.embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(
            self.embeddings.astype(np.float32)
        )

        self.embedding_model = EmbeddingModel()

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:

        query_embedding = self.embedding_model.embed_texts(
            [query]
        )

        query_embedding = (
            query_embedding
            .detach()
            .cpu()
            .numpy()
            .astype(np.float32)
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0],
        ):
            results.append(
                {
                    "chunk": self.chunks[index],
                    "distance": float(distance),
                }
            )

        return results
