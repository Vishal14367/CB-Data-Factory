"""
Quick test script for schema generation.
Run this to verify Groq API is working and schema generation is functional.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models import ChallengeInput, SkillLevel, DataStructure
from schema_generator import SchemaGenerator
import json


def test_schema_generation():
    """Test schema generation with a sample problem."""

    # Sample input
    input_data = ChallengeInput(
        domain="E-Commerce",
        function="Sales & Marketing",
        problem_statement="""
An online retail company is experiencing declining customer retention rates.
Over the past 3 years (2019-2024), repeat purchase rates have dropped from 45% to 28%.
The company needs to analyze customer behavior, purchase patterns, and product performance
to identify the root causes and develop targeted retention strategies.

Key questions to answer:
1. What customer segments have the highest churn rates?
2. Which product categories drive repeat purchases?
3. How does purchase frequency vary by customer demographics?
4. What is the impact of discounts on customer loyalty?
5. Are there seasonal patterns in customer retention?
6. Which marketing channels yield the most loyal customers?
        """,
        skill_level=SkillLevel.INTERMEDIATE,
        dataset_size=10000,
        data_structure=DataStructure.NORMALIZED
    )

    print("=" * 80)
    print("SCHEMA GENERATION TEST")
    print("=" * 80)
    print(f"Domain: {input_data.domain}")
    print(f"Function: {input_data.function}")
    print(f"Skill Level: {input_data.skill_level.value}")
    print(f"Structure: {input_data.data_structure.value}")
    print()

    # Generate schema
    print("Generating schema with Groq AI...")
    generator = SchemaGenerator()
    schema = generator.generate(input_data)

    print("\n" + "=" * 80)
    print("SCHEMA GENERATED SUCCESSFULLY!")
    print("=" * 80)

    print(f"\nTables: {len(schema.tables)}")
    for table in schema.tables:
        print(f"  - {table.name}: {len(table.columns)} columns, PK={table.primary_key}")

    print(f"\nRelationships: {len(schema.relationships)}")
    for rel in schema.relationships:
        print(f"  - {rel.child_table}.{rel.child_column} -> {rel.parent_table}.{rel.parent_column} ({rel.cardinality})")

    print(f"\nBusiness Rules: {len(schema.business_rules)}")
    for rule in schema.business_rules:
        print(f"  - {rule.rule_type}: {rule.description}")

    print(f"\nKPIs: {len(schema.kpis)}")
    for kpi in schema.kpis:
        print(f"  - {kpi.name}: {kpi.expected_trend}")

    print(f"\nEvent Impacts: {len(schema.event_impacts)}")
    for event in schema.event_impacts:
        print(f"  - {event.event_name} ({event.start_date} to {event.end_date}): {event.impact_magnitude}%")

    # Save to file
    output_file = Path(__file__).parent / "output" / "test_schema.json"
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(schema.model_dump(), f, indent=2)

    print(f"\n✅ Schema saved to: {output_file}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_schema_generation()
