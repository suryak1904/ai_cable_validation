import json
import uuid
from llm_client import call_llm
from prompt import extraction_prompt

def extract_kg_facts(page_data):
    prompt = extraction_prompt(page_data["text"], page_data["page"])
    llm_output = call_llm(prompt)
    try:
        data = json.loads(llm_output)
    except json.JSONDecodeError as e:
        print(f" JSON parse error on page {page_data['page']}")
        print(llm_output)
        return []
    if isinstance(data, dict) and "facts" in data:
        data = data["facts"]
    if isinstance(data, list) and len(data) == 1 and isinstance(data[0], list):
        data = data[0]
    if not isinstance(data, list):
        return []

    kg_facts = []
    for fact in data:
        if not isinstance(fact, dict):
            continue
        if not fact.get("parameter") or not fact.get("value"):
            continue
        kg_facts.append({
            "fact_id": str(uuid.uuid4()),
            "parameter": fact.get("parameter"),
            "constraint_type": fact.get("constraint_type", "unknown"),
            "value": fact.get("value"),
            "unit": fact.get("unit"),
            "context": fact.get("context"),
            "source": fact.get("source")
        })

    return kg_facts
