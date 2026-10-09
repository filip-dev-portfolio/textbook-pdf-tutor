import torch

from app.embeddings import EmbeddingModel


model = EmbeddingModel()

texts = [
    "Gradient descent updates model parameters using gradients.",
    "Neural networks learn by adjusting their weights during training.",
    "The capital of France is Paris.",
]

embeddings = model.embed_texts(texts)

print("Shape:", embeddings.shape)
print("Device:", embeddings.device)

similarities = torch.mm(
    embeddings,
    embeddings.T,
)

print("\nSimilarity matrix:")
print(similarities)
