# Codebasics Data Challenge Generator v2.0 — Atomic Task Breakdown

> **Source:** PRD v2.0 (Phase 1 Implementation)
> **Stack:** React 18+ (frontend) + Python (backend) + Claude Sonnet 4 API

---

# FOUNDATION PHASE: Data Quality Engine + PDF Report

> **Priority:** HIGHEST — Must be approved before any other work begins.
> **Goal:** User enters domain, function, problem statement → system generates dataset → runs comprehensive QA → produces detailed PDF validation report.
> **Why first:** This is the core value engine. Everything else (UI, chatbot, packaging) is built on top of this. Getting quality right here means fewer iterations later.

---

## FP-1. Project Setup (Minimal for Foundation)

### FP-1.1 Backend Initialization
- [ ] Create project folder structure: `/backend/src/`, `/backend/tests/`, `/backend/output/`
- [ ] Initialize `pyproject.toml` (or `requirements.txt`) with dependencies
- [ ] Install core: `fastapi`, `uvicorn`, `pydantic`
- [ ] Install data: `pandas`, `pyarrow`, `faker`, `numpy`
- [ ] Install PDF/charts: `matplotlib`, `reportlab`
- [ ] Install AI: `anthropic` SDK
- [ ] Create FastAPI entry point (`main.py`)
- [ ] Configure CORS middleware
- [ ] Set up logging (file + console)
- [ ] Create `config.py` with API key, defaults, constants

### FP-1.2 Frontend Initialization (Minimal Input Form)
- [ ] Scaffold React 18+ project (Vite)
- [ ] Install `lucide-react` for icons
- [ ] Set up API client utility (`api.js`)
- [ ] Create base page layout (white background, clean, minimal)

---

## FP-2. Simple Input Interface

### FP-2.1 Backend — Input Model
- [ ] Create `ChallengeInput` Pydantic model:
  - `domain`: string (required)
  - `function`: string (required)
  - `problem_statement`: string (required, 100–2000 chars)
  - `skill_level`: enum (Beginner / Intermediate / Advanced), default Intermediate
  - `dataset_size`: enum (1K / 5K / 10K / 25K), default 10K
  - `data_structure`: enum (Denormalized / Normalized), default Normalized
- [ ] Create `POST /api/challenge/create` endpoint — accept input, return session ID
- [ ] Create `GET /api/challenge/status/{session_id}` endpoint — return progress

### FP-2.2 Frontend — Input Form
- [ ] Create input form page with:
  - [ ] Domain text input (required)
  - [ ] Function text input (required)
  - [ ] Problem statement textarea (required, 100–2000 chars, char counter)
  - [ ] Skill level selector (Beginner / Intermediate / Advanced)
  - [ ] Dataset size selector (1K / 5K / 10K / 25K)
  - [ ] Data structure toggle (Denormalized / Normalized)
- [ ] "Generate & Validate" button (disabled until required fields filled)
- [ ] Loading/progress display while generation + validation runs
- [ ] Result page: quality score badge + download PDF button

---

## FP-3. Schema Generation (AI-Driven)

### FP-3.1 Schema Generator
- [ ] Create `SchemaGenerator` class
- [ ] Build Claude API prompt: domain + function + problem statement + skill level + structure → schema JSON
- [ ] Prompt must instruct AI to return structured JSON with:
  - [ ] Table definitions (name, description, source_system)
  - [ ] Column definitions (name, datatype, nullable, description, constraints, id_prefix if ID field)
  - [ ] Primary key definitions
  - [ ] Foreign key definitions (parent_table, parent_column, child_table, child_column)
  - [ ] Relationship cardinality (1:N, M:N)
  - [ ] Business rules (status transitions, calculated fields, financial constraints)
  - [ ] KPI definitions (name, formula, expected_trend)
  - [ ] Date range (default 2019–2024)
  - [ ] Event impacts (e.g., COVID dip in 2020, recovery in 2021)
- [ ] Create `Schema` Pydantic model to parse and validate AI response
- [ ] **Normalized path:** 3–5 related tables (dimensions + fact)
- [ ] **Denormalized path:** single flat table
- [ ] Enforce column counts by skill level:
  - [ ] Beginner: ~15 columns
  - [ ] Intermediate: ~22 columns
  - [ ] Advanced: ~30 columns
- [ ] Validate schema internally before proceeding:
  - [ ] All FK references point to existing tables/columns
  - [ ] All tables have primary keys
  - [ ] Column types are supported
  - [ ] Source systems identified per table

