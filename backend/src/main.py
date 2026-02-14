"""
FastAPI application entry point.
"""
import sys
import os
from pathlib import Path

# Add the current directory to sys.path to resolve relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import logging
import time
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uuid
import json
from datetime import datetime
from typing import Dict
import pandas as pd

from models import (
    ChallengeInput, GenerationProgress, ChallengeResult,
    ResearchResult, ProblemStatement,
    Phase2Response, SchemaValidationResult, Schema,
    Phase3Response, PreviewData, PreviewValidationResult,
    Phase4Response, GenerationSizeInput,
    Phase5Response, DownloadPackage,
    ChatRequest
)
from config import HOST, PORT, OUTPUT_DIR, LOG_LEVEL, LOG_FORMAT, GROQ_API_KEY, AI_MODEL
from groq import Groq
from schema_generator import SchemaGenerator
from problem_generator import ProblemGenerator

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Codebasics Data Challenge Generator",
    description="Foundation Phase: Data Quality Engine + PDF Report",
    version="0.1.0"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage (will be replaced with proper storage later)
sessions = {}


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
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
        },
        "endpoints": {
            "phase1": [
                "POST /api/challenge/phase1/research",
                "POST /api/challenge/phase1/generate-problem",
                "POST /api/challenge/phase1/approve",
                "GET /api/challenge/phase1/status/{session_id}"
            ],
            "phase2": [
                "POST /api/challenge/phase2/generate-schema",
                "POST /api/challenge/phase2/approve",
                "POST /api/challenge/phase2/regenerate"
            ],
            "phase3": [
                "POST /api/challenge/phase3/generate-preview",
                "POST /api/challenge/phase3/approve"
            ],
            "phase4": [
                "POST /api/challenge/phase4/generate-full",
                "GET /api/challenge/phase4/status/{session_id}"
            ],
            "phase5": [
                "GET /api/challenge/phase5/prepare/{session_id}",
                "GET /api/challenge/phase5/download/{session_id}"
            ],
            "chat": [
                "POST /api/chat"
            ]
        }
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Context-aware chatbot to help user with the current phase.
    """
    session_id = request.session_id
    message = request.message
    phase = request.phase

    if session_id and session_id not in sessions:
        # Allow chat without session for general info, but context won't be as good
        pass
    
    context = ""
    if session_id in sessions:
        session = sessions[session_id]
        context = f"Session Info: Domain {session.get('input', {}).get('domain')}, Function {session.get('input', {}).get('function')}. "
        if session.get('problem_statement'):
            context += f"Current Problem: {session['problem_statement'].get('title')}. "
        context += f"User is currently in Phase: {phase}. "

    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"You are the Codebasics Data Factory Assistant. Help the user with their data challenge creation. Current Context: {context}"
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return {"response": response.choices[0].message.content}
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PHASE 1: RESEARCH-DRIVEN PROBLEM STATEMENT
# ============================================================================

@app.post("/api/challenge/phase1/research")
async def phase1_research(input_data: ChallengeInput):
    """
    Phase 1A: Conduct domain-specific research.

    Uses web search to find:
    - Recent industry trends
    - KPIs and metrics
    - Business challenges
    - Regulatory updates
    """
    session_id = str(uuid.uuid4())

    logger.info(f"Phase 1A: Starting research for {input_data.domain} - {input_data.function}")

    try:
        problem_gen = ProblemGenerator()
        research = problem_gen.conduct_research(input_data.domain, input_data.function)
        research.session_id = session_id

        # Store in session
        sessions[session_id] = {
            "input": input_data.model_dump(),
            "phase": "phase1",
            "research": research.model_dump(),
            "status": "research_complete",
            "created_at": datetime.now()
        }

        return {
            "session_id": session_id,
            "status": "research_complete",
            "research": research.model_dump(),
            "message": f"Research completed: {len(research.sources)} sources found"
        }

    except Exception as e:
        logger.error(f"Phase 1A research failed: {e}")
        return {
            "session_id": session_id,
            "status": "error",
            "error": str(e)
        }


@app.post("/api/challenge/phase1/generate-problem")
async def phase1_generate_problem(session_id: str, input_data: ChallengeInput):
    """
    Phase 1B: Generate research-backed problem statement with brand characters.

    Ensures:
    - All three brand characters appear (Peter Pandey, Tony Sharma, Bruce Hariyali)
    - Characters are positioned for UI highlighting
    - Analytical questions match skill level
    - Problem is grounded in research
    """
    logger.info(f"Phase 1B: Generating problem statement for session {session_id}")

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        problem_gen = ProblemGenerator()

        # Get research from session
        research_data = sessions[session_id].get("research")
        research = ResearchResult(**research_data)

        # Generate problem statement
        problem_statement = problem_gen.generate_problem_statement(
            session_id, input_data, research
        )

        # Store in session
        sessions[session_id]["problem_statement"] = problem_statement.model_dump()
        sessions[session_id]["status"] = "problem_generated"
        sessions[session_id]["problem_approved"] = False

        return {
            "session_id": session_id,
            "status": "problem_generated",
            "problem_statement": problem_statement.model_dump(),
            "message": "Problem statement generated with research backing"
        }

    except Exception as e:
        logger.error(f"Phase 1B generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/challenge/phase1/approve")
async def phase1_approve(session_id: str):
    """
    Phase 1C: User approves problem statement.

    Unlocks progression to Phase 2 (Schema Generation).
    """
    logger.info(f"Phase 1C: Approving problem statement for session {session_id}")

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    if "problem_statement" not in sessions[session_id]:
        raise HTTPException(status_code=400, detail="No problem statement found")

    try:
        sessions[session_id]["problem_approved"] = True
        sessions[session_id]["approval_timestamp"] = datetime.now().isoformat()

        return {
            "session_id": session_id,
            "status": "phase1_approved",
            "message": "Problem statement approved. Ready for Phase 2: Schema Generation.",
            "next_phase": "phase2"
        }

    except Exception as e:
        logger.error(f"Phase 1 approval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/challenge/phase1/status/{session_id}")
async def phase1_status(session_id: str):
    """Get current Phase 1 status."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]

    return {
        "session_id": session_id,
        "phase": "phase1",
        "status": session.get("status", "unknown"),
        "problem_approved": session.get("problem_approved", False),
        "has_research": "research" in session,
        "has_problem": "problem_statement" in session,
        "created_at": session.get("created_at")
    }


