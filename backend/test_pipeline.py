
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

import pandas as pd
import numpy as np
from dataset_generator import DatasetGenerator
from quality_validator import QualityValidator
from pdf_generator import QualityReportPDF
from models import ChallengeInput, Difficulty, DataStructure, Schema
from schema_generator import SchemaGenerator
import json

def test_pipeline():
    # Mock input
    input_data = ChallengeInput(
        domain="E-Commerce",
        function="Sales",
        problem_statement="A major retail struggle with customer retention issues. We need to analyze 35% decline in sales over 2023. Peter Pandey is the analyst, Tony Sharma is the VP, and Bruce Hariyali is the owner.",
        difficulty=Difficulty.MEDIUM,
        dataset_size=1000,
        data_structure=DataStructure.NORMALIZED
    )
    
    # Normally this calls AI, but let's see if imports and basic class init work
    print("Testing class initializations...")
    gen = DatasetGenerator(seed=42)
    val = QualityValidator("test_session")
    
    # We need a schema to test data gen
    # I'll provide a minimal hardcoded schema to test the engine without AI
    print("Creating mock schema...")
    from models import TableDefinition, ColumnDefinition, ForeignKeyDefinition, BusinessRule, KPIDefinition, EventImpact
    
    customers = TableDefinition(
        name="dim_customers",
        description="Customers",
        columns=[
            ColumnDefinition(name="customer_id", datatype="string", id_prefix="CUST"),
            ColumnDefinition(name="customer_name", datatype="string"),
            ColumnDefinition(name="region", datatype="category", allowed_values=["North", "South", "East", "West"]),
            ColumnDefinition(name="is_active", datatype="boolean")
        ],
        primary_key="customer_id"
    )
    
    products = TableDefinition(
        name="dim_products",
        description="Products",
        columns=[
            ColumnDefinition(name="product_id", datatype="string", id_prefix="PROD"),
            ColumnDefinition(name="product_name", datatype="string"),
            ColumnDefinition(name="category", datatype="category", allowed_values=["Electronics", "Home", "Fashion"]),
            ColumnDefinition(name="price", datatype="float", constraints={"min": 5, "max": 500})
        ],
        primary_key="product_id"
    )

    sales = TableDefinition(
        name="fact_sales",
        description="Sales",
        columns=[
            ColumnDefinition(name="sale_id", datatype="string", id_prefix="SALE"),
            ColumnDefinition(name="customer_id", datatype="string"),
            ColumnDefinition(name="product_id", datatype="string"),
            ColumnDefinition(name="quantity", datatype="integer", constraints={"min": 1, "max": 10}),
            ColumnDefinition(name="amount", datatype="float"),
            ColumnDefinition(name="sale_date", datatype="date")
        ],
        primary_key="sale_id"
    )
    
    schema = Schema(
        tables=[customers, products, sales],
        relationships=[
            ForeignKeyDefinition(parent_table="dim_customers", parent_column="customer_id", child_table="fact_sales", child_column="customer_id"),
            ForeignKeyDefinition(parent_table="dim_products", parent_column="product_id", child_table="fact_sales", child_column="product_id")
        ],
        business_rules=[],
        kpis=[],
        event_impacts=[]
    )
    
    print("Generating data...")
    data = gen.generate(schema, 100)
    
    print("Validating data...")
    results = val.validate(schema, data, input_data)
    print(f"Status: {results.status}, Score: {results.overall_score}")
    
    print("Generating PDF...")
    pdf_path = Path("test_report.pdf")
    pdf_gen = QualityReportPDF(pdf_path)
    pdf_gen.generate(results, schema, data, input_data)
    print(f"PDF generated: {pdf_path.exists()}")

if __name__ == "__main__":
    try:
        test_pipeline()
        print("Test passed successfully!")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