---

## FP-4. Data Generation Engine

### FP-4.1 Generation Orchestrator
- [ ] Create `DatasetGenerator` class
- [ ] Build dependency graph from FK relationships
- [ ] Topological sort: parent tables generated before child tables
- [ ] Detect circular dependencies (error)
- [ ] Implement deterministic seed-based generation
- [ ] Implement batch processing (configurable batch size for memory)
- [ ] Implement progress callback (table name, rows done, % complete)

### FP-4.2 ID Generators
- [ ] Implement prefixed ID generator (e.g., `CUST0001`, `TXN0001`, `PROD0001`)
  - [ ] Accept prefix + zero-padded width
  - [ ] Ensure uniqueness within table
- [ ] Implement auto-increment ID generator (fallback)
- [ ] Implement composite key generator (if schema defines composite PKs)

### FP-4.3 Column Value Generators
- [ ] **Integer** generator (min/max range, realistic distribution)
- [ ] **Float/Decimal** generator (precision 1–2 decimals, min/max)
- [ ] **String** generator (categorical from allowed values, or Faker-based)
- [ ] **Date** generator (within 2019–2024 range, weighted by month/year for seasonality)
- [ ] **DateTime** generator (date + realistic time distribution)
- [ ] **Boolean** generator (configurable true/false ratio, valid values only)
- [ ] **Enum/Category** generator (from schema-defined allowed values, NOT equal distribution)
- [ ] **Email** generator (fictional domains only, e.g., `@fakecorp.example`)
- [ ] **Phone** generator (fictional patterns)
- [ ] **Name** generator (fictional person names)
- [ ] **Address** generator (fictional addresses)
- [ ] **Currency/Money** generator (realistic ranges per domain)
- [ ] **Status** generator (respects defined transition sequences)

### FP-4.4 FK Integrity Enforcement
- [ ] FK value picker: randomly select from parent table's actual PK values
- [ ] Guarantee zero orphan records in child tables
- [ ] Cross-system ID matching: same entity ID across tables from different source systems

### FP-4.5 Business Rule Enforcement
- [ ] Implement calculated field derivation (e.g., total = quantity * unit_price)
- [ ] Implement financial constraints (debit = credit, tax calculations, discount logic)
- [ ] Implement status progression rules (Pending → Shipped → Delivered, no impossible jumps)
- [ ] Implement date sequence rules (created < modified < closed)
- [ ] Implement conditional null rules (e.g., cancellation_reason only when status = Cancelled)

### FP-4.6 Distribution & Realism Engine
- [ ] Implement 80% normal distribution for key numeric metrics
- [ ] Implement 5–10% outlier injection (valid but extreme values)
- [ ] Implement unequal category distribution (NOT uniform — Pareto-like for realistic skew)
- [ ] Implement seasonal patterns (monthly/quarterly variation in date-based metrics)
- [ ] Implement regional variation (if geography columns exist)
- [ ] Implement narrative-aligned trends:
  - [ ] Revenue decline/growth matching problem statement percentages
  - [ ] KPI trend direction matching narrative (decline, spike, recovery)
- [ ] Implement external event simulation:
  - [ ] COVID-like dip (2020 impact)
  - [ ] Recovery patterns (2021–2022)
  - [ ] Impact magnitude within realistic bounds
  - [ ] Timeline effects consistent across related metrics

### FP-4.7 Intentional Data Quality Issues
- [ ] Implement missing value injector (2–5% of optional fields)
- [ ] Implement format inconsistency injector (date formats, phone formats)
- [ ] Implement duplicate record injector (small %, partial matches)
- [ ] Implement outlier injector (statistical outliers for detection exercises)
- [ ] Implement failed transaction records
- [ ] Implement reversed entries
- [ ] Implement backdated entries
- [ ] Implement delayed processing records
- [ ] Track ALL injected issues with metadata (row indices, columns, type, reason)
- [ ] Ensure intentional issues NEVER break FK integrity or PK uniqueness

### FP-4.8 Data Export (Internal)
- [ ] Save generated data per table as Parquet (canonical)
- [ ] Save generated data per table as CSV (UTF-8)
- [ ] Save generation metadata JSON (seed, row counts, duration, injected issues log)

---

## FP-5. Quality Validation Engine

### FP-5.1 Validation Framework
- [ ] Create `QualityValidator` class
- [ ] Define `ValidationCheck` base: name, category, severity, check function, result
- [ ] Define check result structure: pass/fail, score (0–10), message, details, data for charts
- [ ] Implement check runner: execute all checks, collect results
- [ ] Categorize results by section (technical, business, realism, learning, edge cases, schema)

