
# IEC Cable Specification Validation System

**(KG + FAISS + Local LLM + FastAPI)**

##  Overview

This project implements an **IEC cable specification validation system** that validates **free-text cable specifications** against **IEC 60502-1** rules.

Unlike a basic RAG system, this solution uses a **Knowledge Graph–driven retrieval and validation pipeline** to ensure:

* No hallucination
* Evidence-based decisions
* Conservative compliance behavior (PASS / FAIL / WARN)

The system is designed to behave like a **real compliance engine**, not a Q&A chatbot.

---

##  Key Design Principles

* **No hardcoded IEC rules**
* **No guessing when data is ambiguous**
* **Validation uses only extracted IEC facts**
* **Local LLM (Ollama) — no cloud dependency**
* **Explainable results with source traceability**

---

##  Architecture

```
User Input (Free Text)
        ↓
Entity & Parameter Understanding
        ↓
FAISS Retrieval (KG-based facts only)
        ↓
Validation Engine (LLM, evidence-locked)
        ↓
PASS / FAIL / WARN + IEC Source
```

### Why not basic RAG?

Basic RAG retrieves **semantically similar text**, which can lead to:

* Wrong IEC table selection
* Incorrect voltage-class matching
* False PASS / FAIL results

This system avoids that by:

* Extracting **structured engineering facts**
* Retrieving **only relevant IEC constraints**
* Returning **WARN** when rules are ambiguous

---

##  Project Structure

```
cable_validation/
│
├── kg_build/                 # Phase 1: Knowledge Graph creation
│   ├── run_builder.py
│   ├── kg_builder.py
│   ├── text_loader.py
│   └── prompt.py
│
├── retriever/                # Phase 2: FAISS retrieval
│   ├── pipeline.py
│   └── faiss_loader.py
│
├── validation/               # Phase 3: Validation logic
│   ├── run_validator.py
│   └── prompt.py
│
├── data/
│   └── IEC_60502_searchable.pdf
│
├── kg.json                   # Extracted IEC facts
├── kg.index                  # FAISS index
├── kg_meta.json              # KG metadata
│
├── app.py                    # FastAPI application
├── requirements.txt
└── README.md
```

---

##  System Phases

### **Phase 1 — Knowledge Graph Creation**

* IEC PDF is converted to searchable format
* Pages are processed using an LLM
* Only **numeric engineering facts, formulas, and constraints** are extracted
* Output: `kg.json`

> Many IEC pages are descriptive; empty extraction is expected and correct.

---

### **Phase 2 — FAISS Retrieval**

* KG facts are embedded using `sentence-transformers`
* FAISS index is built **once**
* At runtime:

  * Only user query is embedded
  * KG is NOT re-embedded or rebuilt

This ensures **low latency and deterministic retrieval**.

---

### **Phase 3 — Validation**

* LLM validates user input **only against retrieved IEC facts**
* Strict comparison rules:

  * Minimum / Maximum
  * Nominal
  * Formula matching
* If rule applicability is unclear → **WARN**
* No hallucinated rules are allowed

---

## Validation Status Meaning

| Status | Meaning                                           |
| ------ | ------------------------------------------------- |
| PASS   | Explicit IEC rule satisfied                       |
| FAIL   | Explicit IEC rule violated                        |
| WARN   | Rule is ambiguous, descriptive, or not applicable |

Returning **WARN is intentional and correct** for compliance systems.

---

## Running the Project

###  Install Dependencies

```bash
pip install -r requirements.txt
```

###  Start Ollama (Local LLM)

Ensure Ollama is running:

```bash
ollama run qwen2.5:3b
```

> Ollama is a system service and not included in `requirements.txt`.

---

###  Build Knowledge Graph (One Time)

```bash
python kg_build/run_builder.py
```

---

###  Build FAISS Index (One Time)

```bash
python build_faiss_index.py
```

---

### Run API

```bash
uvicorn app:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---
### Post Man endpoint

POST     http://127.0.0.1:8000/design/validate

##  Example API Request

```json
{
  "text": "XLPE cable rated for 1 kV"
}
```

### Example Response

```json
{
  "overall_status": "PASS",
  "results": [
    {
      "parameter": "rated voltage",
      "status": "PASS",
      "reason": "The rated voltage of 1 kV is explicitly defined in IEC 60502-1.",
      "source": "Page 10"
    }
  ]
}
```

---

##  Known Limitations (Honest & Acceptable)

* Some IEC constraints are table-heavy and may not be fully extractable via OCR
* In such cases, the system returns **WARN instead of guessing**
* This behavior is **intentional and standards-compliant**

---

##  Why This System Is Reliable

* No hardcoded thresholds
* No cloud APIs
* No rule hallucination
* Evidence-backed validation only
* Conservative decision-making

---

## Conclusion

This project demonstrates a  approach to standards validation using:

* Knowledge Graphs
* Vector retrieval
* Local LLMs
* Deterministic validation logic


---
