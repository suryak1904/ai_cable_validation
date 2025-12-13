import json
def build_validation_prompt(user_input: str, iec_facts: list):
    return f"""
You are validating cable specifications strictly against IEC rules.

STRICT RULES (MANDATORY):
- Use ONLY the IEC facts provided.
- Do NOT invent limits, tolerances, or assumptions.
- If no IEC fact clearly applies, return WARN.
- If IEC constraint is:
    - maximum → value must be ≤ limit
    - minimum → value must be ≥ limit
    - nominal → deviation is WARN unless exact match is required
- Always cite the IEC source exactly as provided.

User cable specification:
{user_input}

IEC facts (knowledge graph nodes):
{json.dumps(iec_facts, indent=2)}

OUTPUT FORMAT (JSON ONLY):
{{
  "results": [
    {{
      "parameter": "<validated parameter>",
      "status": "PASS | FAIL | WARN",
      "reason": "<why this status was chosen>",
      "suggestion": "<how to fix if FAIL or WARN>",
      "source": "<IEC page / clause>"
    }}
  ]
}}
"""
