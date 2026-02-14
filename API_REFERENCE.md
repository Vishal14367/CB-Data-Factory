# Codebasics Data Factory - API Reference

Complete API documentation for all phases (1-5).

## Base URL

```
http://127.0.0.1:8000
```

---

## Root Endpoint

### GET `/`

Health check and API overview.

**Response:**
```json
{
  "status": "healthy",
  "service": "Codebasics Data Factory - Complete E2E Pipeline",
  "version": "2.0.0",
  "brand": "Codebasics Data Factory",
  "phases": {
    "phase1": "Research & Problem Statement",
    "phase2": "Schema Generation & Validation",
    "phase3": "Preview Generation (10-30 rows)",
    "phase4": "Full Generation + Reports (PDF + Excel)",
    "phase5": "Download Package"
  }
}
```

---

## Session Status

### GET `/api/challenge/session/{session_id}`

Get comprehensive status across all phases.

**Response:**
```json
{
  "session_id": "uuid",
  "current_phase": "phase2",
  "created_at": "2024-02-07T10:30:00",
  "phase_status": {
    "phase1": {
      "completed": true,
      "has_research": true,
      "has_problem": true
    },
    "phase2": {
      "completed": false,
      "has_schema": true,
      "validation_score": 9.5
    },
    "phase3": {...},
    "phase4": {...},
    "phase5": {...}
  },
  "next_action": "POST /api/challenge/phase2/approve"
}
```

---

## Phase 1: Research & Problem Statement

### POST `/api/challenge/phase1/research`

Conduct domain-specific research.

**Request Body:**
```json
{
  "domain": "E-commerce",
  "function": "Sales Analytics",
  "problem_statement": "...",
  "skill_level": "Intermediate",
  "dataset_size": 10000,
  "data_structure": "Normalized",
  "primary_questions": "..."
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "status": "research_complete",
  "research": {
    "sources": [...],
    "domain_insights": [...],
    "identified_kpis": [...],
    "industry_challenges": [...]
  }
}
```

---

### POST `/api/challenge/phase1/generate-problem`

Generate problem statement with brand characters.

**Query Parameters:**
- `session_id`: Session UUID

**Request Body:**
```json
{
  "domain": "E-commerce",
  "function": "Sales Analytics",
  ...
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "status": "problem_generated",
  "problem_statement": {
    "title": "...",
    "company_name": "...",
    "statement": "...",
    "character_positions": {...},
    "analytical_questions": [...]
  }
}
```

---

### POST `/api/challenge/phase1/approve`

Approve problem statement.

**Query Parameters:**
- `session_id`: Session UUID

**Response:**
```json
{
  "session_id": "uuid",
  "status": "phase1_approved",
  "message": "Problem statement approved. Ready for Phase 2.",
  "next_phase": "phase2"
}
```

---

### GET `/api/challenge/phase1/status/{session_id}`

Get Phase 1 status.

**Response:**
```json
{
  "session_id": "uuid",
  "phase": "phase1",
  "status": "problem_generated",
  "problem_approved": false,
  "has_research": true,
  "has_problem": true
}
```

---

## Phase 2: Schema Generation & Validation

### POST `/api/challenge/phase2/generate-schema`

Generate database schema from problem statement.

**Query Parameters:**
- `session_id`: Session UUID

**Response:**
```json
{
  "session_id": "uuid",
  "phase": "phase2",
  "status": "pending_approval",
  "schema": {
    "tables": [...],
    "relationships": [...],
    "business_rules": [...],
    "kpis": [...]
  },
  "validation": {
    "can_answer_all": true,
    "validation_score": 9.5,
    "answerable_questions": [0, 1, 2, 3, 4],
    "missing_capabilities": [],
    "recommendations": ["Schema looks comprehensive"]
  }
}
```

---

### POST `/api/challenge/phase2/approve`

Approve generated schema.

**Query Parameters:**
- `session_id`: Session UUID

**Response:**
```json
{
  "session_id": "uuid",
  "status": "phase2_approved",
  "message": "Schema approved. Ready for Phase 3.",
  "next_phase": "phase3"
}
```

---

### POST `/api/challenge/phase2/regenerate`

Regenerate schema with improvements.

**Query Parameters:**
- `session_id`: Session UUID

**Response:** Same as `generate-schema`

---

## Phase 3: Preview Generation

### POST `/api/challenge/phase3/generate-preview`

Generate preview data (10-30 rows per table).

**Query Parameters:**
- `session_id`: Session UUID

**Response:**
```json
{
  "session_id": "uuid",
  "phase": "phase3",
  "status": "pending_approval",
  "preview_data": [
    {
      "table_name": "customers",
      "sample_rows": [{...}, {...}],
      "row_count": 30,
      "column_count": 8
    }
  ],
  "validation": {
    "fk_integrity_passed": true,
    "orphan_records": {},
    "data_type_issues": [],
    "quality_score": 9.8
  }
}
```

