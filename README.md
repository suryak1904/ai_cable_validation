
# IEC Cable Validation System (RAG & GraphRAG)

## Overview

This project implements an **AI-assisted cable validation system** based on **IEC standards**, designed as part of an assessment to demonstrate:

* Free-text cable specification understanding
* Retrieval-augmented validation using IEC rules
* Comparison of **Normal RAG** and **GraphRAG** approaches
* End-to-end system integration (UI → Backend → AI engine)

The system validates user-provided cable specifications and returns **PASS / FAIL / WARN** decisions along with explanations and IEC rule references.

---

## System Architecture

```
Next.js (Frontend UI)
        ↓
NestJS (Gateway / Proxy)
        ↓
FastAPI (Validation Engine: RAG or GraphRAG)
```

### Key Design Choices

* **One frontend UI** supports multiple validation engines
* **Only one backend engine runs at a time** (RAG or GraphRAG)
* Frontend dynamically renders backend JSON responses
* NestJS acts as a lightweight proxy without enforcing schema normalization

---

## Why This Design? (Justification)

### 1. Separation of Concerns

* **Next.js**: User interface only (input, loading state, result display)
* **NestJS**: Simple API gateway to forward requests
* **FastAPI**: Core validation logic using IEC data

This keeps each layer focused and easy to reason about.

---

### 2. Dynamic Rendering for Assessment

Since this is an **assessment**, the frontend is intentionally designed to:

* Dynamically render backend responses
* Support both **Normal RAG** and **GraphRAG** outputs
* Avoid rigid schema enforcement

This allows easy comparison of different AI validation strategies without rewriting UI logic.

---
## Tech Stack

### Frontend

* Next.js (App Router)
* React
* Fetch API

### Backend

* NestJS (Node.js)
* Axios

### AI / Validation

* FastAPI (Python)
* FAISS
* Sentence Transformers
* Local LLM via **Ollama**

---

## How to Run the Project

### Prerequisites

* Node.js (v18+)
* Python (3.10+ recommended)
* Ollama installed and running
* Git

---

## Step 1: Start the FastAPI Validation Engine

Run **either RAG or GraphRAG backend** (not both).

Refer to the respective folder README for detailed explanations.

FastAPI will be available at:

```
http://localhost:8000/design/validate
```

---

## Step 2: Start NestJS Gateway

```bash
cd backend-nestjs
npm install
npm run start
```

NestJS will run on:

```
http://localhost:3001
```

This service forwards requests to FastAPI and returns responses as-is.

---

## Step 3: Start Next.js Frontend

```bash
cd frontend-nextjs
npm install
npm run dev
```

Open in browser:

```
http://localhost:3000
```

---
Switching Between RAG and GraphRAG

To switch engines:

Stop the currently running FastAPI backend

Start the other one on the same port (8000)

No frontend or NestJS changes required

---