# ============================================================================
# PHASE 2: SCHEMA GENERATION & VALIDATION
# ============================================================================

@app.post("/api/challenge/phase2/generate-schema")
async def phase2_generate_schema(session_id: str):
    """
    Phase 2: Generate database schema from approved problem statement.

    Validates that schema can answer all analytical questions.
    Returns schema with validation score.
    """
    logger.info(f"Phase 2: Generating schema for session {session_id}")

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    if not sessions[session_id].get("problem_approved"):
        raise HTTPException(status_code=400, detail="Problem statement must be approved first")

    try:
        # Get input data and problem statement
        input_data = ChallengeInput(**sessions[session_id]["input"])
        problem_statement = ProblemStatement(**sessions[session_id]["problem_statement"])

        # Generate schema
        schema_gen = SchemaGenerator()
        schema = schema_gen.generate(input_data)

        # Validate schema can answer all questions
        validation = _validate_schema_against_questions(schema, problem_statement)

        # Store schema in session
        sessions[session_id]["schema"] = schema.model_dump()
        sessions[session_id]["schema_validation"] = validation.model_dump()
        sessions[session_id]["schema_approved"] = False
        sessions[session_id]["phase"] = "phase2"

        status = "pending_approval"
        if validation.validation_score < 6.0:
            status = "regenerate"

        return Phase2Response(
            session_id=session_id,
            phase="phase2",
            status=status,
            schema=schema,
            validation=validation,
            message=f"Schema generated with validation score: {validation.validation_score:.1f}/10"
        )

    except Exception as e:
        logger.error(f"Phase 2 schema generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/challenge/phase2/approve")
async def phase2_approve(session_id: str):
    """
    Phase 2: Approve generated schema.

    Unlocks progression to Phase 3 (Preview).
    """
    logger.info(f"Phase 2: Approving schema for session {session_id}")

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    if "schema" not in sessions[session_id]:
        raise HTTPException(status_code=400, detail="No schema found")

    try:
        sessions[session_id]["schema_approved"] = True
        sessions[session_id]["schema_approval_timestamp"] = datetime.now().isoformat()

        return {
            "session_id": session_id,
            "status": "phase2_approved",
            "message": "Schema approved. Ready for Phase 3: Preview Generation.",
            "next_phase": "phase3"
        }

    except Exception as e:
        logger.error(f"Phase 2 approval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/challenge/phase2/regenerate")
async def phase2_regenerate(session_id: str):
    """
    Phase 2: Regenerate schema with improvements.
    """
    logger.info(f"Phase 2: Regenerating schema for session {session_id}")

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    # Simply call generate again - it will create a new schema
    return await phase2_generate_schema(session_id)


# ============================================================================
# PHASE 3: PREVIEW GENERATION
# ============================================================================

