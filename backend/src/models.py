"""
Pydantic models for request/response validation and data structures.
"""
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum


class ChatRequest(BaseModel):
    """Request for context-aware chatbot."""
    session_id: Optional[str] = None
    message: str
    phase: str


class Difficulty(str, Enum):
    """Difficulty levels for dataset complexity."""
    EASY = "Easy"
    MEDIUM = "Medium"
    DIFFICULT = "Difficult"


class DataStructure(str, Enum):
    """Data structure types."""
    NORMALIZED = "Normalized"
    DENORMALIZED = "Denormalized"


class ChallengeInput(BaseModel):
    """Input model for challenge creation."""
    domain: str = Field(..., min_length=3, max_length=100, description="Business domain")
    function: str = Field(..., min_length=3, max_length=100, description="Business function")
    problem_statement: str = Field(
        ...,
        min_length=100,
        max_length=2000,
        description="Complete problem description"
    )
    difficulty: Difficulty = Field(default=Difficulty.MEDIUM)
    dataset_size: int = Field(default=10000, ge=1000, le=1000000)
    data_structure: DataStructure = Field(default=DataStructure.NORMALIZED)
    primary_questions: Optional[str] = Field(None, description="Primary business questions to be answered by the data")

    @field_validator('dataset_size')
    @classmethod
    def validate_dataset_size(cls, v):
        # Allow any size within range [1000, 1M] to be more flexible
        if v < 1000 or v > 1000000:
            raise ValueError("Dataset size must be between 1,000 and 1,000,000")
        return v


class ColumnDefinition(BaseModel):
    """Schema column definition."""
    name: str
    datatype: str
    nullable: bool = True
    description: str = ""
    constraints: Optional[Dict[str, Any]] = None
    id_prefix: Optional[str] = None  # For prefixed IDs like CUST0001
    allowed_values: Optional[List[Any]] = None  # For enums/categories


class TableDefinition(BaseModel):
    """Schema table definition."""
    name: str
    description: str
    source_system: Optional[str] = None
    columns: List[ColumnDefinition]
    primary_key: str
    parent_table: Optional[str] = None  # For FK relationships


class ForeignKeyDefinition(BaseModel):
    """Foreign key relationship definition."""
    parent_table: str
    parent_column: str
    child_table: str
    child_column: str
    cardinality: str = "1:N"  # 1:N, M:N, 1:1


class BusinessRule(BaseModel):
    """Business rule definition."""
    rule_type: str  # "status_transition", "calculated_field", "constraint"
    description: str
    parameters: Dict[str, Any]


class KPIDefinition(BaseModel):
    """KPI definition."""
    name: str
    formula: str
    expected_trend: str  # "decline", "growth", "stable", "spike"
    narrative_percentage: Optional[float] = None  # e.g., 35.0 for "35% decline"


class EventImpact(BaseModel):
    """External event impact definition."""
    event_name: str  # e.g., "COVID-19 Pandemic"
    start_date: str  # "2020-03-01"
    end_date: str  # "2020-12-31"
    impact_magnitude: float  # -0.30 for 30% decline
    affected_metrics: List[str]


class Schema(BaseModel):
    """Complete dataset schema."""
    tables: List[TableDefinition]
    relationships: List[ForeignKeyDefinition]
    business_rules: List[BusinessRule]
    kpis: List[KPIDefinition]
    date_range_start: str = "2019-01-01"
    date_range_end: str = "2024-12-31"
    event_impacts: List[EventImpact] = []


class ValidationCheckResult(BaseModel):
    """Result of a single validation check."""
    check_name: str
    category: str
    passed: bool
    score: float = Field(ge=0.0, le=10.0)
    message: str
    details: Optional[Dict[str, Any]] = None
    severity: Literal["blocker", "warning", "info"] = "info"


class QAResults(BaseModel):
    """Complete QA validation results."""
    session_id: str
    overall_score: float = Field(ge=0.0, le=10.0)
    category_scores: Dict[str, float]
    status: Literal["Approved", "Regenerate", "Rejected"]
    checks: List[ValidationCheckResult]
    strengths: List[str]
    issues: List[str]
    generated_at: datetime
    iteration_number: int = 1


class GenerationProgress(BaseModel):
    """Progress tracking for generation."""
    session_id: str
    stage: str  # "schema", "generation", "validation", "report"
    current_step: str
    percent_complete: float = Field(ge=0.0, le=100.0)
    message: str
    elapsed_seconds: float


