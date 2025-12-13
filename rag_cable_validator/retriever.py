import numpy as np
from build_vector.embedder import encode
from build_vector.faiss_store import load_index

INDEX_DIR = "faiss_index"

def load_faiss():
    index, metadata = load_index(INDEX_DIR)
    return index, metadata

def retrieve_rules(query: str, k: int = 5):
    index, metadata = load_faiss()
    query_embedding = encode([query]).astype("float32")
    scores, indices = index.search(query_embedding, k)
    results = []
    for idx in indices[0]:
        results.append(metadata[idx])
    return results