### FP-5.2 Technical Integrity Checks (Category Weight: 25%)

#### Referential Integrity
- [ ] Check: all FK values exist in parent table (zero orphans)
- [ ] Check: no orphan records in child tables
- [ ] Check: parent tables were generated before child tables (order log)
- [ ] Check: cross-system IDs match correctly

#### Data Type Validation
- [ ] Check: ID fields follow prefix format (CUST0001, TXN0001, etc.)
- [ ] Check: date fields within defined range (2019–2024)
- [ ] Check: numeric fields within realistic min/max ranges
- [ ] Check: float precision consistent (1–2 decimals where needed)
- [ ] Check: boolean fields contain only valid values (True/False, no nulls in required)
- [ ] Check: no mixed data types in any column

#### Null & Completeness
- [ ] Check: required fields contain no unexpected nulls
- [ ] Check: optional fields contain nulls within 2–5% tolerance
- [ ] Check: no blank strings where null should exist
- [ ] Check: no default dummy placeholders ("Test", "NA", "N/A", "TBD")

#### Uniqueness Constraints
- [ ] Check: primary keys are unique per table
- [ ] Check: no duplicate transaction IDs
- [ ] Check: no duplicate composite keys (if applicable)

### FP-5.3 Business Logic Validation (Category Weight: 25%)

#### Financial & Transaction Checks
- [ ] Check: debit = credit (if accounting dataset)
- [ ] Check: calculated fields derive correctly from base values
- [ ] Check: totals match aggregation logic (quantity * price = total)
- [ ] Check: discounts applied logically (discount < original price)
- [ ] Check: tax calculations correct (tax = base * tax_rate)
- [ ] Check: revenue decline/growth matches story narrative percentage

#### Status Progression
- [ ] Check: status flows are logical (defined transitions only)
- [ ] Check: no impossible transitions (e.g., Delivered → Pending)
- [ ] Check: cancelled transactions have proper handling (reason, date)

#### KPI Consistency
- [ ] Check: all domain KPIs are calculable from data
- [ ] Check: KPI values are within realistic bounds
- [ ] Check: KPI trends reflect narrative (decline, growth, spike direction)
- [ ] Check: stated percentages align (e.g., "35% decline" → actual ~35%)

### FP-5.4 Realism & Distribution Checks (Category Weight: 20%)

#### Distribution Patterns
- [ ] Check: categories are NOT equally distributed
- [ ] Check: ~80% of key metrics follow normal distribution
- [ ] Check: 5–10% outliers present
- [ ] Check: 2–5% intentional data quality issues present
- [ ] Check: seasonal patterns visible in time-series data
- [ ] Check: regional variations present (if geography exists)

#### External Event Simulation
- [ ] Check: historical event impact reflected (e.g., COVID dip in 2020)
- [ ] Check: impact magnitude is realistic (not 90% drop for minor event)
- [ ] Check: timeline effects consistent across related metrics

### FP-5.5 Learning Objective Alignment (Category Weight: 20%)
- [ ] Check: dataset supports all defined learning objectives
- [ ] Check: sufficient variety for all analytical tasks
- [ ] Check: edge cases present for advanced analysis
- [ ] Check: anomalies present for detection exercises
- [ ] Check: data cleansing scenarios possible (dirty data exists to clean)
- [ ] Check: cross-system reconciliation possible (if multi-source)
- [ ] Check: audit trail exists (if compliance use case)

### FP-5.6 Edge Case Coverage
- [ ] Check: failed transactions exist
- [ ] Check: reversed entries exist
- [ ] Check: intentional duplicate records present (small %)
- [ ] Check: compliance violations present (if relevant domain)
- [ ] Check: backdated entries exist
- [ ] Check: delayed processing records exist

### FP-5.7 Schema & Architecture Validation
- [ ] Check: source systems identified correctly per table
- [ ] Check: tables align with learning complexity level
- [ ] Check: correct column count per level (Beginner: ~15, Intermediate: ~22, Advanced: ~30)
- [ ] Check: relationships mapped correctly (FK definitions match actual data)
- [ ] Check: row counts match configured size

### FP-5.8 Overall Quality Scoring
- [ ] Calculate per-category scores (0–10):
  - [ ] Technical Integrity: 25% weight
  - [ ] Business Logic: 25% weight
  - [ ] Realism & Distribution: 20% weight
  - [ ] Learning Alignment: 20% weight
  - [ ] Documentation/Schema: 10% weight
