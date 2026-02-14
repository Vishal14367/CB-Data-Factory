# Phase 2 Architecture Plan: Data Schema Generation & Validation
**Status:** PLANNING
**Target:** Next Development Cycle
**Depends on:** Phase 1 ✅ COMPLETE

---

## Overview

Phase 2 builds on Phase 1's approved problem statement to generate a validated database schema that:
- Supports all analytical questions from Phase 1
- Follows OLTP normalization principles
- Includes proper foreign key relationships
- Defines business rules and KPIs
- Is visualized as an Entity Relationship Diagram (ERD)

---

## Architecture Components

### Backend Components

#### 1. Schema Generation Module (NEW)
**File:** `backend/src/schema_generator.py` (UPDATE existing)

**New Methods:**
```python
class SchemaGenerator:
    def generate_from_problem(
        self,
        problem_statement: ProblemStatement,
        input_data: ChallengeInput,
        skill_level: SkillLevel
    ) -> Schema:
        """Generate OLTP schema from approved problem statement."""

    def validate_schema(
        self,
        schema: Schema,
        problem_statement: ProblemStatement
    ) -> SchemaValidationResult:
        """Validate schema answers all questions and supports KPIs."""
```

**Responsibilities:**
- Parse problem statement to extract entities
- Generate appropriate tables (dimensions + fact table)
- Define columns with correct data types
- Create foreign key relationships
- Define business rules from problem context
- Validate schema completeness

#### 2. ERD (Entity Relationship Diagram) Generator (NEW)
**File:** `backend/src/erd_generator.py` (NEW)

**Methods:**
```python
class ERDGenerator:
    def generate_diagram(self, schema: Schema) -> str:
        """Generate ERD as SVG or image."""

    def create_metadata(self, schema: Schema) -> Dict:
        """Create metadata for frontend visualization."""
```

**Responsibilities:**
- Create visual representation of schema
- Show table relationships (1:1, 1:N, M:N)
- Display primary keys and foreign keys
- Generate SVG/PNG for PDF report

#### 3. Models Update (UPDATE)
**File:** `backend/src/models.py`

**New Models:**
```python
class SchemaValidationCheck(BaseModel):
    check_name: str
    category: str  # "answerability", "completeness", "relationships", "normalization"
    passed: bool
    score: float = Field(ge=0.0, le=10.0)
    message: str

class SchemaValidationResult(BaseModel):
    schema_id: str
    overall_score: float = Field(ge=0.0, le=10.0)
    validation_checks: List[SchemaValidationCheck]
    status: Literal["valid", "needs_revision", "invalid"]
    issues: List[str]
    suggestions: List[str]

class Phase2Response(BaseModel):
    session_id: str
    phase: str = "phase2"
    status: Literal["pending_approval", "approved", "failed"]
    schema: Optional[Schema] = None
    validation: Optional[SchemaValidationResult] = None
    erd_svg: Optional[str] = None  # SVG representation
    approval_timestamp: Optional[datetime] = None
```

#### 4. API Endpoints (UPDATE main.py)

```python
# Phase 2A: Generate Schema
@app.post("/api/challenge/phase2/generate-schema")
async def phase2_generate_schema(
    session_id: str,
    input_data: ChallengeInput
) -> Dict:
    """Generate OLTP schema from approved problem statement."""
    # 1. Retrieve problem statement from session
    # 2. Generate schema using AI
    # 3. Generate ERD visualization
    # 4. Store in session
    # 5. Return schema with ERD

# Phase 2B: Validate Schema
@app.post("/api/challenge/phase2/validate-schema")
async def phase2_validate_schema(
    session_id: str
) -> Dict:
    """Run validation checks on generated schema."""
    # 1. Check all questions answerable
    # 2. Check all KPIs calculable
    # 3. Check normalization
    # 4. Check relationships
    # 5. Return validation result with score

# Phase 2C: Approve Schema
@app.post("/api/challenge/phase2/approve")
async def phase2_approve(session_id: str) -> Dict:
    """Approve schema and unlock Phase 3."""

# Phase 2 Status
@app.get("/api/challenge/phase2/status/{session_id}")
async def phase2_status(session_id: str) -> Dict:
    """Get current Phase 2 status."""
```

