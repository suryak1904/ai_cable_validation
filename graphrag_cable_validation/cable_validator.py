from fastapi import FastAPI
from pydantic import BaseModel
from retriever.pipeline import retrieve_context
from validation.run_validator import validate

app = FastAPI(
    title="IEC Cable Validation API",
)

class ValidationRequest(BaseModel):
    text: str

@app.post("/design/validate")
def validate_cable(req: ValidationRequest):
    user_input = req.text
    iec_facts = retrieve_context(user_input)
    result = validate(user_input, iec_facts)
    return result
