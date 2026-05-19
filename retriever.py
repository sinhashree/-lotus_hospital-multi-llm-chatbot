import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# LOAD MODEL ONLY ONCE
# -------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load saved embeddings + texts
embeddings = np.load("embeddings.npy")
texts = np.load("texts.npy", allow_pickle=True)


# -------------------------------
# RETRIEVER FUNCTION
# -------------------------------
def retrieve_top_k(query, k=3):

    # Convert query into embedding
    query_embedding = model.encode([query])

    # Similarity search
    similarities = cosine_similarity(query_embedding, embeddings)[0]

    # Get top matches
    top_k_indices = similarities.argsort()[-k:][::-1]

    # Retrieve text chunks
    results = [texts[i] for i in top_k_indices]

    return "\n".join(results)