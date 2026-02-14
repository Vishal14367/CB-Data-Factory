# Codebasics Data Factory - Complete Phase Implementation Guide

## Overview

This document describes the complete implementation of Phases 2-5 for the CB Data Factory backend.

## Architecture

### Phase Flow
```
Phase 1: Research & Problem Statement
    ↓
Phase 2: Schema Generation & Validation
    ↓
Phase 3: Preview Generation (10-30 rows)
    ↓
Phase 4: Full Generation + Reports
    ↓
Phase 5: Download Package
```

## Implementation Details

### Phase 2: Schema Generation & Validation

**Purpose**: Generate database schema from approved problem statement and validate it can answer all analytical questions.

**Endpoints**:
- `POST /api/challenge/phase2/generate-schema` - Generate schema
- `POST /api/challenge/phase2/approve` - Approve schema
- `POST /api/challenge/phase2/regenerate` - Regenerate if needed

**Process**:
1. Takes approved problem statement from Phase 1
2. Uses SchemaGenerator to create database schema
3. Validates schema against analytical questions
4. Returns validation score (0-10)
5. User can approve or request regeneration

**Validation Checks**:
- ✓ Required tables exist for analysis
- ✓ Date columns present for temporal analysis
- ✓ Numeric columns for aggregation
- ✓ Categorical columns for segmentation
- ✓ Relationships support joins

**Response Model**:
```python
{
    "session_id": "uuid",
    "phase": "phase2",
    "status": "pending_approval|approved|regenerate",
    "schema": {...},
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

### Phase 3: Preview Generation

**Purpose**: Generate small preview dataset (10-30 rows) to verify schema works before full generation.

**Endpoints**:
- `POST /api/challenge/phase3/generate-preview` - Generate preview
- `POST /api/challenge/phase3/approve` - Approve preview

**Process**:
1. Takes approved schema from Phase 2
2. Generates 30 rows per table using DatasetGenerator
3. Validates foreign key integrity
4. Returns sample data (first 10 rows) for UI display
5. User can approve or request regeneration

**Validation Checks**:
- ✓ Foreign key integrity (no orphan records)
- ✓ Data types match schema
- ✓ Primary keys are unique
- ✓ Sample data looks realistic

**Response Model**:
```python
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

### Phase 4: Full Generation with Reports

**Purpose**: Generate full dataset and create comprehensive reports (PDF + Excel).

**Endpoints**:
- `POST /api/challenge/phase4/generate-full` - Start full generation
- `GET /api/challenge/phase4/status/{session_id}` - Poll progress

**Process** (Background Task):
1. Generate full dataset (user-specified size: 1K-100K rows)
2. Run complete quality validation (8 categories)
3. Generate PDF quality report with 12 visuals
4. Generate Excel report with analytical answers
5. Save all artifacts to session directory

**Input**:
```python
{
    "dataset_size": 10000  # 1000-100000
}
```

**Progress Stages**:
- `data_generation` (20%) - Generating rows
- `quality_validation` (50%) - Running 8 validation categories
- `pdf_generation` (70%) - Creating PDF with visuals
- `excel_generation` (85%) - Creating Excel with answers
- `completed` (100%) - All done

**Generated Files**:
1. **CSV files** - All table data
2. **quality_report.pdf** - Comprehensive quality validation
3. **analytical_answers.xlsx** - Answers to questions with charts
4. **qa_results.json** - Raw validation data
5. **schema.json** - Schema definition

**Excel Report Structure**:
- **Sheet 1**: Executive Summary
- **Sheet 2-N**: One sheet per analytical question with:
  - Question text
  - Sample answer/analysis
  - Supporting data table
  - Visualization (chart)
- **Sheet N+1**: Data Dictionary
- **Sheet N+2**: Quality Metrics
- **Sheet N+3**: Raw Data Samples

---

### Phase 5: Download Package

**Purpose**: Create comprehensive ZIP package with all deliverables.

**Endpoints**:
- `GET /api/challenge/phase5/prepare/{session_id}` - Prepare package
- `GET /api/challenge/phase5/download/{session_id}` - Download ZIP

**Process**:
1. Creates package directory
2. Copies all CSV files
3. Copies PDF and Excel reports
4. Generates data_dictionary.txt
5. Generates README.txt
6. Creates ZIP file

**Package Contents**:
```
codebasics_data_challenge_{session_id}.zip
├── table1.csv
├── table2.csv
├── table3.csv
├── quality_report.pdf
├── analytical_answers.xlsx
├── data_dictionary.txt
└── README.txt
```

**README.txt includes**:
- Challenge title and metadata
- Package contents description
- Analytical questions list
- How to use guide
- Recommended tools
- Support information

---

## Complete E2E Workflow

### Example Flow

```python
# PHASE 1: Research & Problem
POST /api/challenge/phase1/research
{
    "domain": "E-commerce",
    "function": "Sales Analytics",
    "problem_statement": "...",
    "skill_level": "Intermediate",
    "dataset_size": 10000
}
# Returns: session_id, research results

POST /api/challenge/phase1/generate-problem
{
    "session_id": "...",
    "input_data": {...}
}
# Returns: problem statement with characters and questions

POST /api/challenge/phase1/approve
{
    "session_id": "..."
}
# Returns: phase1_approved

# PHASE 2: Schema
POST /api/challenge/phase2/generate-schema
{
    "session_id": "..."
}
# Returns: schema with validation score

POST /api/challenge/phase2/approve
{
    "session_id": "..."
}
# Returns: phase2_approved

# PHASE 3: Preview
POST /api/challenge/phase3/generate-preview
{
    "session_id": "..."
}
# Returns: preview data (10-30 rows)

POST /api/challenge/phase3/approve
{
    "session_id": "..."
}
# Returns: phase3_approved

# PHASE 4: Full Generation
POST /api/challenge/phase4/generate-full
{
    "session_id": "...",
    "dataset_size": 10000
}
# Returns: generation started

# Poll for progress
GET /api/challenge/phase4/status/{session_id}
# Returns: progress updates

# PHASE 5: Download
GET /api/challenge/phase5/prepare/{session_id}
# Returns: package info

GET /api/challenge/phase5/download/{session_id}
# Downloads: ZIP file
```

