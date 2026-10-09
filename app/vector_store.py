from pathlib import Path
import json

import numpy as np
import torch


class VectorStore:
    """
    Simple persistent vector store.

    Stores:
    - embedding vectors
    - the chunk metadata associated with each vector
    """

    def __init__(
        self,
        embeddings_path: str | Path,
        chunks_path: str | Path,
    ):
        self.embeddings_path = Path(embeddings_path)
        self.chunks_path = Path(chunks_path)

        self.embeddings = None
        self.chunks = None

    def save(
        self,
        embeddings: torch.Tensor,
        chunks: list[dict],
    ) -> None:
        """
        Save embeddings and their corresponding chunks to disk.
        """

        if len(embeddings) != len(chunks):
            raise ValueError(
                "Number of embeddings must match number of chunks"
            )

        embeddings_cpu = embeddings.detach().cpu().numpy()

        np.save(
            self.embeddings_path,
            embeddings_cpu,
        )

        with open(
            self.chunks_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                chunks,
                file,
                ensure_ascii=False,
                indent=2,
            )

    def load(self) -> None:
        """
        Load embeddings and chunks from disk.
        """

        self.embeddings = np.load(
            self.embeddings_path,
        )

        with open(
            self.chunks_path,
            "r",
            encoding="utf-8",
        ) as file:
            self.chunks = json.load(file)

        if len(self.embeddings) != len(self.chunks):
            raise ValueError(
                "Number of embeddings does not match number of chunks"
            )
