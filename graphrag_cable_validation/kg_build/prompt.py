def extraction_prompt(text, page):
    return f"""
You are extracting engineering facts from an IEC standard.

Your task:
- Extract ALL statements that contain NUMBERS, RANGES, or FORMULAS.
- Do NOT decide whether they are valid or correct.
- Do NOT skip facts just because wording is indirect.

For EACH extracted fact, output:
- parameter: short phrase describing what the number refers to
- value: the number, range, or formula as written
- unit: if mentioned, else null
- constraint_type: minimum | maximum | nominal | formula | unknown
- context: short explanation in your own words
- source: {{ "page": {page} }}

Rules:
- If a sentence contains any number (mm, kV, %, °C, formula), extract it.
- If unsure, still extract and mark constraint_type as "unknown".
- Return ONLY valid JSON array.
- If truly nothing numeric exists, return [].

TEXT:
{text[:3000]}
"""