### Frontend Components

#### 1. Phase 2 UI Component
**File:** `frontend_new/src/app/page.tsx` (UPDATE)

**Phase 2 Section:**
```tsx
interface SchemaData {
  tables: Table[];
  relationships: Relationship[];
  business_rules: BusinessRule[];
  kpis: KPI[];
  validation: ValidationResult;
}

<Phase2Component
  schema={schema}
  validation={validation}
  erdSvg={erdSvg}
  onApprove={handleApproveSchema}
  onRegenerate={handleRegenerateSchema}
/>
```

#### 2. ERD Visualization Component (NEW)
**File:** `frontend_new/src/components/ERDViewer.tsx` (NEW)

**Features:**
- Interactive display of tables and relationships
- Color-coded table types (dimension/fact)
- Zoomable/pannable interface
- Show/hide foreign keys
- Table detail expansion
- Column listing with types

**Implementation:**
```tsx
interface ERDViewerProps {
  schema: Schema;
  erdSvg: string;  // SVG from backend
  onTableClick?: (table: string) => void;
}

export function ERDViewer({ schema, erdSvg, onTableClick }: ERDViewerProps) {
  // Render interactive ERD
  // Allow clicking tables to see details
  // Highlight relationships
}
```

#### 3. Schema Details Component (NEW)
**File:** `frontend_new/src/components/SchemaDetails.tsx` (NEW)

**Expandable Sections:**
- Tables (sortable list with columns)
- Relationships (1:1, 1:N, M:N visual indicators)
- Business Rules (if applicable)
- KPIs (calculated fields)
- Validation Results (pass/fail indicators)

### UI Flow for Phase 2

```
Phase 2: Schema Generation
├─ Show approved problem statement summary
├─ Show "Generating schema..." loading state
│  ├─ Creates OLTP tables
│  ├─ Defines relationships
│  ├─ Validates completeness
│  └─ Generates ERD
├─ Display Schema Section:
│  ├─ ERD Visualization (interactive)
│  ├─ Expandable Table Details
│  │  ├─ Table Name
│  │  ├─ Columns (name, type, nullable, constraints)
│  │  ├─ Primary Key
│  │  └─ Foreign Keys
│  ├─ Relationships Section
│  │  ├─ Shows all FK relationships
│  │  ├─ Cardinality indicators (1:1, 1:N)
│  │  └─ Visual relationship map
│  └─ Validation Results
│     ├─ Score badge (0-10)
│     ├─ Check results (✓/✗)
│     ├─ Issues list
│     └─ Suggestions
├─ Action Buttons:
│  ├─ "Regenerate" (with feedback chatbot)
│  └─ "Approve & Continue" (to Phase 3)
└─ (On Reject/Regenerate)
   ├─ Open Chatbot
   ├─ Collect feedback
   └─ Regenerate with improvements
```

---

## Implementation Details

### Schema Generation Logic

#### Step 1: Entity Identification
From problem statement, identify:
- **Dimension Entities** (master data):
  - Customers/Users
  - Products
  - Employees
  - Locations
  - Time (if temporal)

- **Fact Entities** (transactions/events):
  - Orders/Sales
  - Interactions
  - Events
  - Metrics

#### Step 2: Column Definition
For each entity, create columns:
```python
{
  "entity": "customers",
  "columns": [
    {
      "name": "customer_id",
      "type": "VARCHAR(20)",  # CUST0001 format
      "nullable": False,
      "constraints": {"primary_key": True, "unique": True},
      "description": "Unique customer identifier"
    },
    {
      "name": "customer_name",
      "type": "VARCHAR(100)",
      "nullable": False,
      "description": "Full name of customer"
    },
    {
      "name": "email",
      "type": "VARCHAR(100)",
      "nullable": False,
      "constraints": {"unique": True},
      "description": "Email address"
    },
    ...
  ]
}
```

