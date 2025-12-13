import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    device_map="auto",
    dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    temperature=0.0,
    max_new_tokens=500,
    do_sample=False
)
def call_qwen(prompt: str) -> str:
    return generator(prompt)[0]["generated_text"]
