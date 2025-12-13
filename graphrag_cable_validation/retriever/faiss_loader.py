import faiss
import json
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
INDEX_PATH = "kg.index"
META_PATH = "kg_meta.json"

_model = None
_index = None
_kg = None

def load_faiss():
    global _model, _index, _kg
    if _index is None:
        _index = faiss.read_index(INDEX_PATH)
        _model = SentenceTransformer(MODEL_NAME)
        with open(META_PATH, "r", encoding="utf-8") as f:
            _kg = json.load(f)
    return _index, _kg, _model