- [ ] Calculate weighted overall score (1–10)
- [ ] Apply decision rule:
  - [ ] >= 8.0 → **Approved**
  - [ ] 6.0–7.9 → **Regenerate** (flag issues, suggest fixes)
  - [ ] < 6.0 → **Rejected** (major issues listed)
- [ ] Generate key strengths list
- [ ] Generate issues list with severity + fix suggestions
- [ ] Save `qa_results.json` to output folder

---

## FP-6. PDF Validation Report

### FP-6.1 PDF Framework
- [ ] Create `QualityReportPDF` class
- [ ] Set up PDF document: A4, professional margins, consistent fonts
- [ ] Implement header/footer on every page (dataset name, date, page number)
- [ ] Implement page numbering
- [ ] Create matplotlib chart styling config (consistent colors, fonts, sizes)
- [ ] Define chart color palette matching brand colors

### FP-6.2 Page 1: Cover Page
- [ ] Render dataset name (large, prominent)
- [ ] Render domain
- [ ] Render function
- [ ] Render skill level
- [ ] Render dataset size
- [ ] Render Normalized / Denormalized indicator
- [ ] Render generated timestamp
- [ ] Render overall quality score (X / 10) with visual badge/gauge
- [ ] Render status: Approved / Regenerated / Failed (with color coding)

### FP-6.3 Page 2: Executive Summary
- [ ] Render overall quality score (prominent)
- [ ] Render total issues found
- [ ] Render issues fixed during regeneration (if applicable)
- [ ] Render remaining warnings (if any)
- [ ] Render approval recommendation text
- [ ] Keep to 1 page max

### FP-6.4 Page 3: Dataset Overview
- [ ] Render summary table:
  | Metric | Value |
  | Total Tables | X |
  | Total Rows | X |
  | Total Columns | X |
  | Null % Overall | X% |
  | Duplicate Records | X |
  | Outlier % | X% |
  | Date Range | 2019–2024 |
- [ ] Render per-table breakdown (table name, rows, columns, source system)

### FP-6.5 Pages 4–5: Schema Validation Section
- [ ] Render validation results:
  - [ ] Column names valid (pass/fail)
  - [ ] Data types correct (pass/fail)
  - [ ] Expected column count per level (actual vs expected)
  - [ ] Primary keys unique (pass/fail)
  - [ ] Foreign keys valid (pass/fail)
- [ ] **Visual: ERD Diagram** (matplotlib/graphviz — if normalized)
  - [ ] Table boxes with columns listed
  - [ ] Relationship lines with cardinality labels
- [ ] **Visual: Foreign key mapping table**
- [ ] **Visual: Column Type Distribution Bar Chart**
  - [ ] Count of string / int / float / date / bool columns
- [ ] **Visual: Table Row Count Bar Chart**
  - [ ] Each table's row volume

### FP-6.6 Pages 6–7: Technical Integrity Validation
- [ ] Render check results table:
  - [ ] Referential integrity (pass/fail + details)
  - [ ] Duplicate primary keys (count)
  - [ ] Null % per column (table format)
  - [ ] Date range validation (pass/fail)
  - [ ] Numeric min/max validation (pass/fail per column)
- [ ] **Visual: Null Percentage Heatmap**
  - [ ] Columns vs null % (color-coded)
- [ ] **Visual: Duplicate Record Count Bar Chart**
- [ ] **Visual: Date Distribution Line Chart**
  - [ ] Record count per month/year
- [ ] **Visual: Numeric Range Box Plots**
  - [ ] Key numeric columns (revenue, quantity, cost, etc.)

### FP-6.7 Pages 8–9: Business Logic Validation
- [ ] Render check results:
  - [ ] Calculated fields correct (pass/fail with sample)
  - [ ] Financial balancing (if applicable)
  - [ ] Status progression valid (pass/fail)
  - [ ] Story alignment assessment
- [ ] **Visual: Revenue Trend Line (2019–2024)**
  - [ ] Must reflect story narrative (decline/growth visible)
- [ ] **Visual: Category Distribution Pie/Bar Chart**
  - [ ] Show unequal distribution (NOT uniform)
- [ ] **Visual: Status Progression Bar Chart**
  - [ ] Show logical order validation (count per status)
- [ ] **Visual: KPI Calculation Snapshot Table**
  - [ ] Sample KPI calculation with actual values