---

### POST `/api/challenge/phase3/approve`

Approve preview data.

**Query Parameters:**
- `session_id`: Session UUID

**Response:**
```json
{
  "session_id": "uuid",
  "status": "phase3_approved",
  "message": "Preview approved. Ready for Phase 4.",
  "next_phase": "phase4"
}
```

---

## Phase 4: Full Generation with Reports

### POST `/api/challenge/phase4/generate-full`

Start full dataset generation (background task).

**Query Parameters:**
- `session_id`: Session UUID

**Request Body:**
```json
{
  "dataset_size": 10000
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "phase": "phase4",
  "status": "generating",
  "message": "Full generation started. Poll /api/challenge/phase4/status."
}
```

---

### GET `/api/challenge/phase4/status/{session_id}`

Poll Phase 4 generation progress.

**Response:**
```json
{
  "session_id": "uuid",
  "phase": "phase4",
  "status": "generating",
  "progress": {
    "stage": "quality_validation",
    "percent": 50,
    "message": "Running quality validation checks...",
    "elapsed": 45.2
  },
  "qa_results": null
}
```

**When Complete:**
```json
{
  "session_id": "uuid",
  "phase": "phase4",
  "status": "completed",
  "progress": {
    "stage": "completed",
    "percent": 100,
    "message": "Generation complete!",
    "elapsed": 87.5
  },
  "qa_results": {
    "overall_score": 8.7,
    "status": "Approved",
    "category_scores": {...},
    "checks": [...],
    "strengths": [...],
    "issues": [...]
  }
}
```

---

## Phase 5: Download Package

### GET `/api/challenge/phase5/prepare/{session_id}`

Prepare complete download package.

**Response:**
```json
{
  "session_id": "uuid",
  "phase": "phase5",
  "status": "ready",
  "package": {
    "csv_files": ["customers.csv", "orders.csv"],
    "pdf_report": "quality_report.pdf",
    "excel_report": "analytical_answers.xlsx",
    "data_dictionary": "data_dictionary.txt",
    "readme": "README.txt",
    "zip_path": "/path/to/package.zip"
  },
  "download_url": "/api/challenge/phase5/download/{session_id}"
}
```

---

### GET `/api/challenge/phase5/download/{session_id}`

Download complete package as ZIP.

**Response:** Binary ZIP file

**Headers:**
```
Content-Type: application/zip
Content-Disposition: attachment; filename="codebasics_data_challenge_{session_id}.zip"
```

---

## Legacy Endpoints (Backward Compatibility)

### POST `/api/challenge/create`

Old single-phase endpoint (still functional).

**Request Body:**
```json
{
  "domain": "...",
  "function": "...",
  "problem_statement": "...",
  "skill_level": "Intermediate",
  "dataset_size": 10000
}
```

---

### GET `/api/challenge/status/{session_id}`

Old progress endpoint.

---

### GET `/api/challenge/result/{session_id}`

Old result endpoint.

---

### GET `/api/report/download/{session_id}`

Download PDF report only.

---

### GET `/api/download/{session_id}`

Download datasets only (no full package).

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Schema must be approved first"
}
```

### 404 Not Found
```json
{
  "detail": "Session not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Schema generation failed: ..."
}
```

---

## Data Models

### ChallengeInput
```python
{
  "domain": str,              # Min 3, max 100 chars
  "function": str,            # Min 3, max 100 chars
  "problem_statement": str,   # Min 100, max 2000 chars
  "skill_level": "Beginner" | "Intermediate" | "Advanced",
  "dataset_size": 1000 | 5000 | 10000 | 25000 | 50000 | 100000,
  "data_structure": "Normalized" | "Denormalized",
  "primary_questions": str    # Optional
}
```

### GenerationSizeInput
```python
{
  "dataset_size": int  # 1000-100000
}
```

---

## Rate Limits

Currently no rate limits implemented.

**Recommended limits for production:**
- 100 requests per hour per IP
- 10 concurrent generations per user
- Max file size: 500MB

---

## Webhooks (Future)

Not yet implemented. Future support for:
- Phase completion notifications
- Error notifications
- Download ready notifications

---

## SDK Support (Future)

Python SDK planned:
```python
from codebasics_df import DataFactory

df = DataFactory(api_key="...")
session = df.create_challenge(domain="E-commerce", ...)
session.wait_for_completion()
session.download()
```

---

## Change Log

### v2.0.0 (Current)
- Added Phase 2: Schema Generation
- Added Phase 3: Preview Generation
- Added Phase 4: Full Generation with Reports
- Added Phase 5: Download Package
- Added comprehensive session status endpoint

### v1.0.0
- Initial release with Phase 1 only
- Basic PDF report generation
- Single-phase workflow
