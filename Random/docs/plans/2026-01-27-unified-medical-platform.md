# Unified Medical Platform Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a "Breathable" AI Medical Companion that ingests medical data (OCR), understands it (RAG + Graph), proactively guards health (Reminders), and optimizes lifestyle (Health Index + Pharma).

**Architecture:**
- **Backend:** FastAPI (Python) serving REST & WebSockets.
- **AI Brain:** "Triple-Store" Memory:
    1.  **SQL (PostgreSQL):** Structured vitals, user profiles, schedules.
    2.  **Vector (ChromaDB):** Semantic understanding of reports/notes.
    3.  **Graph (NetworkX/Neo4j):** Medical relationships (Symptom -> Disease -> Test).
- **Frontend:** Next.js (TypeScript) with a "Calm/Breathable" UI (Tailwind + Framer Motion).
- **Async Workers:** Celery + Redis for background "Health Scans" and Reminders.

**Tech Stack:** Python 3.11, FastAPI, LangChain, PostgreSQL, ChromaDB, Next.js 14, TypeScript, Tailwind, Shadcn UI.

---

## Phase 0: The "Brain" & Skeleton (Infrastructure)

### Task 1: Project Initialization & Docker Setup
**Goal:** detailed setup of the mono-repo structure with Docker for DBs.
**Files:**
- Create: `docker-compose.yml` (Postgres, Redis, Chroma)
- Create: `backend/pyproject.toml`
- Create: `frontend/package.json`

**Step 1: Create Monorepo Structure**
```bash
mkdir -p backend/app frontend
touch backend/pyproject.toml
```

**Step 2: Define Docker Infrastructure**
Create `docker-compose.yml` with:
- PostgreSQL (User/Medical Data)
- Redis (Task Queue)
- ChromaDB (Vector Store)

**Step 3: Initialize FastAPI Backend**
Create `backend/app/main.py` with a health check endpoint.

**Step 4: Initialize Next.js Frontend**
Initialize standard Next.js app in `frontend/`.

**Step 5: Verification**
Run `docker-compose up -d` and verify all containers are healthy. curl the backend health check.

### Task 2: Database Schema (The "Triple Store" Foundation)
**Goal:** Set up SQLAlchemy models for the structured data.
**Files:**
- Create: `backend/app/core/db.py`
- Create: `backend/app/models/user.py` (User, MedicalProfile)
- Create: `backend/app/models/medical.py` (VitalSign, LabResult, Medication)

**Step 1: Define User & Profile Models**
`User` (auth info), `MedicalProfile` (age, gender, blood_type, genetic_markers).

**Step 2: Define Medical Data Models**
`MedicalRecord` (metadata for a file), `ExtractedMetric` (key-value pairs like "Hemoglobin": 13.5).

**Step 3: Run Migrations**
Use Alembic to initialize the DB.

---

## Phase 1: The "Senses" (Ingestion & Interpretation)

### Task 3: File Upload & OCR Pipeline
**Goal:** Allow uploading a PDF/Image and getting raw text back.
**Files:**
- Create: `backend/app/services/ocr.py`
- Create: `backend/app/api/endpoints/upload.py`

**Step 1: File Upload Endpoint**
FastAPI endpoint accepting `UploadFile`. Save to local `uploads/` directory (temp).

**Step 2: OCR Service Implementation**
Implement `extract_text_from_file(filepath)`. Use `pytesseract` or a Vision API mock for V1.
*Creative Edge Case:* If text confidence is low, flag for "User Review".

**Step 3: Connect Endpoint to Service**
Endpoint calls service, returns raw text.

### Task 4: The "Extraction Agent" (LLM Structuring)
**Goal:** Convert raw OCR text into structured `ExtractedMetric` rows.
**Files:**
- Create: `backend/app/services/extraction.py`
- Modify: `backend/app/models/medical.py`

**Step 1: Prompt Engineering**
Create a prompt that takes raw medical text and outputs JSON: `[{ "metric": "Hemoglobin", "value": 13.5, "unit": "g/dL", "flag": "normal" }]`.

**Step 2: LLM Service Integration**
Use LangChain to call an LLM (OpenAI/Anthropic/Local) with the prompt.

**Step 3: Persist to DB**
Parse JSON and save to `ExtractedMetric` table.

