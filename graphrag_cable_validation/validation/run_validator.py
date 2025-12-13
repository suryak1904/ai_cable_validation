from validation.validator import call_llm
from validation.validation_prompt import build_validation_prompt
import json

def validate(user_input: str, iec_facts: list) -> dict:
    if not iec_facts:
        return {
            "results": [
                {
                    "parameter": "N/A",
                    "status": "WARN",
                    "reason": "No IEC rules were retrieved for the given input.",
                    "suggestion": "Provide more detailed cable specifications.",
                    "source": "N/A"
                }
            ]
        }

    prompt = build_validation_prompt(user_input, iec_facts)
    response = call_llm(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "results": [
                {
                    "parameter": "N/A",
                    "status": "WARN",
                    "reason": "LLM returned an invalid response format.",
                    "suggestion": "Retry validation.",
                    "source": "N/A"
                }
            ]
        }
