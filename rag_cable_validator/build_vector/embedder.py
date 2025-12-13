from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
    return _model

def encode(texts):
    model = get_model()
    return model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )
