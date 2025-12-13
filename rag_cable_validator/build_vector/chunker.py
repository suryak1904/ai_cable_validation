import re
def chunk_pages(pages, max_len=400):
    chunks = []
    buffer = ""
    start_page = None
    for p in pages:
        text = re.sub(r"\s+", " ", p["text"])
        sentences = re.split(r"(?<=[.;])\s+", text)

        for s in sentences:
            if not buffer:
                start_page = p["page"]

            if len(buffer) + len(s) <= max_len:
                buffer += s + " "
            else:
                chunks.append({
                    "text": buffer.strip(),
                    "page": start_page
                })
                buffer = s + " "
                start_page = p["page"]

    if buffer:
        chunks.append({
            "text": buffer.strip(),
            "page": start_page
        })

    return chunks
