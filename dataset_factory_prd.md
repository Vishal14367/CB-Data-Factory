# Product Requirements Document (PRD)
## Codebasics Data Challenge Generator v2.0 - Final Specification

**Document Version:** 2.0 (Phase 1 Implementation)  
**Last Updated:** February 6, 2025  
**Status:** Ready for Development  
**Authors:** Product Team + SOP Integration + Dataset Factory Alignment

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Branding & Design Guidelines](#2-branding--design-guidelines)
3. [Brand Characters](#3-brand-characters)
4. [Multi-Phase Workflow Architecture](#4-multi-phase-workflow-architecture)
5. [Phase 0: Initial Configuration](#5-phase-0-initial-configuration)
6. [Phase 1: Research-Driven Problem Statement](#6-phase-1-research-driven-problem-statement)
7. [Phase 2: Data Schema Generation](#7-phase-2-data-schema-generation)
8. [Phase 3: Dataset Preview](#8-phase-3-dataset-preview-pilot-generation)
9. [Phase 4: Full Dataset Generation + Quality Validation](#9-phase-4-full-dataset-generation--quality-validation)
10. [Phase 5: Final Downloads](#10-phase-5-final-downloads)
11. [Data Quality Validation Framework](#11-data-quality-validation-framework)
12. [Chatbot System Specifications](#12-chatbot-system-specifications)
13. [Progress Tracking & Visual Feedback](#13-progress-tracking--visual-feedback)
14. [Technical Implementation](#14-technical-implementation)
15. [Error Handling & Edge Cases](#15-error-handling--edge-cases)
16. [Performance Optimization](#16-performance-optimization)
17. [Success Metrics & Analytics](#17-success-metrics--analytics)
18. [Future Enhancements](#18-future-enhancements-post-phase-1)
19. [Documentation Requirements](#19-documentation-requirements)
20. [Acceptance Criteria Summary](#20-acceptance-criteria-summary)
21. [Risk Mitigation](#21-risk-mitigation)
22. [Glossary](#22-glossary)
23. [Appendix: Sample Workflow](#23-appendix-sample-workflow)

---

## 1. Executive Summary

### 1.1 Product Overview

**Codebasics Data Challenge Generator v2.0** is an AI-powered web application that generates realistic, story-driven data challenges for learners through a research-driven, multi-phase validation workflow. The tool creates complete challenge packages with rigorous data quality validation at each step, ensuring datasets are pedagogically sound and technically accurate.

### 1.2 Key Improvements from v1.0

- ✅ Multi-phase workflow with mandatory approval gates
- ✅ Real-time research integration for authenticity
- ✅ Interactive chatbot for iterative refinement
- ✅ Comprehensive PDF quality reports with matplotlib visualizations
- ✅ SOP-compliant validation framework
- ✅ OLTP normalized data structure (learners build star schema)
- ✅ Quality-first approach: no progression without approval
- ✅ Dataset Factory alignment for production-grade datasets

### 1.3 Target Users

- Codebasics instructors creating data challenges
- Course designers developing practice problems
- Internal content creators for videos/courses
- Future: External collaborators using packaged application

### 1.4 Core Value Proposition

- **Research-driven authenticity**: Real-time web research ensures domain relevance
- **Quality-first workflow**: Comprehensive validation at every stage blocks poor quality
- **Interactive refinement**: Chatbot-assisted regeneration with context awareness
- **Production-ready datasets**: SOP-compliant generation with full documentation
- **Complete transparency**: Research sources, validation criteria, and quality metrics visible

---

## 2. Branding & Design Guidelines

### 2.1 Identity

- **Product Name**: Codebasics Data Challenge Generator (capital C mandatory)
- **Version**: v2.0 (Phase 1 Implementation)
- **Tagline**: "Research-driven data challenges with quality validation"
- **No AI branding**: Never mention "AI Powered" or show AI icons/logos
- **No Codebasics logo**: Remove logo completely from interface

### 2.2 Color Palette

**Primary Colors:**
- Blue: `#3B82F6` - Main brand color, primary CTAs, Tony Sharma highlight
- Purple: `#6F53C1` - Character highlights, accents, Bruce Hariyali highlight
- Navy: `#3F4C78` - Secondary elements
- Dark: `#181830` - Header background
- White: `#FFFFFF` - Main background (mandatory)

**Secondary Colors:**
- Lime Yellow: `#D7EF3F` - Highlights
- Light Blue: `#E1E3FA` - Subtle backgrounds
- Orange: `#FD7E15` - Warnings, regeneration needed
- Green: `#20C997` - Success states, approval, Peter Pandey highlight
- Pink: `#D63384` - Special accents

### 2.3 UI/UX Principles

- **White background** - Clean, minimal, professional interface
- **Progressive disclosure** - Show only relevant phase content
- **Clear phase indicators** - Visual progress through workflow (always visible)
- **Action clarity** - Approve vs Regenerate always distinct
- **Feedback integration** - Chatbot seamlessly embedded for refinement
- **Generous whitespace** - Not cramped or cluttered
- **Self-explanatory** - Tooltips on complex options
- **Error prevention** - Validate inputs, block invalid states

---

## 3. Brand Characters

### 3.1 Character Roles & Highlighting

**Peter Pandey** 🟢
- **Role**: Data Analyst (the learner)
- **Represents**: The humble learner navigating the data world
- **Highlight Color**: Green (`#20C997`)
- **Highlight Style**: `background: #20C99730; color: #20C997; font-weight: 700; padding: 2px 8px; border-radius: 4px;`

**Tony Sharma** 🔵
- **Role**: VP/Senior Executive
- **Represents**: Helpful senior guiding through professional challenges
- **Highlight Color**: Blue (`#3B82F6`)
- **Highlight Style**: `background: #3B82F630; color: #3B82F6; font-weight: 700; padding: 2px 8px; border-radius: 4px;`

**Bruce Hariyali** 🟣
- **Role**: Business Owner/Stakeholder
- **Represents**: Decision-maker identifying business problems
- **Highlight Color**: Purple (`#6F53C1`)
- **Highlight Style**: `background: #6F53C130; color: #6F53C1; font-weight: 700; padding: 2px 8px; border-radius: 4px;`
- **Tone**: Sage archetype language

### 3.2 Character Integration Requirements

- All three characters MUST appear in every problem statement
- Names must be visually highlighted with colored backgrounds (case-insensitive matching)
- Story ends with: **"Imagine yourself as Peter Pandey..."**
- Characters should have realistic roles within the fictional company context

---

## 4. Multi-Phase Workflow Architecture

### 4.1 Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    QUALITY-GATED WORKFLOW                    │
└─────────────────────────────────────────────────────────────┘

Phase 0: Initial Configuration
    ↓ (User Input: Domain, Function, Level, Structure, Size, Context)
    
Phase 1: Research-Driven Problem Statement
    ↓ (Research → Generate → Validate → Approve/Regenerate)
    ↓ Quality Gate: Problem must be domain-authentic & answerable
    
Phase 2: Data Schema Generation  
    ↓ (Generate OLTP Schema → Validate → Approve/Regenerate)
    ↓ Quality Gate: Schema must support all questions
    
Phase 3: Dataset Preview (Pilot Generation)
    ↓ (Generate 10-30 rows → Validate relationships → Approve/Regenerate)
    ↓ Quality Gate: Preview must show realistic patterns
    
Phase 4: Full Dataset + Quality Validation
    ↓ (Generate full dataset → Run QA → Create PDF → Approve/Regenerate)
    ↓ Quality Gate: Comprehensive validation must pass
    
Phase 5: Final Downloads
    ↓ (Package ZIP with all components)
    
✓ Challenge Complete
```

### 4.2 Approval Gate Philosophy

**Non-Negotiable Rule**: User cannot proceed to next phase without explicit approval of current phase. This ensures:
- Quality is validated at each stage
- Issues are caught early (cheaper to fix)
- Final dataset is production-ready
- Learning objectives are preserved throughout

**Regeneration**: At any phase, user can request regeneration with feedback via chatbot. The system will:
1. Open contextual chatbot
2. Collect structured feedback
3. Regenerate with improvements
4. Present updated content for re-approval

---

## 5. Phase 0: Initial Configuration

### 5.1 Input Fields

#### Domain Selection
**Type**: Chip-based selection  
**Options**: 13 predefined + "Other" with custom input

**Predefined Domains:**
1. Fast Food Industry
2. E-Commerce
3. Healthcare
4. Banking & Finance
5. Real Estate
6. Retail
7. Tourism & Travel
8. Education
9. Logistics & Supply Chain
10. Telecom
11. Automobile
12. Agriculture
13. Other (reveals text input)

**Validation**: 
- Required field
- Selected domain must be visually distinct (filled background, colored border)
- Custom domain must be 3-50 characters

#### Function Selection
**Type**: Chip-based selection  
**Purpose**: Specify business function focus area

**Options:**
- Sales & Marketing
- Operations  
- Finance & Accounting
- Human Resources
- Supply Chain
- Customer Service
- Product Management
- Risk & Compliance
- IT & Technology
- Other (with text input)

**Tooltip**: "The business function this challenge focuses on (e.g., Sales, Operations)"  
**Validation**: Required field

#### Dataset Size Selection
**Type**: Chip-based selection  
**Options**: 1K, 5K, 10K, 25K, 50K, 100K rows  
**Default**: 10K  
**Note**: Sizes > 25K show warning about generation time

#### Skill Level Selection
**Type**: Chip-based selection  
**Options**: 
- **Beginner**: 15 columns, direct queries, simple analysis
- **Intermediate**: 22 columns, moderate complexity, joins required
- **Advanced**: 30 columns, complex analysis, multiple aggregations

**Default**: Intermediate

#### Data Structure Toggle
**Type**: Toggle button (Denormalized / Normalized)

**Denormalized**:
- Single flat CSV with all columns
- Easier for beginners
- No join complexity

**Normalized (OLTP)**:
- Multiple related tables (3-5 tables)
- Dimensions: customers, products, employees
- Fact table: transactions, events
- Learners practice building star schema
- Reflects real-world source systems

**Default**: Normalized (OLTP)

#### Complete Problem Context
**Type**: Multi-line textarea  
**Character Limit**: 2000 characters  
**Optional**: Yes, but strongly recommended

**Prompt Guide**:
```
Describe your complete challenge requirements:

• What business problem should this simulate?
• What specific analytical skills should learners practice?
• Are there specific metrics or KPIs to include?
• Any industry-specific regulations or constraints?
• Specific time periods or seasonal patterns?
• Any edge cases or anomalies to include?
```

### 5.2 Action Button

**Button**: "Start Challenge Creation"  
**State**: 
- Disabled until Domain and Function selected
- Enabled when ready
- Loading (spinner) when clicked

**Action**: Validates inputs, saves configuration, advances to Phase 1

---

## 6. Phase 1: Research-Driven Problem Statement

### 6.1 Research Process

**Research Sources** (via `web_search` tool):
- Recent industry news (past 6-12 months)
- Domain-specific reports and whitepapers
- Public datasets and case studies
- Regulatory updates
- Market trend analyses

**Research Constraints**:
- Publicly available, credible sources
- Prioritize past 2 years
- Extract 3-5 key insights per source
- Identify domain-specific KPIs

### 6.2 Problem Statement Generation

**AI Generates**:
1. Fictional company name (domain-appropriate)
2. Challenge title
3. Problem statement (300-400 words) with:
   - Timeline (2019-2024)
   - Business struggle (quantified)
   - Character introductions (Bruce, Tony, Peter)
   - Ends with "Imagine yourself as Peter Pandey..."
4. Analytical questions (5-7, skill-appropriate)

### 6.3 Output Display

- Problem statement with highlighted character names
- Analytical questions (formatted list)
- Research sources with attribution
- Approve/Regenerate buttons

### 6.4 Chatbot for Refinement

Opens on "Regenerate" click:
- Context-aware feedback collection
- Suggested prompts for common issues
- Multi-turn conversation support
- Regeneration with improvements

---

## 7. Phase 2: Data Schema Generation

### 7.1 Schema Generation

**For Normalized (OLTP)**:
- 3-5 related tables
- Dimension tables (master data)
- Fact table (transactions)
- Proper parent-child relationships
- Total columns: 15-30 based on skill level

**For Denormalized**:
- Single flat table
- All columns in one file

### 7.2 Schema Display

- Entity relationship diagram
- Expandable table details
- Column specifications (type, description, constraints)
- Relationship validation results
- Approve/Regenerate buttons

### 7.3 Validation Checks

- All questions answerable from schema
- All KPIs calculable
- Proper relationships defined
- OLTP normalization principles followed
- Skill-appropriate complexity

---

## 8. Phase 3: Dataset Preview (Pilot Generation)

### 8.1 Preview Generation

**Purpose**: Generate small sample (10-30 rows per table) to validate:
- Data looks realistic
- Relationships work correctly
- Distributions make sense

**Generation Rules**:
- Parent-first order (dimensions before facts)
- Referential integrity maintained
- Realistic distributions
- Sample edge cases included

### 8.2 Preview Display

- Tables with sample rows
- Quick statistics per table
- Relationship validation (sample joins)
- Quick analysis preview (mini charts)
- Approve/Regenerate buttons

### 8.3 Validation

Automated checks for:
- Foreign key integrity
- Data type consistency
- Null compliance
- Value ranges
- Date sequences

---

## 9. Phase 4: Full Dataset Generation + Quality Validation

### 9.1 Full Generation

**Process**:
1. Generate complete dataset (full row count)
2. Batch processing with progress updates
3. Validation during generation

### 9.2 Quality Validation (SOP + Dataset Factory Compliant)

**Comprehensive QA Suite**:

**Technical Integrity Checks**:
- Foreign key integrity (100% required)
- Date field validation
- Numeric range checks
- Required field validation
- Unique constraints
- Data type consistency

**Business Logic Validation**:
- Financial reconciliation
- Calculated field verification
- Status progression validation
- Business constraint checks
- KPI calculability

**Statistical Analysis**:
- Distribution analysis
- Correlation analysis
- Outlier detection
- Temporal pattern analysis

**Relationship Validation** (Normalized):
- Foreign key analysis
- Cardinality verification
- Join performance testing

**Learning Objective Alignment**:
- Problem statement alignment
- Analytical questions coverage
- Skill level appropriateness
- Edge cases for learning

**Intentional Data Quality Issues** (5-7%):
- Missing values: 5%
- Format inconsistencies: 2%
- Duplicate records: 1%
- Statistical outliers: 2-3%

### 9.3 Quality Report PDF (11 Pages)

**Page 1**: Executive Summary
- Overall score (1-10)
- Status (Approved/Needs Work)
- Category breakdown
- Key strengths
- Intentional issues summary

**Pages 2-3**: Technical Integrity
- FK integrity with charts
- Date validation
- Numeric ranges
- Required fields
- Unique constraints
- Data types

**Pages 4-5**: Business Logic
- Financial reconciliation
- Calculated fields
- Status progressions
- Business constraints
- KPI calculability

**Page 6-7**: Statistical Analysis
- Distribution analysis (histograms)
- Correlation matrix (heatmap)
- Outlier detection (box plots)
- Temporal patterns (line charts)

**Page 8**: Relationship Validation
- FK relationships
- Cardinality verification
- Join performance
- Sample join results

**Page 9**: Learning Objective Alignment
- Problem statement alignment
- Questions coverage
- Skill appropriateness
- Edge cases

**Page 10**: Intentional Issues
- Missing values
- Format inconsistencies
- Duplicates
- Outliers
- Learning objectives for each

**Page 11**: Final Recommendations
- Overall assessment
- Strengths
- Minor observations
- Approval recommendation
- Usage recommendations

### 9.4 UI Display

- Quality score badge
- Quick stats
- View/Download PDF report
- Approve/Regenerate buttons

---

## 10. Phase 5: Final Downloads

### 10.1 Complete ZIP Package

**File Name**: `[CompanyName]_Challenge_[Date].zip`

**Structure**:
```
[CompanyName]_Challenge_[Date].zip
│
├── datasets/
│   ├── dim_customers.csv (if normalized)
│   ├── dim_products.csv (if normalized)
│   ├── fact_sales.csv (if normalized)
│   └── dataset.csv (if denormalized)
│
├── documentation/
│   ├── Challenge_Document.pdf
│   ├── Data_Dictionary.csv
│   ├── Problem_Statement.txt
│   └── README.txt
│
├── quality_assurance/
│   ├── Data_Quality_Report.pdf (11 pages)
│   └── QA_Results.json
│
├── resources/
│   ├── Research_Sources.txt
│   ├── Schema_Diagram.png
│   └── Suggested_Visualizations.txt
│
└── metadata.json
```

### 10.2 File Contents

**Challenge_Document.pdf**: Professionally formatted problem statement, questions, characters

**Data_Dictionary.csv**: Detailed column descriptions with constraints

**Data_Quality_Report.pdf**: Full 11-page validation report

**Research_Sources.txt**: All sources with URLs and relevance notes

**Schema_Diagram.png**: Visual ER diagram (if normalized)

**README.txt**: Comprehensive usage guide (detailed)

**metadata.json**: Complete technical specifications

### 10.3 Separate Solution File

**File**: `[CompanyName]_Solution_Guide.pdf`

**Contents**:
- Approach guidance for each question
- Sample SQL queries
- Expected insights
- Visualization recommendations
- Business recommendations
- Learning resources

### 10.4 Download Success

Shows confirmation with:
- Package details
- Next steps
- Support links
- Options to create new or view history

---

## 11. Data Quality Validation Framework

### 11.1 SOP Compliance Mapping

| SOP Phase | App Phase | Implementation |
|-----------|-----------|----------------|
| Phase 1: Learning Objectives | Phase 0 | Configuration inputs |
| Phase 2: Business Entity | Phase 1 | Problem generation |
| Phase 3: Financial Flow | Phase 1 | Embedded in problem |
| Phase 4: Architecture | Phase 2 | Schema generation |
| Phase 5: Data Generation | Phase 3-4 | Preview & Full |
| Phase 6: Validation | Phase 4 | Quality report |

### 11.2 Validation Implementation

```python
def validate_dataset(dataset, schema, problem):
    """Comprehensive validation"""
    
    technical = validate_technical_integrity(dataset, schema)
    business = validate_business_logic(dataset, problem)
    statistical = analyze_statistics(dataset)
    relationships = validate_relationships(dataset, schema)
    learning = validate_learning_alignment(dataset, problem)
    
    score = calculate_overall_score(
        technical, business, statistical, 
        relationships, learning
    )
    
    return {
        'score': score,
        'technical': technical,
        'business': business,
        'statistical': statistical,
        'relationships': relationships,
        'learning': learning
    }
```

### 11.3 Intentional Issues

**Purpose**: Teach data cleaning skills

**Implementation**:
- Missing values (5%): Optional fields
- Format inconsistencies (2%): Date/phone formats
- Duplicates (1%): Partial matches
- Outliers (2-3%): Valid edge cases

All documented in quality report with learning objectives.

---

## 12. Chatbot System Specifications

### 12.1 Trigger Points

- Phase 1: Problem statement refinement
- Phase 2: Schema refinement
- Phase 3: Preview refinement
- Phase 4: Dataset regeneration

### 12.2 Chatbot Behavior

- **Context-aware**: Knows current phase and content
- **Clarifying**: Asks follow-up questions
- **Suggestive**: Offers 2-4 concrete options
- **Iterative**: Multi-turn conversations
- **Confirming**: Summarizes before regenerating

### 12.3 Sample Conversations

See detailed examples in sections 6.4, 7.4, 8.4, 9.5

### 12.4 Technical Implementation

**AI Prompt Template**:
```
You are a dataset regeneration assistant.

Context:
- Phase: {phase_name}
- Current Content: {content}
- Feedback History: {history}

Your role:
1. Ask clarifying questions
2. Provide specific options
3. Explain implications
4. Confirm understanding
5. Be concise

User Feedback: {user_message}
```

---

## 13. Progress Tracking & Visual Feedback

### 13.1 Phase Progress Indicator

Always visible at top showing:
- Current phase highlighted
- Completed phases with checkmarks
- Upcoming phases grayed out

### 13.2 Loading States

Detailed progress bars showing:
- Current stage
- Percentage complete
- Steps completed/remaining
- Time elapsed/estimated

### 13.3 Success Animations

- Green checkmark on approval
- Subtle confetti burst
- Smooth transitions
- Success toasts

---

## 14. Technical Implementation

### 14.1 Technology Stack

**Frontend**:
- React 18+ with hooks
- Inline styles
- Lucide-react for icons
- No localStorage

**Libraries**:
- JSZip: ZIP creation
- jsPDF: PDF generation
- matplotlib (backend): Charts
- Recharts: UI visualizations

**AI Integration**:
- Claude Sonnet 4 API
- Web search tool
- Multiple calls per workflow

**PDF Generation**:
- Backend Python service (recommended)
- Matplotlib for charts
- Professional formatting

### 14.2 Data Generation Engine

**Core Functions**:
```python
def generate_schema(problem, config)
def generate_preview_data(schema, size=30)
def generate_full_dataset(schema, size)
def validate_dataset(dataset, schema, problem)
def generate_quality_report_pdf(validation, dataset)
```

**Principles**:
- Parent-first generation
- Referential integrity
- Realistic distributions
- Event simulation
- Intentional issues

### 14.3 State Management

Global state with phases, content, UI state, chatbot state

### 14.4 API Call Structure

- Research → Problem → Schema → Preview → Full → Validation
- Chatbot: Multiple calls per phase
- Error handling with retries

---

## 15. Error Handling & Edge Cases

### 15.1 Error Categories

- User input errors
- API errors
- Data generation errors
- Quality validation errors

### 15.2 Error Messages

User-friendly with:
- Clear explanation
- What to try
- Action buttons

### 15.3 Fallback Mechanisms

- Research fails → Template-based
- PDF fails → JSON/HTML report
- Generation fails → Save progress

---

## 16. Performance Optimization

### 16.1 Target Timings

- Research: < 10s
- Problem: < 5s
- Schema: < 5s
- Preview: < 2s
- Full dataset (10K): < 30s
- Validation: < 10s
- PDF: < 5s

### 16.2 Strategies

- Parallel generation
- Streaming progress
- Batch processing
- Caching research

### 16.3 Memory Management

- Generate in batches
- Stream to files
- Compress before ZIP
- Clear intermediate data

---

## 17. Success Metrics & Analytics

### 17.1 Quality Metrics

- Average quality score
- First-attempt success rate
- Iterations per challenge

### 17.2 Usage Metrics

- Challenges created
- Popular domains/functions
- Average dataset size
- Download completion rate

### 17.3 Performance Metrics

- Generation time by phase
- API success rate
- Error frequency

---

## 18. Future Enhancements (Post-Phase 1)

### 18.1 Phase 2 Features

- Full research-assisted brief creation
- Enhanced chatbot with memory
- Interactive quality reports
- Advanced visualizations

### 18.2 Phase 3 Features

- Collaborative features
- Advanced data features (complex relationships)
- Integration & export (databases, cloud, BI tools)

### 18.3 Enterprise Features

- User management
- Advanced analytics
- A/B testing
- Recommendation engine

---

## 19. Documentation Requirements

### 19.1 User Documentation

- Getting started guide
- Reference documentation
- Video tutorials

### 19.2 Developer Documentation

- Architecture overview
- Setup guide
- Contribution guidelines

---

## 20. Acceptance Criteria Summary

### 20.1 Must Have (MVP)

**Phase 0**:
- ✅ Domain, function, skill, size, structure selection
- ✅ Complete problem context input

**Phase 1**:
- ✅ Real-time research with sources
- ✅ Problem statement with characters
- ✅ Approve/Regenerate with chatbot

**Phase 2**:
- ✅ OLTP schema generation
- ✅ Schema validation
- ✅ Approve/Regenerate with chatbot

**Phase 3**:
- ✅ Preview data (10-30 rows)
- ✅ Relationship visualization
- ✅ Approve/Regenerate with chatbot

**Phase 4**:
- ✅ Full dataset generation
- ✅ Comprehensive QA (SOP compliant)
- ✅ 11-page PDF with matplotlib charts
- ✅ Approve/Regenerate with chatbot

**Phase 5**:
- ✅ Complete ZIP with all files
- ✅ Separate solution file
- ✅ All downloads working

**Throughout**:
- ✅ Progress indicator always visible
- ✅ Character highlighting
- ✅ White background UI
- ✅ No localStorage
- ✅ Quality-gated workflow

---

## 21. Risk Mitigation

### 21.1 Technical Risks

- API rate limiting → Exponential backoff
- Memory issues → Batch processing
- PDF generation fails → JSON fallback

### 21.2 UX Risks

- Long wait times → Detailed progress
- Unclear chatbot → Specific options
- Complex reports → Executive summary first

### 21.3 Data Quality Risks

- Data doesn't match problem → Iterative validation
- FK violations → Auto-fix or notify
- Unrealistic distributions → Research-based parameters

---

## 22. Glossary

**OLTP**: Online Transaction Processing (normalized data)  
**Denormalized**: Single flat table  
**Normalized**: Multiple related tables  
**Foreign Key**: Column linking to another table  
**Referential Integrity**: All FKs point to existing records  
**KPI**: Key Performance Indicator  
**SOP**: Standard Operating Procedure  
**Quality Score**: Automated assessment (1-10)  
**Edge Case**: Unusual but valid scenarios for learning  
**Intentional Issue**: Planned data quality problem for teaching

---

## 23. Appendix: Sample Workflow

### Complete Example: E-Commerce Challenge

**Phase 0: Configuration**
- Domain: E-Commerce
- Function: Sales & Marketing
- Skill: Intermediate
- Size: 10,000 rows
- Structure: Normalized

**Phase 1: Problem** (approved after research)
- Title: "Reversing the Retention Crisis at ShopSphere"
- Company: ShopSphere
- Problem: Repeat purchase rate declined 45% → 28%
- 6 questions generated
- 5 research sources attributed

**Phase 2: Schema** (approved after adding demographics)
- 3 tables: dim_customers, dim_products, fact_orders
- 22 total columns
- All relationships validated

**Phase 3: Preview** (approved after date distribution fix)
- 65 preview rows across 3 tables
- Realistic patterns confirmed
- Relationships working

**Phase 4: Quality** (approved - score 9.3/10)
- Full dataset generated (11,500 rows)
- Quality report: 11 pages with charts
- All validations passed

**Phase 5: Downloads**
- ZIP: 8.5 MB with all files
- Solution guide: 2.1 MB

**Total Time**: ~8 minutes (including user review)

---

**END OF PRD**

---

**Next Steps:**
1. Development environment setup
2. Phase 0-1 implementation
3. Quality report PDF generation system
4. Phase 2-4 implementation
5. Chatbot integration
6. User acceptance testing
7. Production deployment

