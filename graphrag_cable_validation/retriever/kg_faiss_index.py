import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
INDEX_PATH = "kg.index"
META_PATH = "kg_meta.json"

def build_and_save_index(kg_path="kg.json"):
    with open(kg_path, "r", encoding="utf-8") as f:
        kg = json.load(f)
    model = SentenceTransformer(MODEL_NAME)
    texts = [
        f"{fact['parameter']} {fact.get('context', '')}"
        for fact in kg
    ]
    embeddings = model.encode(texts, convert_to_numpy=True).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(kg, f, indent=2)
    print("FAISS index built and saved.")

if __name__ == "__main__":
    build_and_save_index()
