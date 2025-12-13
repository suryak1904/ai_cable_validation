import pdfplumber

def extract_pages_from_pdf(pdf_path):
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and len(text.strip()) > 200:
                pages.append({
                    "page": i + 1,
                    "text": text.strip()
                })
    return pages
