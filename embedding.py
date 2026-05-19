from sentence_transformers import SentenceTransformer
import numpy as np

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = []

# Read website data
with open('corpus_text.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()

        if line and not line.startswith("Chunk"):
            sentences.append(line)

print(f"Loaded {len(sentences)} sentences")

# Generate embeddings
embeddings = model.encode(sentences)

# Save embeddings + texts(creating vector database)
np.save('embeddings.npy', embeddings)
np.save('texts.npy', sentences)

print("Embeddings created successfully!")