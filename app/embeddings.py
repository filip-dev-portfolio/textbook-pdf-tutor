from sentence_transformers import SentenceTransformer
import torch


class EmbeddingModel:
    """
    Wrapper around a Sentence Transformer embedding model.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        device: str | None = None,
    ):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.device = device

        self.model = SentenceTransformer(
            model_name,
            device=device,
        )

    def embed_texts(
        self,
        texts: list[str],
    ) -> torch.Tensor:
        """
        Convert a list of texts into embedding vectors.
        """

        if not texts:
            raise ValueError("texts cannot be empty")

        embeddings = self.model.encode(
            texts,
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        return embeddings
