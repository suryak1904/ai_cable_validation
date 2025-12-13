from pypdf import PdfReader
def load_pdf(pdf_path: str):
    reader = PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append({
                "page": i + 1,
                "text": text.strip()
            })
    if not pages:
        raise RuntimeError("No text extracted.")
    return pages