### FP-6.8 Pages 10–11: Realism & Distribution Validation
- [ ] Render check results:
  - [ ] 80% normal distribution confirmation
  - [ ] 5–10% outliers present
  - [ ] 2–5% intentional anomalies
  - [ ] Seasonal pattern detected
  - [ ] Regional variation detected
- [ ] **Visual: Histogram for Key Metrics**
  - [ ] Revenue distribution
  - [ ] Quantity distribution
  - [ ] Cost distribution
- [ ] **Visual: Outlier Detection Scatter Plot**
  - [ ] Highlight extreme values in red
- [ ] **Visual: Seasonality Line Graph**
  - [ ] Monthly revenue trend showing seasonal patterns
- [ ] **Visual: Regional Performance Comparison Bar Chart**

### FP-6.9 Page 12: Edge Case Validation
- [ ] Render checks:
  - [ ] Failed transactions present
  - [ ] Duplicates (small %)
  - [ ] Reversed entries
  - [ ] Backdated entries
- [ ] **Visual: Edge Case Summary Table**
  - [ ] Type | Count | %
- [ ] **Visual: Anomaly Highlight Chart**
  - [ ] Mark outliers/anomalies in red on scatter

### FP-6.10 Page 13: Learning Objective Alignment
- [ ] Render alignment table:
  | Learning Objective | Supporting Data | Validation Status |
  - [ ] Row per objective from problem statement
  - [ ] Confirm data supports all objectives
  - [ ] Confirm sufficient variety
  - [ ] Confirm reconciliation possible

### FP-6.11 Page 14: Data Quality Score Breakdown
- [ ] Render scoring table:
  | Category | Score | Weight | Weighted Score |
  | Technical Integrity | X | 25% | X |
  | Business Logic | X | 25% | X |
  | Realism & Distribution | X | 20% | X |
  | Learning Alignment | X | 20% | X |
  | Documentation | X | 10% | X |
- [ ] Render final score: X / 10
- [ ] Render decision: Approved / Regenerate / Reject
- [ ] Display decision rule thresholds

### FP-6.12 Page 15: Issues & Regeneration Log
- [ ] If regenerated, render per-iteration:
  - [ ] Iteration number
  - [ ] Issues found (list)
  - [ ] Improvements made (list)
  - [ ] New score
- [ ] Max 3 iterations documented
- [ ] If first generation, render "First generation — no regeneration history"

### FP-6.13 Page 16: Appendix
- [ ] Render data dictionary snapshot (table → column → type → description)
- [ ] Render validation SQL snippets (optional, for advanced users)
- [ ] Render assumptions made during generation
- [ ] Render variation parameters used (distribution settings, outlier %, etc.)

### FP-6.14 Final Page: Mandatory Visual Summary Dashboard
- [ ] **One-page consolidated dashboard with:**
  - [ ] Revenue Trend chart (small)
  - [ ] Null Heatmap (small)
  - [ ] Outlier Scatter (small)
  - [ ] Category Distribution (small)
  - [ ] KPI Snapshot (small table)
  - [ ] Overall Score Badge (large, prominent)
- [ ] Purpose: quick one-glance approval page

### FP-6.15 Visual Count Validation
- [ ] **Denormalized datasets:** minimum 8–12 visuals in report
- [ ] **Normalized datasets:** minimum 10–15 visuals (including ERD + relationship charts)
- [ ] Count all visuals and validate against minimum threshold

### FP-6.16 PDF Output
- [ ] Generate PDF file: `[DatasetName]_Quality_Report.pdf`
- [ ] Save to output folder
- [ ] Create `GET /api/report/download/{session_id}` endpoint
- [ ] Implement PDF compression for large reports

---

## FP-7. End-to-End Pipeline

