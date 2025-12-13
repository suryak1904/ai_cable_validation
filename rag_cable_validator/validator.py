import json
import re
from prompt import build_validation_prompt
from qwen_llm import call_qwen

def extract_json(text: str):
    cleaned = text.replace("```json", "").replace("```", "")
    matches = re.findall(r"\{[\s\S]*?\}", cleaned)
    if not matches:
        raise ValueError("No JSON object found in LLM output")
    return json.loads(matches[-1])

def validate_with_llm(user_spec: str, rules: list[dict]):
    prompt = build_validation_prompt(user_spec, rules)
    raw = call_qwen(prompt)
    try:
        return extract_json(raw)
    except Exception as e:
        return {
            "overall_status": "UNKNOWN",
            "error": str(e),
            "raw_output": raw
        }
