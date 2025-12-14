from fastapi import FastAPI, HTTPException
from retriever import retrieve_rules
from validator import validate_with_llm
from pydantic import BaseModel
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
def validate_design(request: ValidationRequest):
    user_spec = request.text.strip()
    if not user_spec:
        raise HTTPException(
            status_code=400,
            detail="Input text cannot be empty"
        )
    rules = retrieve_rules(user_spec, k=5)
    if not rules:
        return {
            "status": "WARN",
            "reason": "No relevant IEC rules found for the given input.",
            "source": None
        }
    result = validate_with_llm(user_spec, rules)
    return result
