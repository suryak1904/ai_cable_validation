# build_index.py
from pdf_loader import load_pdf
from chunker import chunk_pages
from embedder import encode
from faiss_store import create_index, add_embeddings, save_index

PDF_PATH = r"E:\cable_validation\data\IEC_60502_searchable.pdf"
INDEX_DIR = "faiss_index"

def build_faiss_index():
    print(" Loading PDF.")
    pages = load_pdf(PDF_PATH)
    print(" Chunking IEC rules")
    chunks = chunk_pages(pages)
    texts = [c["text"] for c in chunks]
    print("Creating embeddings")
    embeddings = encode(texts)
    print("Building FAISS index")
    index = create_index(embeddings.shape[1])
    add_embeddings(index, embeddings)
    metadata = [
        {
            "text": c["text"],
            "page": c["page"]
        }
        for c in chunks
    ]

    save_index(index, metadata, INDEX_DIR)
    print("FAISS index built successfully")
    print(f" Total rules indexed: {len(metadata)}")


if __name__ == "__main__":
    build_faiss_index()