@app.post("/api/challenge/phase3/generate-preview")
async def phase3_generate_preview(session_id: str):
    """
    Phase 3: Generate preview data (10-30 sample rows per table).

    Validates foreign key relationships and data types.
    Shows user a preview before full generation.
    """
    logger.info(f"Phase 3: Generating preview for session {session_id}")

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    if not sessions[session_id].get("schema_approved"):
        raise HTTPException(status_code=400, detail="Schema must be approved first")

    try:
        from dataset_generator import DatasetGenerator

        # Get schema
        schema = Schema(**sessions[session_id]["schema"])

        # Generate preview data (30 rows for preview)
        preview_size = 30
        data_gen = DatasetGenerator(seed=42)
        preview_dataframes = data_gen.generate(schema, preview_size)

        # Validate preview
        validation = _validate_preview(schema, preview_dataframes)

        # Convert to PreviewData format
        preview_data = []
        for table_name, df in preview_dataframes.items():
            # Convert first 10 rows to list of dicts
            sample_rows = df.head(10).fillna("NULL").to_dict('records')
            preview_data.append(PreviewData(
                table_name=table_name,
                sample_rows=sample_rows,
                row_count=len(df),
                column_count=len(df.columns)
            ))

        # Store preview in session
        sessions[session_id]["preview_data"] = [p.model_dump() for p in preview_data]
        sessions[session_id]["preview_validation"] = validation.model_dump()
        sessions[session_id]["preview_approved"] = False
        sessions[session_id]["phase"] = "phase3"

        status = "pending_approval"
        if validation.quality_score < 7.0:
            status = "regenerate"

        return Phase3Response(
            session_id=session_id,
            phase="phase3",
            status=status,
            preview_data=preview_data,
            validation=validation,
            message=f"Preview generated with quality score: {validation.quality_score:.1f}/10"
        )

    except Exception as e:
        logger.error(f"Phase 3 preview generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/challenge/phase3/approve")
