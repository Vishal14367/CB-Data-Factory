"""
AI-driven schema generation using Groq API.
"""
import json
import logging
from typing import Dict, Any
from groq import Groq

from config import GROQ_API_KEY, AI_MODEL, DIFFICULTY_CONFIG, DENORMALIZED_TABLES
from models import (
    ChallengeInput, Schema, TableDefinition, ColumnDefinition,
    ForeignKeyDefinition, BusinessRule, KPIDefinition, EventImpact
)

logger = logging.getLogger(__name__)


class SchemaGenerator:
    """Generate database schema from problem description using AI."""

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def generate(self, input_data: ChallengeInput) -> Schema:
        """
        Generate complete database schema from user input.

        Args:
            input_data: User's challenge configuration

        Returns:
            Complete schema with tables, relationships, rules, KPIs
        """
        logger.info(f"Generating schema for: {input_data.domain} - {input_data.function}")

        prompt = self._build_prompt(input_data)

        try:
            response = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=8000,
                response_format={"type": "json_object"}
            )

            schema_json = json.loads(response.choices[0].message.content)
            logger.info("Schema generated successfully")

            # Parse and validate schema
            schema = self._parse_schema(schema_json)
            return schema

        except Exception as e:
            logger.error(f"Schema generation failed: {e}")
            raise

    def _get_system_prompt(self) -> str:
        """System prompt defining AI's role and constraints."""
        return """You are a database schema architect for educational datasets.

Your role:
1. Design realistic OLTP database schemas for business analytics training
2. Ensure schemas support the problem statement and learning objectives
3. Follow normalization principles for multi-table designs
4. Define business rules, KPIs, and event impacts
5. Use ONLY fictional company names, addresses, emails (never real ones)

Output MUST be valid JSON matching this structure:
{
  "tables": [...],
  "relationships": [...],
  "business_rules": [...],
  "kpis": [...],
  "event_impacts": [...],
  "date_range_start": "2019-01-01",
  "date_range_end": "2024-12-31"
}

Constraints:
- Use prefixed IDs (CUST0001, TXN0001, PROD0001 format)
- All foreign keys must reference existing tables/columns
- Status transitions must be logical
- Financial calculations must balance
- KPI formulas must be computable from defined columns
- Event impacts should reflect realistic historical events (COVID, seasonal changes)
"""

    def _build_prompt(self, input_data: ChallengeInput) -> str:
        """Build specific prompt from user input."""

        diff_config = DIFFICULTY_CONFIG[input_data.difficulty.value]
        column_count = diff_config["columns"]
        
        if input_data.data_structure.value == "Normalized":
            table_count = diff_config["normalized_tables"]
            structure_guidance = f"""
Create {table_count} related tables:
- Dimension tables (master data): customers, products, employees, locations, etc.
- Fact table: transactions, orders, events, etc.
- Total columns across all tables: ~{column_count}
- Proper parent-child relationships with foreign keys
"""
        else:
            structure_guidance = f"""
Create 1 denormalized table with all columns in a flat structure.
- Total columns: ~{column_count}
- No foreign keys (all data in one table)
"""

        prompt = f"""
Generate a complete database schema for this data challenge:

**Domain:** {input_data.domain}
**Function:** {input_data.function}
**Skill Level:** {input_data.difficulty.value}
**Dataset Size:** {input_data.dataset_size:,} rows
**Structure:** {input_data.data_structure.value}

**Problem Statement:**
{input_data.problem_statement}

**Primary Business Questions:**
{input_data.primary_questions or "Not specified"}

**Structure Requirements:**
{structure_guidance}

**Instructions:**
1. Design tables that support both the problem statement AND help answer the primary business questions
2. Define columns with appropriate data types:
   - Use prefixed IDs (e.g., CUST0001, TXN0001)
   - Include realistic constraints (min/max, allowed values)
   - Mark nullable vs required fields
3. Define foreign key relationships (parent-child order)
4. Define business rules:
   - Status transitions (if applicable)
   - Calculated fields (e.g., total = quantity * price)
   - Financial constraints (e.g., refund <= payment)
5. Define 4-6 KPIs that directly address the business problem and questions
6. Define 1-2 event impacts (e.g., COVID-19 impact in 2020)

**Table Definition Format:**
{{
  "name": "dim_customers",
  "description": "Customer master data",
  "source_system": "CRM",
  "columns": [
    {{
      "name": "customer_id",
      "datatype": "string",
      "nullable": false,
      "description": "Unique customer identifier",
      "id_prefix": "CUST",
      "constraints": {{"format": "CUST####"}}
    }},
    {{
      "name": "customer_name",
      "datatype": "string",
      "nullable": false,
      "description": "Customer full name",
      "constraints": {{"min_length": 3, "max_length": 100}}
    }},
    {{
      "name": "region",
      "datatype": "category",
      "nullable": false,
      "description": "Geographic region",
      "allowed_values": ["North", "South", "East", "West"]
    }}
  ],
  "primary_key": "customer_id"
}}

**Foreign Key Format:**
{{
  "parent_table": "dim_customers",
  "parent_column": "customer_id",
  "child_table": "fact_orders",
  "child_column": "customer_id",
  "cardinality": "1:N"
}}

**Business Rule Format:**
{{
  "rule_type": "status_transition",
  "description": "Order status flow",
  "parameters": {{
    "transitions": [
      ["Pending", "Confirmed"],
      ["Confirmed", "Shipped"],
      ["Shipped", "Delivered"],
      ["Pending", "Cancelled"],
      ["Confirmed", "Cancelled"]
    ]
  }}
}}

**KPI Format:**
{{
  "name": "Customer Retention Rate",
  "formula": "repeat_customers / total_customers * 100",
  "expected_trend": "decline",
  "narrative_percentage": 35.0
}}

**Event Impact Format:**
{{
  "event_name": "COVID-19 Pandemic",
  "start_date": "2020-03-01",
  "end_date": "2020-12-31",
  "impact_magnitude": -0.30,
  "affected_metrics": ["revenue", "order_count"]
}}

Generate the complete schema now.
"""
        return prompt

    def _parse_schema(self, schema_json: Dict[str, Any]) -> Schema:
        """Parse and validate JSON schema into Pydantic models."""

        # Parse tables
        tables = [
            TableDefinition(
                name=t["name"],
                description=t["description"],
                source_system=t.get("source_system"),
                columns=[
                    ColumnDefinition(
                        name=c["name"],
                        datatype=c["datatype"],
                        nullable=c.get("nullable", True),
                        description=c.get("description", ""),
                        constraints=c.get("constraints"),
                        id_prefix=c.get("id_prefix"),
                        allowed_values=c.get("allowed_values")
                    )
                    for c in t["columns"]
                ],
                primary_key=t["primary_key"],
                parent_table=t.get("parent_table")
            )
            for t in schema_json["tables"]
        ]

        # Parse relationships
        relationships = [
            ForeignKeyDefinition(**r)
            for r in schema_json.get("relationships", [])
        ]

        # Parse business rules
        business_rules = [
            BusinessRule(**br)
            for br in schema_json.get("business_rules", [])
        ]

        # Parse KPIs
        kpis = [
            KPIDefinition(**kpi)
            for kpi in schema_json.get("kpis", [])
        ]

        # Parse event impacts
        event_impacts = [
            EventImpact(**ei)
            for ei in schema_json.get("event_impacts", [])
        ]

        schema = Schema(
            tables=tables,
            relationships=relationships,
            business_rules=business_rules,
            kpis=kpis,
            date_range_start=schema_json.get("date_range_start", "2019-01-01"),
            date_range_end=schema_json.get("date_range_end", "2024-12-31"),
            event_impacts=event_impacts
        )

        # Validate schema
        self._validate_schema(schema)

        return schema

    def _validate_schema(self, schema: Schema):
        """Validate schema integrity."""

        table_names = {t.name for t in schema.tables}

        # Validate foreign key references
        for fk in schema.relationships:
            if fk.parent_table not in table_names:
                raise ValueError(f"FK parent table '{fk.parent_table}' not found")
            if fk.child_table not in table_names:
                raise ValueError(f"FK child table '{fk.child_table}' not found")

        # Validate primary keys exist
        for table in schema.tables:
            pk_columns = [c.name for c in table.columns]
            if table.primary_key not in pk_columns:
                raise ValueError(f"Primary key '{table.primary_key}' not in columns for table '{table.name}'")

        logger.info("Schema validation passed")