#### Step 3: Relationship Definition
Create foreign keys connecting dimensions to facts:
```python
{
  "parent_table": "customers",
  "parent_column": "customer_id",
  "child_table": "orders",
  "child_column": "customer_id",
  "cardinality": "1:N",
  "constraint_name": "fk_orders_customer"
}
```

#### Step 4: Business Rules
Define constraints and logic:
```python
{
  "rule_type": "status_transition",
  "description": "Order status must follow valid transitions",
  "parameters": {
    "table": "orders",
    "column": "status",
    "valid_transitions": {
      "pending": ["processing", "cancelled"],
      "processing": ["completed", "cancelled"],
      "completed": [],
      "cancelled": []
    }
  }
}
```

#### Step 5: KPI Definition
Define calculated metrics:
```python
{
  "name": "Customer Lifetime Value",
  "formula": "SUM(order_amount) WHERE customer_id = X",
  "expected_trend": "growth",
  "description": "Total revenue from each customer"
}
```

### Validation Checks

#### Check 1: Answerability
- For each analytical question from Phase 1:
  - Can it be answered with the generated schema?
  - Are all required tables present?
  - Are all required columns present?
  - Score: 0-10 based on % of questions answerable

#### Check 2: Completeness
- All entities identified from problem have tables
- All required calculations have supporting columns
- All business processes represented
- Score: 0-10 based on coverage

#### Check 3: Normalization
- Denormalized columns eliminated (where appropriate)
- No unnecessary duplication
- Proper primary/foreign key setup
- Score: 0-10 based on normalization level

#### Check 4: Relationships
- All foreign keys point to valid columns
- No orphaned foreign keys
- Cardinality matches business logic
- Score: 0-10 based on relationship integrity

#### Check 5: Learning Alignment
- Complexity matches skill level
- Schema supports the intended learning
- Appropriate number of joins required
- Score: 0-10 based on alignment

**Overall Score:** Weighted average of all checks (40% answerability, 30% completeness, 20% normalization, 10% learning alignment)

---

## Data Flow

```
Phase 1: Problem Statement (Approved)
    ↓
Phase 2A: Generate Schema
    ├─ Parse problem text
    ├─ Identify entities
    ├─ Define columns/types
    ├─ Create relationships
    └─ Generate ERD
    ↓
Phase 2B: Validate Schema
    ├─ Check answerability
    ├─ Check completeness
    ├─ Check normalization
    ├─ Check relationships
    └─ Calculate score
    ↓
Display Schema with:
    ├─ Interactive ERD
    ├─ Table details
    ├─ Validation results
    ├─ Issues & suggestions
    └─ Approve/Regenerate buttons
    ↓
[User Reviews & Decides]
    ↓
    ├─ Approve → Phase 3 (Preview)
    └─ Regenerate → Chatbot Feedback → Phase 2A
```

---

## Sample Schema Output

### Example: E-Commerce Challenge

**Tables:**
```
1. dim_customers (20 columns)
   - customer_id (PK)
   - name, email, address, signup_date
   - segment, lifecycle_stage, total_orders

2. dim_products (15 columns)
   - product_id (PK)
   - name, category, price, cost
   - manufacturer, sku, in_stock

3. dim_dates (4 columns)
   - date_id (PK)
   - full_date, month, year, quarter

4. fact_orders (18 columns)
   - order_id (PK)
   - customer_id (FK)
   - product_id (FK)
   - order_date, quantity, unit_price, total_amount
   - status, payment_method, shipping_address
```

**Relationships:**
```
fact_orders → dim_customers (N:1)
fact_orders → dim_products (N:1)
fact_orders → dim_dates (N:1)
```

**KPIs:**
```
1. Customer Acquisition Cost = Total Marketing Spend / New Customers
2. Repeat Purchase Rate = Customers with 2+ orders / Total Customers
3. Average Order Value = Total Revenue / Total Orders
4. Customer Lifetime Value = Total Revenue per Customer (avg)
```