---

## Phase 2: The "Mind" (RAG & Knowledge Graph)

### Task 5: Vector Indexing (The Semantic Memory)
**Goal:** Chunk and embed medical reports so the chatbot can "read" them.
**Files:**
- Create: `backend/app/services/rag.py`

**Step 1: Chunking Strategy**
Implement a splitter that respects medical sections (e.g., split by "Hematology", "Lipid Profile").

**Step 2: Embedding & Storage**
Ingest text into ChromaDB.

### Task 6: The "Graph Builder" (Relationship Memory)
**Goal:** Map simple relationships. "User -> Has -> Diabetes".
**Files:**
- Create: `backend/app/services/graph.py`

**Step 1: Graph Node Definition**
Define nodes: `Patient`, `Condition`, `Biomarker`, `Medication`.

**Step 2: Extraction Logic**
When a report says "HbA1c is High", create edge: `Patient` --has_biomarker--> `HbA1c(High)` --indicates_risk--> `Diabetes`.

---

## Phase 3: The "Voice" (Chat Interface)

### Task 7: The "Breathable" Chat UI
**Goal:** A clean, non-cluttered chat interface.
**Files:**
- Create: `frontend/components/ChatInterface.tsx`
- Create: `frontend/app/dashboard/page.tsx`

**Step 1: UI Components**
Build a chat window that supports:
- Text messages
- "Reasoning" expandable sections (to show *why* the AI said something)
- "Artifacts" (rendering a table of results inside the chat).

**Step 2: WebSocket Connection**
Connect to FastAPI WebSocket endpoint.

### Task 8: The Medical Agent (RAG + Graph Retrieval)
**Goal:** The backend logic for answering questions.
**Files:**
- Create: `backend/app/api/endpoints/chat.py`
- Create: `backend/app/agents/medical_agent.py`

**Step 1: Retrieval Logic**
Query Vector DB for context + Query SQL for specific values ("What was my last glucose?").

**Step 2: Synthesis**
LLM generates answer using retrieved context + "Baymax" persona prompt.

---

## Phase 4: The "Guardian" (Reminders & Health Index)

### Task 9: The "Health Index" Algorithm
**Goal:** Calculate the 0-100 score.
**Files:**
- Create: `backend/app/services/health_score.py`

**Step 1: The Formula**
Implement `calculate_score(user_id)`:
- Base: 100
- Deduct for missing baseline data (encourage uploading).
- Deduct for out-of-range metrics.
- Add "Confidence Score" (Edge Case handling).

**Step 2: API Endpoint**
Expose `GET /health-score` for the frontend dashboard.

### Task 10: Dynamic Reminder Engine
**Goal:** Generate tasks based on rules.
**Files:**
- Create: `backend/app/services/reminders.py`

**Step 1: Rule Engine**
- Static: `if gender == 'F' and age > 40: suggest("Mammogram")`
- Dynamic: `if last_dental_visit > 6 months: suggest("Dentist")`

**Step 2: Scheduler**
Setup Celery beat to run this check daily.

---

## Phase 5: The "Utility" (Pharma & Extras)

### Task 11: Medication Tracker & Conflict Check
**Goal:** Manage current meds and check interactions.
**Files:**
- Create: `backend/app/api/endpoints/medications.py`

**Step 1: Add Medication Endpoint**
POST /medications (Name, Dosage).

**Step 2: Conflict Logic**
Mock interaction check: `if "Aspirin" in meds and "Warfarin" in meds: return WARNING`.

### Task 12: Pharma Price Comparison
**Goal:** "Cheap vs Expensive" logic.
**Files:**
- Create: `backend/app/services/pharma.py`

**Step 1: Generic Mapping**
Map "Panadol" -> "Paracetamol".

**Step 2: Price Mocking**
Return list of brands with mocked prices for the active ingredient.

---

## Phase 6: Edge Case Polish

### Task 13: "Privacy Mode" & Localization
**Goal:** UI features for privacy and language.
**Files:**
- Modify: `frontend/components/Dashboard.tsx`

**Step 1: Blur Toggle**
Add a state `isPrivate` that blurs numbers on the dashboard.

**Step 2: Language Context**
Pass `user_language` to the LLM prompt to support multi-lingual responses.
