"""
Simple Demo - Data Challenge Generator
No installation required (except Python)

Just run: python demo_simple.py
"""

import json
import os
from datetime import datetime, timedelta
import random

# Check if required packages are installed, if not, install them
def install_required_packages():
    """Install required packages if not present."""
    required = {
        'groq': 'groq',
        'faker': 'faker',
        'pandas': 'pandas',
    }

    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"Installing required packages: {', '.join(missing)}")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing, '--quiet'])
        print("✅ Packages installed!\n")

# Install packages first
install_required_packages()

# Now import them
from groq import Groq
from faker import Faker
import pandas as pd

# Configuration
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"  # Replace with your actual Groq API key
AI_MODEL = "llama-3.3-70b-versatile"


class SimpleDataGenerator:
    """Simplified data generator for demo purposes."""

    def __init__(self):
        self.fake = Faker()
        Faker.seed(42)
        random.seed(42)

    def generate_schema(self, domain, function, problem_statement):
        """Generate schema using Groq AI."""
        print("\n📋 Generating database schema with AI...")

        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""Generate a simple database schema for this problem:

Domain: {domain}
Function: {function}
Problem: {problem_statement}

Create a normalized schema with 3-4 tables for intermediate skill level.

Return ONLY valid JSON in this format:
{{
  "tables": [
    {{
      "name": "dim_customers",
      "columns": [
        {{"name": "customer_id", "type": "string", "is_pk": true}},
        {{"name": "customer_name", "type": "string"}},
        {{"name": "region", "type": "category", "values": ["North", "South", "East", "West"]}}
      ]
    }},
    {{
      "name": "fact_orders",
      "columns": [
        {{"name": "order_id", "type": "string", "is_pk": true}},
        {{"name": "customer_id", "type": "foreign_key", "references": "dim_customers"}},
        {{"name": "order_date", "type": "date"}},
        {{"name": "revenue", "type": "float", "min": 10, "max": 5000}}
      ]
    }}
  ]
}}"""

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "You are a database schema designer. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        schema = json.loads(response.choices[0].message.content)
        print(f"✅ Generated {len(schema['tables'])} tables")
        return schema

    def generate_data(self, schema, num_rows=1000):
        """Generate realistic data from schema."""
        print(f"\n📊 Generating {num_rows:,} rows of data...")

        datasets = {}

        # Generate each table
        for table in schema['tables']:
            table_name = table['name']
            print(f"  - Generating {table_name}...")

            # Determine row count (dimension tables get fewer rows)
            if table_name.startswith('dim_'):
                rows = min(num_rows // 10, 500)
            else:
                rows = num_rows

            data = {}

            # Generate each column
            for col in table['columns']:
                col_name = col['name']
                col_type = col['type']

                if col.get('is_pk'):
                    # Primary key
                    prefix = table_name[:4].upper()
                    data[col_name] = [f"{prefix}{i:04d}" for i in range(1, rows + 1)]

                elif col_type == 'foreign_key':
                    # Foreign key - reference parent table
                    parent_table = col['references']
                    if parent_table in datasets:
                        parent_pks = datasets[parent_table].iloc[:, 0].tolist()
                        data[col_name] = [random.choice(parent_pks) for _ in range(rows)]
                    else:
                        data[col_name] = [f"{parent_table[:4].upper()}{random.randint(1, 100):04d}" for _ in range(rows)]

                elif col_type == 'string':
                    data[col_name] = [self.fake.name() for _ in range(rows)]

                elif col_type == 'category':
                    values = col.get('values', ['A', 'B', 'C'])
                    # Not uniform - weighted distribution
                    weights = [0.4, 0.3, 0.2] + [0.1] * (len(values) - 3)
                    data[col_name] = random.choices(values, weights=weights[:len(values)], k=rows)

                elif col_type == 'date':
                    start_date = datetime(2019, 1, 1)
                    end_date = datetime(2024, 12, 31)
                    date_range = (end_date - start_date).days
                    data[col_name] = [(start_date + timedelta(days=random.randint(0, date_range))).strftime('%Y-%m-%d') for _ in range(rows)]

                elif col_type == 'float':
                    min_val = col.get('min', 0)
                    max_val = col.get('max', 1000)
                    # Normal distribution with outliers
                    mean = (min_val + max_val) / 2
                    std = (max_val - min_val) / 6
                    values = [random.gauss(mean, std) for _ in range(rows)]
                    # Add 5% outliers
                    outlier_count = int(rows * 0.05)
                    for _ in range(outlier_count):
                        idx = random.randint(0, rows - 1)
                        values[idx] = random.uniform(max_val * 2, max_val * 5)
                    data[col_name] = [round(max(min_val, min(v, max_val * 5)), 2) for v in values]

                elif col_type == 'int':
                    min_val = col.get('min', 1)
                    max_val = col.get('max', 100)
                    data[col_name] = [random.randint(min_val, max_val) for _ in range(rows)]

            # Create DataFrame
            df = pd.DataFrame(data)

            # Add 3% missing values to random optional columns
            for col in table['columns']:
                if not col.get('is_pk') and col['type'] != 'foreign_key':
                    if random.random() < 0.5:  # 50% chance this column has nulls
                        null_indices = random.sample(range(len(df)), int(len(df) * 0.03))
                        df.loc[null_indices, col['name']] = None

            datasets[table_name] = df

        print(f"✅ Generated {sum(len(df) for df in datasets.values()):,} total rows")
        return datasets

    def quick_qa(self, datasets, schema):
        """Run quick quality checks."""
        print("\n🔍 Running quality checks...")

        issues = []
        score = 10.0

        # Check 1: No empty tables
        for name, df in datasets.items():
            if len(df) == 0:
                issues.append(f"❌ Table {name} is empty")
                score -= 2

        # Check 2: Foreign key integrity (simplified)
        for table in schema['tables']:
            table_name = table['name']
            if table_name not in datasets:
                continue

            for col in table['columns']:
                if col['type'] == 'foreign_key':
                    parent_table = col['references']
                    if parent_table in datasets:
                        # Check FK values exist in parent
                        parent_pks = set(datasets[parent_table].iloc[:, 0])
                        child_fks = set(datasets[table_name][col['name']].dropna())
                        orphans = child_fks - parent_pks
                        if orphans:
                            issues.append(f"⚠️ {len(orphans)} orphan FKs in {table_name}.{col['name']}")
                            score -= 0.5

        # Check 3: Null percentages
        for name, df in datasets.items():
            null_pct = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
            if null_pct > 10:
                issues.append(f"⚠️ {name} has {null_pct:.1f}% nulls (high)")
                score -= 0.2

        # Check 4: Duplicate PKs
        for table in schema['tables']:
            table_name = table['name']
            if table_name not in datasets:
                continue
            pk_col = next((c['name'] for c in table['columns'] if c.get('is_pk')), None)
            if pk_col:
                df = datasets[table_name]
                if df[pk_col].duplicated().any():
                    issues.append(f"❌ Duplicate PKs in {table_name}")
                    score -= 1

        score = max(0, min(10, score))

        if not issues:
            print("✅ All checks passed!")
        else:
            print(f"Found {len(issues)} issue(s):")
            for issue in issues[:5]:
                print(f"  {issue}")

        return score, issues

    def save_results(self, datasets, schema, score):
        """Save datasets and summary."""
        output_dir = "demo_output"
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n💾 Saving results to {output_dir}/...")

        # Save CSVs
        for name, df in datasets.items():
            filepath = os.path.join(output_dir, f"{name}.csv")
            df.to_csv(filepath, index=False)
            print(f"  ✅ {name}.csv ({len(df)} rows)")

        # Save schema
        with open(os.path.join(output_dir, "schema.json"), "w") as f:
            json.dump(schema, f, indent=2)

        # Save summary
        summary = {
            "generated_at": datetime.now().isoformat(),
            "quality_score": score,
            "tables": {name: len(df) for name, df in datasets.items()},
            "total_rows": sum(len(df) for df in datasets.values())
        }
        with open(os.path.join(output_dir, "summary.json"), "w") as f:
            json.dump(summary, f, indent=2)

        print(f"\n📁 All files saved to: {os.path.abspath(output_dir)}/")


def main():
    """Main demo workflow."""
    print("=" * 70)
    print("  DATA CHALLENGE GENERATOR - SIMPLE DEMO")
    print("=" * 70)

    # User input
    print("\nEnter your challenge details:")
    domain = input("Domain (e.g., E-Commerce): ").strip() or "E-Commerce"
    function = input("Function (e.g., Sales): ").strip() or "Sales & Marketing"
    problem = input("Problem (or press Enter for default): ").strip() or """
    A retail company is experiencing declining customer retention.
    Repeat purchase rates dropped from 45% to 28% over 2019-2024.
    Need to analyze customer behavior and purchase patterns to identify causes.
    """
    num_rows = input("Number of rows (default 1000): ").strip()
    num_rows = int(num_rows) if num_rows.isdigit() else 1000

    print("\n" + "=" * 70)

    # Generate
    generator = SimpleDataGenerator()

    # Step 1: Schema
    schema = generator.generate_schema(domain, function, problem)

    # Step 2: Data
    datasets = generator.generate_data(schema, num_rows)

    # Step 3: QA
    score, issues = generator.quick_qa(datasets, schema)

    # Step 4: Save
    generator.save_results(datasets, schema, score)

    # Summary
    print("\n" + "=" * 70)
    print("  RESULTS")
    print("=" * 70)
    print(f"✅ Quality Score: {score:.1f} / 10")
    if score >= 8:
        print("🎉 Status: APPROVED")
    elif score >= 6:
        print("⚠️  Status: NEEDS REVIEW")
    else:
        print("❌ Status: REJECTED")

    print(f"\n📊 Generated {len(datasets)} tables")
    for name, df in datasets.items():
        print(f"   • {name}: {len(df):,} rows × {len(df.columns)} columns")

    print("\n" + "=" * 70)
    print("Demo complete! Check the demo_output/ folder for CSV files.")
    print("=" * 70)


if __name__ == "__main__":
    main()
