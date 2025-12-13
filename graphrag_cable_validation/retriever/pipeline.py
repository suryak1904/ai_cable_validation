from retriever.faiss_loader import load_faiss

def retrieve_context(user_text,top_k=5):
    index, kg, model = load_faiss()
    user_emb = model.encode([user_text], convert_to_numpy=True).astype("float32")
    _, indices = index.search(user_emb, top_k)
    return [kg[i] for i in indices[0] if i < len(kg)]
