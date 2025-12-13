from text_loader import extract_pages_from_pdf
from kg_builder import extract_kg_facts
import json
import os

PDF_PATH = r" path of IEC_60502_searchable.pdf"
KG_PATH = "kg.json"

def load_existing_kg():
    if os.path.exists(KG_PATH):
        with open(KG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_kg(kg):
    with open(KG_PATH, "w", encoding="utf-8") as f:
        json.dump(kg, f, indent=2)

def fact_key(fact):
    return (
        fact.get("parameter"),
        fact.get("constraint_type"),
        fact.get("value"),
        fact.get("unit"),
        fact.get("source", {}).get("page")
    )

def run():
    pages = extract_pages_from_pdf(PDF_PATH)
    knowledge_graph = load_existing_kg()
    processed_pages = {
        f["source"]["page"]
        for f in knowledge_graph
        if isinstance(f.get("source"), dict) and "page" in f["source"]
    }
    existing_keys = {fact_key(f) for f in knowledge_graph}
    for page in pages:
        page_no = page["page"]
        print(f"Processing page {page_no}...")
        facts = extract_kg_facts(page)
        for f in facts:
            if fact_key(f) not in existing_keys:
                knowledge_graph.append(f)
                existing_keys.add(fact_key(f))
        save_kg(knowledge_graph)
    print(f" KG build completed. Total facts: {len(knowledge_graph)}")

if __name__ == "__main__":
    run()