class ChallengeResult(BaseModel):
    """Final result of challenge generation."""
    session_id: str
    status: Literal["success", "failed"]
    quality_score: Optional[float] = None
    qa_status: Optional[Literal["Approved", "Regenerate", "Rejected"]] = None
    report_path: Optional[str] = None
    data_paths: List[str] = []
    error: Optional[str] = None
    completed_at: Optional[datetime] = None


class ResearchSource(BaseModel):
    """Single research source with insights."""
    title: str
    url: str
    source_type: str = "Search"  # "News", "Trends", "Search"
    relevance: str  # "high", "medium", "low"
    is_primary: bool = False  # Main case study?
    key_insights: List[str]
    publication_date: Optional[str] = None


class ResearchResult(BaseModel):
    """Research findings for a domain."""
    session_id: str
    domain: str
    function: str
    sources: List[ResearchSource]
    domain_insights: List[str]
    identified_kpis: List[str]
    industry_challenges: List[str]
    generated_at: datetime


class ProblemStatement(BaseModel):
    """AI-generated problem statement with characters."""
    session_id: str
    company_name: str
    title: str
    statement: str  # 300-400 words
    character_positions: Dict[str, List[int]]  # {peter_pandey: [10, 245], ...}
    analytical_questions: List[str]  # Questions based on difficulty
    research_id: str
    difficulty: Difficulty
    generated_at: datetime


class Phase1Response(BaseModel):
    """Response for Phase 1 (Research & Problem)."""
    session_id: str
    phase: str = "phase1"
    status: Literal["pending_approval", "approved", "failed"]
    research: Optional[ResearchResult] = None
    problem_statement: Optional[ProblemStatement] = None
    approval_timestamp: Optional[datetime] = None
    message: str = ""


class SchemaValidationResult(BaseModel):
    """Schema validation against analytical questions."""
    can_answer_all: bool
    validation_score: float = Field(ge=0.0, le=10.0)
    answerable_questions: List[int]  # indices of questions that can be answered
    missing_capabilities: List[str]  # what's missing to answer remaining questions
    recommendations: List[str]


class Phase2Response(BaseModel):
    """Response for Phase 2 (Schema Generation)."""
    session_id: str
    phase: str = "phase2"
    status: Literal["pending_approval", "approved", "regenerate", "failed"]
    schema: Optional[Schema] = None
    validation: Optional[SchemaValidationResult] = None
    approval_timestamp: Optional[datetime] = None
    message: str = ""


class PreviewData(BaseModel):
    """Preview data for Phase 3."""
    table_name: str
    sample_rows: List[Dict[str, Any]]
    row_count: int
    column_count: int


class PreviewValidationResult(BaseModel):
    """Preview validation results."""
    fk_integrity_passed: bool
    orphan_records: Dict[str, int]
    data_type_issues: List[str]
    quality_score: float = Field(ge=0.0, le=10.0)


class Phase3Response(BaseModel):
    """Response for Phase 3 (Preview Generation)."""
    session_id: str
    phase: str = "phase3"
    status: Literal["pending_approval", "approved", "regenerate", "failed"]
    preview_data: List[PreviewData] = []
    validation: Optional[PreviewValidationResult] = None
    approval_timestamp: Optional[datetime] = None
    message: str = ""


class GenerationSizeInput(BaseModel):
    """Input for full dataset generation size."""
    dataset_size: int = Field(ge=1000, le=100000, description="Number of rows for main fact table")


class Phase4Response(BaseModel):
    """Response for Phase 4 (Full Generation)."""
    session_id: str
    phase: str = "phase4"
    status: Literal["generating", "completed", "failed"]
    qa_results: Optional[QAResults] = None
    pdf_report_path: Optional[str] = None
    excel_report_path: Optional[str] = None
    completion_timestamp: Optional[datetime] = None
    message: str = ""


class DownloadPackage(BaseModel):
    """Download package contents."""
    csv_files: List[str]
    pdf_report: str
    excel_report: str
    data_dictionary: str
    readme: str
    zip_path: str


class Phase5Response(BaseModel):
    """Response for Phase 5 (Downloads)."""
    session_id: str
    phase: str = "phase5"
    status: Literal["ready", "failed"]
    package: Optional[DownloadPackage] = None
    download_url: str = ""
    message: str = ""