**Validation Score: 8.5/10**
```
✓ Answerability: 9/10 (6/6 questions can be answered)
✓ Completeness: 9/10 (all entities covered)
✓ Normalization: 8/10 (proper OLTP structure)
✓ Relationships: 8/10 (all FKs valid)
✓ Learning Alignment: 8/10 (Intermediate level appropriate)
```

---

## API Response Examples

### Phase 2A: Generate Schema Response
```json
{
  "session_id": "uuid",
  "status": "schema_generated",
  "schema": {
    "tables": [
      {
        "name": "dim_customers",
        "description": "Customer master data",
        "columns": [...],
        "primary_key": "customer_id"
      }
    ],
    "relationships": [
      {
        "parent_table": "dim_customers",
        "child_table": "fact_orders",
        "parent_column": "customer_id",
        "child_column": "customer_id",
        "cardinality": "1:N"
      }
    ]
  },
  "erd_svg": "<svg>...</svg>",
  "message": "Schema generated with 4 tables and 3 relationships"
}
```

### Phase 2B: Validation Response
```json
{
  "session_id": "uuid",
  "status": "schema_validated",
  "validation": {
    "overall_score": 8.5,
    "status": "valid",
    "checks": [
      {
        "check_name": "Answerability",
        "category": "answerability",
        "passed": true,
        "score": 9.0,
        "message": "6/6 questions can be answered with this schema"
      },
      ...
    ],
    "issues": [],
    "suggestions": [
      "Consider adding order_timestamp for time-series analysis"
    ]
  }
}
```

---

## Timeline & Dependencies

### Prerequisites
- ✅ Phase 1: Problem Statement (COMPLETE)
- ✅ Models in place (COMPLETE)

### Phase 2 Development Steps
1. Update `models.py` with schema validation models
2. Create/update `schema_generator.py` with generation logic
3. Create `erd_generator.py` for visualization
4. Update `main.py` with Phase 2 endpoints
5. Create `ERDViewer.tsx` component
6. Create `SchemaDetails.tsx` component
7. Update `page.tsx` to include Phase 2
8. Integration testing
9. User acceptance testing

### Estimated Effort
- Backend: 2-3 days
- Frontend: 2-3 days
- Testing: 1-2 days
- **Total: 5-8 days**

---

## Success Criteria

Phase 2 is complete when:

- ✅ Schema generation produces valid OLTP structures
- ✅ All analytical questions from Phase 1 are answerable
- ✅ Validation score >= 7.5/10 for approval
- ✅ ERD visualization accurate and interactive
- ✅ Can approve schema and proceed to Phase 3
- ✅ Can regenerate with feedback
- ✅ E2E test from Phase 0 → Phase 2 approval

---

## Known Future Challenges

1. **Complex Entity Extraction**
   - Problem statements can be ambiguous
   - AI may miss implicit entities
   - Mitigation: Allow manual schema editing

2. **Relationship Complexity**
   - M:N relationships require junction tables
   - Circular dependencies possible
   - Mitigation: Validation catches most issues

3. **KPI Calculability**
   - Some KPIs may require data not in schema
   - Mitigation: Suggest columns to add

4. **Normalization vs Practicality**
   - Over-normalization makes generation slow
   - Under-normalization defeats learning
   - Mitigation: Tuning based on skill level

---

## Integration with Existing Code

### Reuse from Phase 1
- ✅ Session management (sessions dict)
- ✅ Error handling patterns
- ✅ Logging setup
- ✅ Groq/Claude API patterns
- ✅ Frontend UI patterns

### Potential Conflicts
- Schema generation already exists in `schema_generator.py`
- May need to refactor existing code
- Existing schema takes `ChallengeInput`, new version takes `ProblemStatement`

---

## Next Steps

When ready to implement Phase 2:

1. **Review this architecture document**
2. **Create detailed task breakdown**
3. **Start with backend schema generator**
4. **Build validation system**
5. **Create frontend visualization**
6. **Comprehensive testing**

---

**END OF PHASE 2 ARCHITECTURE**

*For detailed Phase 1 implementation, see [PHASE1_IMPLEMENTATION.md](PHASE1_IMPLEMENTATION.md)*