async def phase3_approve(session_id: str):
    """
    Phase 3: Approve preview data.

    Unlocks progression to Phase 4 (Full Generation).
    """
    logger.info(f"Phase 3: Approving preview for session {session_id}")

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    if "preview_data" not in sessions[session_id]:
        raise HTTPException(status_code=400, detail="No preview data found")

    try:
        sessions[session_id]["preview_approved"] = True
        sessions[session_id]["preview_approval_timestamp"] = datetime.now().isoformat()

        return {
            "session_id": session_id,
            "status": "phase3_approved",
            "message": "Preview approved. Ready for Phase 4: Full Dataset Generation.",
            "next_phase": "phase4"
        }

    except Exception as e:
        logger.error(f"Phase 3 approval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PHASE 4: FULL GENERATION WITH REPORTS
# ============================================================================

@app.post("/api/challenge/phase4/generate-full")
async def phase4_generate_full(session_id: str, size_input: GenerationSizeInput, background_tasks: BackgroundTasks):
    """
    Phase 4: Generate full dataset with specified size.

    Runs:
    1. Full data generation
    2. Complete quality validation
    3. PDF report generation
    4. Excel report with answers to analytical questions

    This runs in the background. Poll status endpoint for progress.
    """
    logger.info(f"Phase 4: Starting full generation for session {session_id}")

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    if not sessions[session_id].get("preview_approved"):
        raise HTTPException(status_code=400, detail="Preview must be approved first")

    try:
        # Update session
        sessions[session_id]["phase"] = "phase4"
        sessions[session_id]["generation_size"] = size_input.dataset_size
        sessions[session_id]["phase4_status"] = "generating"

        # Create session directory
        session_dir = OUTPUT_DIR / session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        # Launch background generation
        background_tasks.add_task(_run_phase4_generation, session_id, size_input.dataset_size, session_dir)

        return Phase4Response(
            session_id=session_id,
            phase="phase4",
            status="generating",
            message=f"Full generation started for {size_input.dataset_size:,} rows. Poll /api/challenge/phase4/status for progress."
        )

    except Exception as e:
        logger.error(f"Phase 4 generation start failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/challenge/phase4/status/{session_id}")
async def phase4_status(session_id: str):
    """Get Phase 4 generation status and progress."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]

    return {
        "session_id": session_id,
        "phase": "phase4",
        "status": session.get("phase4_status", "unknown"),
        "progress": session.get("progress", {}),
        "qa_results": session.get("qa_results"),
        "error": session.get("error")
    }


# ============================================================================
# PHASE 5: DOWNLOAD PACKAGE
# ============================================================================

@app.get("/api/challenge/phase5/prepare/{session_id}")
async def phase5_prepare_download(session_id: str):
    """
    Phase 5: Prepare complete download package.

    Creates ZIP containing:
    - All CSV files
    - PDF quality report
    - Excel answers report
    - Data dictionary
    - README file
    """
    logger.info(f"Phase 5: Preparing download package for session {session_id}")

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    if sessions[session_id].get("phase4_status") != "completed":
        raise HTTPException(status_code=400, detail="Phase 4 generation must be completed first")

    try:
        session_dir = OUTPUT_DIR / session_id

        # Create package
        package = _create_download_package(session_id, session_dir)

        # Store package info
        sessions[session_id]["download_package"] = package.model_dump()
        sessions[session_id]["phase"] = "phase5"

        return Phase5Response(
            session_id=session_id,
            phase="phase5",
            status="ready",
            package=package,
            download_url=f"/api/challenge/phase5/download/{session_id}",
            message="Download package ready"
        )

    except Exception as e:
        logger.error(f"Phase 5 package preparation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/challenge/phase5/download/{session_id}")
async def phase5_download(session_id: str):
    """Download the complete package as ZIP."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    if "download_package" not in sessions[session_id]:
        raise HTTPException(status_code=400, detail="Download package not prepared. Call /phase5/prepare first")

    package = DownloadPackage(**sessions[session_id]["download_package"])

    if not Path(package.zip_path).exists():
        raise HTTPException(status_code=404, detail="Download package not found")

    return FileResponse(
        path=package.zip_path,
        media_type="application/zip",
        filename=f"codebasics_data_challenge_{session_id}.zip"
    )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _validate_schema_against_questions(schema: Schema, problem: ProblemStatement) -> SchemaValidationResult:
    """
    Validate that the schema can answer all analytical questions.

    Checks:
    - Required tables exist
    - Required columns exist
    - Relationships support joins
    - Metrics can be calculated
    """
    answerable = []
    missing = []
    recommendations = []

    # Get all column names by table
    all_columns = {}
    for table in schema.tables:
        all_columns[table.name.lower()] = {c.name.lower() for c in table.columns}

    # Check each question
    for i, question in enumerate(problem.analytical_questions):
        q_lower = question.lower()
        can_answer = True

        # Basic heuristics for question answerability
        # Check for temporal analysis
        if any(word in q_lower for word in ['trend', 'over time', 'monthly', 'yearly', 'seasonal']):
            has_date = any('date' in col for cols in all_columns.values() for col in cols)
            if not has_date:
                can_answer = False
                missing.append(f"Q{i+1}: Missing date/time column for temporal analysis")

        # Check for aggregation capability
        if any(word in q_lower for word in ['total', 'average', 'sum', 'count']):
            has_numeric = any(
                any(c.datatype in ['integer', 'float'] for c in table.columns)
                for table in schema.tables
            )
            if not has_numeric:
                can_answer = False
                missing.append(f"Q{i+1}: Missing numeric columns for aggregation")

        # Check for categorical analysis
        if any(word in q_lower for word in ['category', 'type', 'segment', 'region']):
            has_category = any(
                any(c.datatype in ['category', 'string'] for c in table.columns)
                for table in schema.tables
            )
            if not has_category:
                can_answer = False
                missing.append(f"Q{i+1}: Missing categorical columns")

        if can_answer:
            answerable.append(i)

    # Calculate validation score
    answerable_pct = len(answerable) / len(problem.analytical_questions) if problem.analytical_questions else 0
    validation_score = answerable_pct * 10

    # Generate recommendations
    if validation_score < 10:
        recommendations.append("Consider adding date columns for temporal analysis")
        recommendations.append("Ensure numeric metrics for KPI calculation")
        recommendations.append("Add categorical columns for segmentation analysis")

    return SchemaValidationResult(
        can_answer_all=len(answerable) == len(problem.analytical_questions),
        validation_score=round(validation_score, 1),
        answerable_questions=answerable,
        missing_capabilities=missing,
        recommendations=recommendations if validation_score < 10 else ["Schema looks comprehensive"]
    )


def _validate_preview(schema: Schema, dataframes: Dict[str, pd.DataFrame]) -> PreviewValidationResult:
    """
    Validate preview data for foreign key integrity and data types.
    """
    orphan_records = {}
    data_type_issues = []
    fk_integrity_passed = True

    # Check FK integrity
    for fk in schema.relationships:
        if fk.child_table in dataframes and fk.parent_table in dataframes:
            child_df = dataframes[fk.child_table]
            parent_df = dataframes[fk.parent_table]

            child_vals = set(child_df[fk.child_column].dropna().unique())
            parent_vals = set(parent_df[fk.parent_column].unique())

            orphans = child_vals - parent_vals
            if orphans:
                orphan_records[f"{fk.child_table}.{fk.child_column}"] = len(orphans)
                fk_integrity_passed = False

    # Check data types match schema
    for table in schema.tables:
        if table.name in dataframes:
            df = dataframes[table.name]
            for col in table.columns:
                if col.name in df.columns:
                    actual_type = str(df[col.name].dtype)
                    expected_type = col.datatype

                    # Basic type checking
                    if expected_type == 'integer' and 'int' not in actual_type:
                        data_type_issues.append(f"{table.name}.{col.name}: Expected integer, got {actual_type}")
                    elif expected_type == 'float' and 'float' not in actual_type:
                        data_type_issues.append(f"{table.name}.{col.name}: Expected float, got {actual_type}")

    # Calculate quality score
    score = 10.0
    if not fk_integrity_passed:
        score -= 3.0
    if data_type_issues:
        score -= min(3.0, len(data_type_issues) * 0.5)

    return PreviewValidationResult(
        fk_integrity_passed=fk_integrity_passed,
        orphan_records=orphan_records,
        data_type_issues=data_type_issues[:10],  # Limit to 10
        quality_score=max(0.0, score)
    )


async def _run_phase4_generation(session_id: str, dataset_size: int, session_dir: Path):
    """
    Run Phase 4 full generation in background.

    Steps:
    1. Generate full dataset
    2. Run quality validation
    3. Generate PDF report
    4. Generate Excel report with answers
    """
    from dataset_generator import DatasetGenerator
    from quality_validator import QualityValidator
    from pdf_generator import QualityReportPDF
    from excel_generator import SolutionExcelGenerator

    start_time = time.time()

    try:
        # Update progress
        sessions[session_id]["progress"] = {
            "stage": "data_generation",
            "percent": 20,
            "message": f"Generating {dataset_size:,} rows of data...",
            "elapsed": time.time() - start_time
        }

        # Get schema and problem
        schema = Schema(**sessions[session_id]["schema"])
        problem = ProblemStatement(**sessions[session_id]["problem_statement"])
        input_data = ChallengeInput(**sessions[session_id]["input"])

        # Generate full dataset
        data_gen = DatasetGenerator(seed=int(time.time()))
        dataframes = data_gen.generate(schema, dataset_size)

        # Save datasets
        datasets_dir = session_dir / "datasets"
        data_gen.save_to_disk(datasets_dir)

        # Update progress
        sessions[session_id]["progress"] = {
            "stage": "quality_validation",
            "percent": 50,
            "message": "Running quality validation checks...",
            "elapsed": time.time() - start_time
        }

        # Run quality validation
        validator = QualityValidator(session_id)
        qa_results = validator.validate(schema, dataframes, input_data)

        # Save QA results
        with open(session_dir / "qa_results.json", "w") as f:
            json.dump(qa_results.model_dump(), f, indent=2, default=str)

        # Update progress
        sessions[session_id]["progress"] = {
            "stage": "pdf_generation",
            "percent": 70,
            "message": "Generating PDF quality report...",
            "elapsed": time.time() - start_time
        }

        # Generate PDF report
        pdf_path = session_dir / "quality_report.pdf"
        pdf_gen = QualityReportPDF(pdf_path)
        pdf_gen.generate(qa_results, schema, dataframes, input_data)

        # Update progress
        sessions[session_id]["progress"] = {
            "stage": "excel_generation",
            "percent": 85,
            "message": "Generating Excel report with analytical answers...",
            "elapsed": time.time() - start_time
        }

        # Generate Excel report
        excel_path = session_dir / "analytical_answers.xlsx"
        excel_gen = SolutionExcelGenerator(excel_path)
        excel_gen.generate(qa_results, problem, dataframes)

        # Complete
        sessions[session_id]["progress"] = {
            "stage": "completed",
            "percent": 100,
            "message": "Generation complete!",
            "elapsed": time.time() - start_time
        }

        sessions[session_id].update({
            "phase4_status": "completed",
            "qa_results": qa_results.model_dump(),
            "pdf_report_path": str(pdf_path),
            "excel_report_path": str(excel_path),
            "completion_timestamp": datetime.now().isoformat()
        })

        logger.info(f"Phase 4 completed for session {session_id} - Score: {qa_results.overall_score}")

    except Exception as e:
        logger.error(f"Phase 4 generation failed: {e}", exc_info=True)
        sessions[session_id]["phase4_status"] = "failed"
        sessions[session_id]["error"] = str(e)
        sessions[session_id]["progress"] = {
            "stage": "failed",
            "percent": 0,
            "message": f"Generation failed: {str(e)}",
            "elapsed": time.time() - start_time
        }


def _create_download_package(session_id: str, session_dir: Path) -> DownloadPackage:
    """
    Create complete download package with all files.
    """
    import shutil

    # Create package directory
    package_dir = session_dir / "package"
    package_dir.mkdir(exist_ok=True)

    # Copy CSV files
    datasets_dir = session_dir / "datasets"
    csv_files = []
    if datasets_dir.exists():
        for csv_file in datasets_dir.glob("*.csv"):
            shutil.copy(csv_file, package_dir / csv_file.name)
            csv_files.append(csv_file.name)

    # Copy PDF report
    pdf_path = session_dir / "quality_report.pdf"
    if pdf_path.exists():
        shutil.copy(pdf_path, package_dir / "quality_report.pdf")

    # Copy Excel report
    excel_path = session_dir / "analytical_answers.xlsx"
    if excel_path.exists():
        shutil.copy(excel_path, package_dir / "analytical_answers.xlsx")

    # Create data dictionary
    schema = Schema(**sessions[session_id]["schema"])
    data_dict_path = package_dir / "data_dictionary.txt"
    _create_data_dictionary(schema, data_dict_path)

    # Create README
    readme_path = package_dir / "README.txt"
    _create_readme(session_id, readme_path)

    # Create ZIP
    zip_path = session_dir / f"codebasics_data_challenge_{session_id}.zip"
    shutil.make_archive(str(zip_path.with_suffix('')), 'zip', package_dir)

    return DownloadPackage(
        csv_files=csv_files,
        pdf_report="quality_report.pdf",
        excel_report="analytical_answers.xlsx",
        data_dictionary="data_dictionary.txt",
        readme="README.txt",
        zip_path=str(zip_path)
    )


def _create_data_dictionary(schema: Schema, output_path: Path):
    """Create human-readable data dictionary."""
    with open(output_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("CODEBASICS DATA FACTORY - DATA DICTIONARY\n")
        f.write("=" * 80 + "\n\n")

        for table in schema.tables:
            f.write(f"\nTable: {table.name}\n")
            f.write(f"Description: {table.description}\n")
            f.write(f"Primary Key: {table.primary_key}\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Column':<30} {'Type':<15} {'Nullable':<10} {'Description'}\n")
            f.write("-" * 80 + "\n")

            for col in table.columns:
                nullable = "Yes" if col.nullable else "No"
                f.write(f"{col.name:<30} {col.datatype:<15} {nullable:<10} {col.description}\n")

            f.write("\n")

        # Relationships
        f.write("\n" + "=" * 80 + "\n")
        f.write("RELATIONSHIPS\n")
        f.write("=" * 80 + "\n")

        for rel in schema.relationships:
            f.write(f"\n{rel.parent_table}.{rel.parent_column} -> {rel.child_table}.{rel.child_column}")
            f.write(f" ({rel.cardinality})\n")


def _create_readme(session_id: str, output_path: Path):
    """Create README file for the package."""
    problem = ProblemStatement(**sessions[session_id]["problem_statement"])

    with open(output_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("CODEBASICS DATA FACTORY - DATA CHALLENGE PACKAGE\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Challenge Title: {problem.title}\n")
        f.write(f"Company: {problem.company_name}\n")
        f.write(f"Difficulty: {problem.difficulty.value}\n")
        f.write(f"Generated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}\n\n")

        f.write("PACKAGE CONTENTS:\n")
        f.write("-" * 80 + "\n")
        f.write("1. CSV Files - Raw data tables for analysis\n")
        f.write("2. quality_report.pdf - Comprehensive data quality validation report\n")
        f.write("3. analytical_answers.xlsx - Answers to analytical questions with visuals\n")
        f.write("4. data_dictionary.txt - Complete schema and column descriptions\n")
        f.write("5. README.txt - This file\n\n")

        f.write("ANALYTICAL QUESTIONS:\n")
        f.write("-" * 80 + "\n")
        for i, q in enumerate(problem.analytical_questions, 1):
            f.write(f"{i}. {q}\n")

        f.write("\n\nHOW TO USE:\n")
        f.write("-" * 80 + "\n")
        f.write("1. Import CSV files into your preferred tool (Excel, Power BI, Tableau, SQL)\n")
        f.write("2. Review the data dictionary to understand table relationships\n")
        f.write("3. Analyze the data to answer the analytical questions\n")
        f.write("4. Compare your answers with the provided Excel report\n")
        f.write("5. Check the quality report to understand data characteristics\n\n")

        f.write("TOOLS RECOMMENDED:\n")
        f.write("-" * 80 + "\n")
        f.write("- Microsoft Excel / Google Sheets (Beginner)\n")
        f.write("- Power BI / Tableau (Intermediate)\n")
        f.write("- SQL + Python/R (Advanced)\n\n")

        f.write("SUPPORT:\n")
        f.write("-" * 80 + "\n")
        f.write("For questions or issues, visit: https://codebasics.io\n")
        f.write("Happy Learning!\n")


async def run_pipeline(session_id: str, input_data: ChallengeInput, session_dir: Path):
    """Run the complete generation pipeline in background."""
    from dataset_generator import DatasetGenerator
    from quality_validator import QualityValidator
    from pdf_generator import QualityReportPDF
    
    start_time = time.time()
    from config import QUALITY_APPROVED_THRESHOLD, MAX_REGENERATION_ITERATIONS
    
    current_iteration = 1
    best_results = None
    best_score = -1.0

    while current_iteration <= MAX_REGENERATION_ITERATIONS:
        try:
            # Stage 1: Schema Generation
            sessions[session_id]["progress"] = {
                "stage": "schema_generation",
                "percent": 10 + (current_iteration - 1) * 5,
                "message": f"Iteration {current_iteration}: Generating schema...",
                "elapsed": time.time() - start_time
            }

            schema_gen = SchemaGenerator()
            schema = schema_gen.generate(input_data)

            # Stage 2: Data Generation
            sessions[session_id]["progress"] = {
                "stage": "data_generation",
                "percent": 30 + (current_iteration - 1) * 5,
                "message": f"Iteration {current_iteration}: Generating realistic dataset...",
                "elapsed": time.time() - start_time
            }
            
            data_gen = DatasetGenerator(seed=int(time.time()))
            dataframes = data_gen.generate(schema, input_data.dataset_size)
            
            # Stage 3: QA Validation
            sessions[session_id]["progress"] = {
                "stage": "qa_validation",
                "percent": 60 + (current_iteration - 1) * 5,
                "message": f"Iteration {current_iteration}: Running validation...",
                "elapsed": time.time() - start_time
            }
            
            validator = QualityValidator(session_id)
            qa_results = validator.validate(schema, dataframes, input_data)
            
            if qa_results.overall_score > best_score:
                best_score = qa_results.overall_score
                best_results = (schema, dataframes, qa_results)
            
            if qa_results.overall_score >= QUALITY_APPROVED_THRESHOLD and qa_results.status != "Regenerate":
                logger.info(f"Target quality reached on iteration {current_iteration}")
                break
            
            logger.info(f"Iteration {current_iteration} score {qa_results.overall_score} below threshold. Retrying...")
            current_iteration += 1

        except Exception as e:
            logger.error(f"Iteration {current_iteration} failed: {e}")
            if current_iteration == MAX_REGENERATION_ITERATIONS and not best_results:
                raise
            current_iteration += 1

    # Use best results obtained
    schema, dataframes, qa_results = best_results
    
    try:
        # Final Stage: Save and Report
        sessions[session_id]["progress"] = {
            "stage": "finalizing",
            "percent": 90,
            "message": "Finalizing best dataset and report...",
            "elapsed": time.time() - start_time
        }
        
        # Save schema to file
        with open(session_dir / "schema.json", "w") as f:
            json.dump(schema.model_dump(), f, indent=2, default=str)

        # Save datasets
        datasets_dir = session_dir / "datasets"
        data_gen.save_to_disk(datasets_dir)
        
        # Save QA results
        with open(session_dir / "qa_results.json", "w") as f:
            json.dump(qa_results.model_dump(), f, indent=2, default=str)

        # Stage 4: PDF Report
        report_path = session_dir / "quality_report.pdf"
        pdf_gen = QualityReportPDF(report_path)
        pdf_gen.generate(qa_results, schema, dataframes, input_data)

        # Complete
        sessions[session_id]["progress"] = {
            "stage": "completed",
            "percent": 100,
            "message": f"Generation successful! (Used best of {current_iteration if current_iteration <= MAX_REGENERATION_ITERATIONS else MAX_REGENERATION_ITERATIONS} iterations)",
            "elapsed": time.time() - start_time
        }
        sessions[session_id].update({
            "status": "completed",
            "quality_score": qa_results.overall_score,
            "qa_status": qa_results.status,
            "completed_at": datetime.now()
        })

        logger.info(f"Pipeline completed for session {session_id}")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        sessions[session_id]["status"] = "failed"
        sessions[session_id]["error"] = str(e)
        sessions[session_id]["progress"] = {
            "stage": "failed",
            "percent": 0.0,
            "message": f"Generation failed: {str(e)}",
            "elapsed": time.time() - start_time
        }


@app.post("/api/challenge/create")
async def create_challenge(input_data: ChallengeInput, background_tasks: BackgroundTasks):
    """
    Create a new challenge: generate schema, data, validate, and produce PDF report.

    This is the main pipeline endpoint that orchestrates:
    1. Schema generation (AI-driven)
    2. Data generation (with business rules, FK integrity, distributions)
    3. Quality validation (6 categories)
    4. PDF report generation
    """
    session_id = str(uuid.uuid4())

    # Create session output folder
    session_dir = OUTPUT_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    # Store session data
    sessions[session_id] = {
        "input": input_data.model_dump(),
        "status": "started",
        "progress": {
            "stage": "initializing",
            "percent": 0,
            "message": "Starting challenge generation...",
            "elapsed": 0
        }
    }

    logger.info(f"Created new challenge session: {session_id}")
    logger.info(f"Input: domain={input_data.domain}, function={input_data.function}, difficulty={input_data.difficulty}")

    # Launch background pipeline
    background_tasks.add_task(run_pipeline, session_id, input_data, session_dir)

    return {
        "session_id": session_id,
        "status": "started",
        "message": "Challenge generation started. Poll /api/challenge/status/{session_id} for progress."
    }


@app.get("/api/challenge/status/{session_id}")
async def get_challenge_status(session_id: str) -> GenerationProgress:
    """Get current progress of challenge generation."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    progress = session.get("progress", {})

    return GenerationProgress(
        session_id=session_id,
        stage=progress.get("stage", "unknown"),
        current_step=progress.get("step", ""),
        percent_complete=progress.get("percent", 0.0),
        message=progress.get("message", ""),
        elapsed_seconds=progress.get("elapsed", 0.0)
    )


@app.get("/api/challenge/result/{session_id}")
async def get_challenge_result(session_id: str) -> ChallengeResult:
    """Get final result of challenge generation."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]

    if session["status"] == "failed":
        return ChallengeResult(
            session_id=session_id,
            status="failed",
            error=session.get("error", "Unknown error")
        )

    if session["status"] != "completed":
        return ChallengeResult(
            session_id=session_id,
            status="success",
            quality_score=None,
            qa_status=None,
            report_path=None,
            data_paths=[]
        )

    return ChallengeResult(
        session_id=session_id,
        status="success",
        quality_score=session.get("quality_score"),
        qa_status=session.get("qa_status"),
        report_path=f"/api/report/download/{session_id}",
        data_paths=[]
    )


@app.get("/api/report/download/{session_id}")
async def download_report(session_id: str):
    """Download PDF quality report."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    report_path = OUTPUT_DIR / session_id / "quality_report.pdf"

    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(
        path=report_path,
        media_type="application/pdf",
        filename=f"quality_report_{session_id}.pdf"
    )


@app.get("/api/challenge/session/{session_id}")
async def get_session_status(session_id: str):
    """
    Get comprehensive session status across all phases.

    Returns current phase, completion status, and available next actions.
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]

    # Determine current phase and status
    current_phase = session.get("phase", "phase1")

    # Build phase status summary
    phase_status = {
        "phase1": {
            "completed": session.get("problem_approved", False),
            "has_research": "research" in session,
            "has_problem": "problem_statement" in session
        },
        "phase2": {
            "completed": session.get("schema_approved", False),
            "has_schema": "schema" in session,
            "validation_score": session.get("schema_validation", {}).get("validation_score")
        },
        "phase3": {
            "completed": session.get("preview_approved", False),
            "has_preview": "preview_data" in session,
            "quality_score": session.get("preview_validation", {}).get("quality_score")
        },
        "phase4": {
            "completed": session.get("phase4_status") == "completed",
            "status": session.get("phase4_status"),
            "progress": session.get("progress", {}),
            "qa_score": session.get("qa_results", {}).get("overall_score")
        },
        "phase5": {
            "completed": "download_package" in session,
            "package_ready": "download_package" in session
        }
    }

    # Determine next available action
    next_action = None
    if not phase_status["phase1"]["completed"]:
        if not phase_status["phase1"]["has_research"]:
            next_action = "POST /api/challenge/phase1/research"
        elif not phase_status["phase1"]["has_problem"]:
            next_action = "POST /api/challenge/phase1/generate-problem"
        else:
            next_action = "POST /api/challenge/phase1/approve"
    elif not phase_status["phase2"]["completed"]:
        if not phase_status["phase2"]["has_schema"]:
            next_action = "POST /api/challenge/phase2/generate-schema"
        else:
            next_action = "POST /api/challenge/phase2/approve"
    elif not phase_status["phase3"]["completed"]:
        if not phase_status["phase3"]["has_preview"]:
            next_action = "POST /api/challenge/phase3/generate-preview"
        else:
            next_action = "POST /api/challenge/phase3/approve"
    elif not phase_status["phase4"]["completed"]:
        if phase_status["phase4"]["status"] == "generating":
            next_action = "Wait for generation to complete (poll /api/challenge/phase4/status)"
        else:
            next_action = "POST /api/challenge/phase4/generate-full"
    elif not phase_status["phase5"]["completed"]:
        next_action = "GET /api/challenge/phase5/prepare/{session_id}"
    else:
        next_action = "GET /api/challenge/phase5/download/{session_id}"

    return {
        "session_id": session_id,
        "current_phase": current_phase,
        "created_at": session.get("created_at"),
        "phase_status": phase_status,
        "next_action": next_action,
        "error": session.get("error")
    }


@app.get("/api/download/{session_id}")
async def download_data(session_id: str):
    """Download generated dataset files as a ZIP."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    import shutil
    import tempfile
    
    session_dir = OUTPUT_DIR / session_id
    datasets_dir = session_dir / "datasets"
    
    if not datasets_dir.exists():
        raise HTTPException(status_code=404, detail="Datasets not found")

    # Create temporary zip file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        # Zip the datasets directory
        zip_path = shutil.make_archive(tmp.name, 'zip', datasets_dir)
        
    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename=f"challenge_data_{session_id}.zip"
    )


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)
