from fastapi import FastAPI
from pydantic import BaseModel
from retriever.pipeline import retrieve_context
from validation.run_validator import validate
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="IEC Cable Design Validator"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],
)
class ValidationRequest(BaseModel):
    text: str

@app.post("/design/validate")
def validate_cable(req: ValidationRequest):
    user_input = req.text
    iec_facts = retrieve_context(user_input)
    result = validate(user_input, iec_facts)
    return result