### FP-7.1 Pipeline Orchestrator
- [ ] Create `ChallengePipeline` class
- [ ] Wire pipeline: Input → Schema Gen → Data Gen → QA Validation → PDF Report
- [ ] Implement progress tracking across all stages
- [ ] Handle errors at each stage (don't crash — report and continue where possible)
- [ ] If QA score < 8.0: auto-flag for regeneration (up to 3 iterations)
- [ ] Save all artifacts to session output folder

### FP-7.2 API Endpoints
- [ ] `POST /api/challenge/create` — start full pipeline
- [ ] `GET /api/challenge/status/{session_id}` — get progress (stage, %, message)
- [ ] `GET /api/challenge/result/{session_id}` — get final result (score, status, file paths)
- [ ] `GET /api/report/download/{session_id}` — download PDF report
- [ ] `GET /api/data/download/{session_id}` — download generated CSV/Parquet files

### FP-7.3 Frontend — Results Display
- [ ] Show generation + validation progress bar
- [ ] Display final quality score badge (color-coded: green/orange/red)
- [ ] Display status: Approved / Regenerated / Failed
- [ ] "Download PDF Report" button
- [ ] "Download Dataset" button
- [ ] Summary stats: tables, rows, score, issue count

---

## FP-8. Testing

### FP-8.1 Unit Tests
- [ ] Test schema generator output structure (valid JSON, required fields)
- [ ] Test each column value generator (types, ranges, constraints)
- [ ] Test prefixed ID generator (format, uniqueness)
- [ ] Test FK integrity enforcement (zero orphans)
- [ ] Test each QA check individually with known-good and known-bad data
- [ ] Test quality scoring formula (weights, thresholds, decision rules)
- [ ] Test intentional issue injectors (correct percentages, no FK breaks)
- [ ] Test distribution generators (normal dist, outlier %, seasonal patterns)

### FP-8.2 Integration Tests
- [ ] Test full pipeline: e-commerce domain, normalized, intermediate, 1K rows
- [ ] Test full pipeline: healthcare domain, denormalized, beginner, 1K rows
- [ ] Test full pipeline: finance domain, normalized, advanced, 5K rows
- [ ] Verify PDF generates with correct page count and all required visuals
- [ ] Verify same seed produces identical dataset
- [ ] Verify QA catches intentionally broken data (test with bad data)

### FP-8.3 Sample Scenarios
- [ ] Create test input: E-Commerce + Sales & Marketing (normalized, intermediate)
- [ ] Create test input: Banking + Finance & Accounting (normalized, advanced)
- [ ] Create test input: Healthcare + Operations (denormalized, beginner)
- [ ] Run each scenario end-to-end and validate PDF output manually

---

## FP-9. Foundation Phase Milestone Checklist

### Must pass before moving to full application:
- [ ] User can enter domain + function + problem statement
- [ ] AI generates appropriate schema (tables, columns, relationships, rules)
- [ ] Generator produces data respecting ALL business rules and FK integrity
- [ ] Data has realistic distributions (not uniform), outliers, seasonal patterns
- [ ] Intentional quality issues injected without breaking integrity
- [ ] QA engine validates all 6 categories (technical, business, realism, learning, edge cases, schema)
- [ ] Quality score computed correctly with weighted formula
- [ ] Decision rule applied: >=8 Approved, 6-7.9 Regenerate, <6 Reject
- [ ] PDF report generates with ALL required pages (cover through dashboard)
- [ ] PDF contains minimum visual count (8-12 denormalized, 10-15 normalized)
- [ ] Every visual listed in the spec appears in the PDF
- [ ] Report is human-reviewable and professional quality
- [ ] End-to-end pipeline runs for at least 3 different domain scenarios
- [ ] Same seed produces identical output (deterministic)

---
---

# FULL APPLICATION PHASES (Deferred — build after Foundation Phase approved)

> The sections below are the remaining tasks from the full PRD.
> They will be detailed and executed only after the Foundation Phase is approved.

## Deferred: Full UI Multi-Phase Workflow
- Phase 0: Chip-based configuration UI (domain, function, size, skill, structure selectors)
- Phase 1: Research-driven problem statement with web_search + character integration
- Phase 2: Schema generation with ERD visualization + approval gate
- Phase 3: Dataset preview (10-30 rows) with mini charts + approval gate
- Phase 4: Full generation + QA + PDF (leverages Foundation Phase engine)
- Phase 5: ZIP packaging + solution guide + downloads

## Deferred: Chatbot System
- Context-aware chatbot per phase
- Multi-turn conversations
- Suggested prompts
- Regeneration with feedback

## Deferred: Branding & Design System
- Brand character highlighting (Peter Pandey, Tony Sharma, Bruce Hariyali)
- Phase progress indicator (always visible)
- Color palette implementation
- Success animations (confetti, checkmarks)
- Full component library (chips, toasts, modals, etc.)

## Deferred: Advanced Features
- Research caching
- Regeneration log (up to 3 iterations with score tracking)
- Solution guide PDF generation
- Data dictionary CSV export
- Challenge document PDF
- Metadata JSON packaging

## Deferred: Deployment & Packaging
- Windows EXE bundling
- Installer creation
- Production build scripts