---

## Session Management

### Session State Tracking

Each session maintains state across all phases:

```python
{
    "session_id": "uuid",
    "created_at": "datetime",
    "phase": "phase1|phase2|phase3|phase4|phase5",

    # Phase 1 data
    "input": {...},
    "research": {...},
    "problem_statement": {...},
    "problem_approved": bool,

    # Phase 2 data
    "schema": {...},
    "schema_validation": {...},
    "schema_approved": bool,

    # Phase 3 data
    "preview_data": [...],
    "preview_validation": {...},
    "preview_approved": bool,

    # Phase 4 data
    "generation_size": int,
    "phase4_status": "generating|completed|failed",
    "progress": {...},
    "qa_results": {...},
    "pdf_report_path": "...",
    "excel_report_path": "...",

    # Phase 5 data
    "download_package": {...}
}
```

### Comprehensive Status Endpoint

```
GET /api/challenge/session/{session_id}
```

Returns complete status across all phases with next recommended action.

---

## Quality Validation (Phase 4)

### 8 Validation Categories

1. **Structural Integrity** (25% weight)
   - Primary key uniqueness
   - Foreign key validity
   - No orphan records
   - Column count matches skill level

2. **Business Logic** (25% weight)
   - Business rules applied
   - Calculated fields correct
   - Status transitions valid

3. **Realism & Distribution** (20% weight)
   - Natural distributions (not uniform)
   - Seasonal variation
   - Appropriate outliers (5-10%)

4. **Learning Alignment** (20% weight)
   - Questions answerable
   - Appropriate complexity
   - Educational value

5. **Documentation & Schema** (10% weight)
   - Clear descriptions
   - Proper naming
   - Complete metadata

### Quality Thresholds

- **Approved**: Overall score ≥ 8.0
- **Regenerate**: 6.0 ≤ Score < 8.0
- **Rejected**: Score < 6.0

---

## Error Handling

### Phase 2 Errors
- Schema generation fails → Retry with different prompt
- Validation score < 6.0 → Auto-regenerate
- Missing required columns → Recommendations provided

### Phase 3 Errors
- FK integrity issues → Auto-regenerate with fixes
- Data type mismatches → Schema adjustment
- Quality score < 7.0 → Regenerate

### Phase 4 Errors
- Generation timeout → Reduce dataset size
- Quality validation fails → Up to 3 retries (uses best result)
- Report generation fails → Partial completion allowed

### Phase 5 Errors
- Missing files → Error with details
- ZIP creation fails → Retry
- Large file size → Compression optimization

---

## File Structure

```
backend/
├── src/
│   ├── main.py                 # Complete API with all phases
│   ├── models.py               # All phase models
│   ├── config.py               # Configuration
│   ├── schema_generator.py     # Phase 2
│   ├── dataset_generator.py    # Phase 3 & 4
│   ├── quality_validator.py    # Phase 4
│   ├── pdf_generator.py        # Phase 4
│   ├── excel_generator.py      # Phase 4
│   └── problem_generator.py    # Phase 1
├── output/
│   └── {session_id}/
│       ├── datasets/
│       │   ├── table1.csv
│       │   └── table2.csv
│       ├── quality_report.pdf
│       ├── analytical_answers.xlsx
│       ├── qa_results.json
│       ├── schema.json
│       └── package/
│           └── ... (ZIP contents)
```

---

## API Documentation

Complete API is self-documented at:
```
GET /
```

Returns all endpoints organized by phase.

---

## Testing

### Manual Testing Flow

1. Start server: `python main.py`
2. Test Phase 1: Research + Problem
3. Test Phase 2: Schema generation
4. Test Phase 3: Preview
5. Test Phase 4: Full generation (watch progress)
6. Test Phase 5: Download package
7. Verify all files in ZIP

### Automated Testing

Use `demo_complete_workflow.py` to test entire E2E flow.

---

## Performance

### Typical Execution Times

- Phase 1: 10-30 seconds (AI research + problem)
- Phase 2: 5-15 seconds (AI schema generation)
- Phase 3: 2-5 seconds (30 rows generation)
- Phase 4: 30-120 seconds (depends on size)
  - 1K rows: ~30 sec
  - 10K rows: ~60 sec
  - 100K rows: ~120 sec
- Phase 5: 5-10 seconds (packaging)

**Total E2E**: ~2-5 minutes for typical workflow

---

## Future Enhancements

1. **Database persistence** - Replace in-memory sessions
2. **Authentication** - User accounts and sessions
3. **Async improvements** - Better background task handling
4. **Caching** - Cache schema/preview for regeneration
5. **Analytics** - Track usage and popular domains
6. **Export formats** - Support Parquet, JSON, SQL dumps
7. **Cloud storage** - S3/Azure blob for large files
8. **WebSocket** - Real-time progress updates

---

## Conclusion

This complete implementation provides a robust, production-ready E2E workflow for generating educational datasets with comprehensive quality validation and reporting. All phases are integrated and ready for frontend integration.
