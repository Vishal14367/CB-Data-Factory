"""
Realistic dataset generation engine.
"""
import pandas as pd
import numpy as np
from faker import Faker
import logging
from typing import Dict, List, Any, Optional
import uuid
import random
from datetime import datetime, timedelta
from pathlib import Path

from models import (
    ChallengeInput, Schema, TableDefinition, ColumnDefinition,
    ForeignKeyDefinition, BusinessRule, KPIDefinition, EventImpact
)
from config import (
    INTENTIONAL_MISSING_VALUES_PCT, INTENTIONAL_FORMAT_INCONSISTENCY_PCT,
    INTENTIONAL_DUPLICATES_PCT, INTENTIONAL_OUTLIERS_PCT,
    NORMAL_DISTRIBUTION_PCT
)

logger = logging.getLogger(__name__)

class DatasetGenerator:
    """Generate realistic datasets based on AI-generated schema."""

    def __init__(self, seed: Optional[int] = None):
        self.fake = Faker()
        if seed:
            random.seed(seed)
            np.random.seed(seed)
            Faker.seed(seed)
        
        self.generated_data: Dict[str, pd.DataFrame] = {}

    def generate(self, schema: Schema, total_rows: int) -> Dict[str, pd.DataFrame]:
        """
        Generate complete dataset for all tables in schema.
        
        Args:
            schema: The database schema to follow
            total_rows: Target row count for the main fact table
            
        Returns:
            Dictionary mapping table names to Pandas DataFrames
        """
        logger.info(f"Starting data generation for {len(schema.tables)} tables")
        
        # Determine generation order (topological sort based on FKs)
        generation_order = self._get_generation_order(schema)
        
        for table_name in generation_order:
            table_def = next(t for t in schema.tables if t.name == table_name)
            
            # Determine row count for this table
            # Fact tables get total_rows, dimension tables usually get 5-10% of total_rows or a reasonable minimum
            is_fact = "fact" in table_name.lower() or not any(fk.parent_table == table_name for fk in schema.relationships)
            
            if is_fact:
                row_count = total_rows
            else:
                # Dimension tables are smaller
                row_count = max(50, int(total_rows * 0.05))
                # Cap dimensions at a reasonable limit for realism unless specified
                row_count = min(row_count, 5000)

            logger.info(f"Generating {row_count} rows for table: {table_name}")
            df = self._generate_table_data(table_def, row_count, schema)
            self.generated_data[table_name] = df
            
        # Apply business rules and cross-table logic
        self._apply_business_rules(schema)
        
        # Inject intentional quality issues
        self._inject_quality_issues(schema)
        
        return self.generated_data

    def _get_generation_order(self, schema: Schema) -> List[str]:
        """Sort tables so parents are generated before children."""
        order = []
        visited = set()
        
        def visit(table_name):
            if table_name in visited:
                return
            if table_name in [item for item in order]:
                return
                
            # Find dependencies (parents)
            parents = [fk.parent_table for fk in schema.relationships if fk.child_table == table_name]
            for parent in parents:
                visit(parent)
                
            visited.add(table_name)
            order.append(table_name)

        for table in schema.tables:
            visit(table.name)
            
        return order

    def _generate_table_data(self, table_def: TableDefinition, row_count: int, schema: Schema) -> pd.DataFrame:
        """Generate data for a single table."""
        data = {}
        
        # First generate IDs and FKs to ensure integrity
        pks = self._generate_primary_key(table_def, row_count)
        data[table_def.primary_key] = pks
        
        # Foreign Keys
        for fk in schema.relationships:
            if fk.child_table == table_def.name:
                parent_df = self.generated_data.get(fk.parent_table)
                if parent_df is not None:
                    # Pick random values from parent's PK
                    parent_pks = parent_df[fk.parent_column].values
                    data[fk.child_column] = np.random.choice(parent_pks, size=row_count)
        
        # Other columns
        for col in table_def.columns:
            if col.name in data:
                continue # Already generated (PK or FK)
                
            data[col.name] = self._generate_column_values(col, row_count, schema)
            
        return pd.DataFrame(data)

    def _generate_primary_key(self, table_def: TableDefinition, row_count: int) -> List[str]:
        """Generate unique prefixed IDs."""
        pk_col = next(c for c in table_def.columns if c.name == table_def.primary_key)
        prefix = pk_col.id_prefix or table_def.name[:3].upper()
        
        ids = [f"{prefix}{str(i).zfill(6)}" for i in range(1, row_count + 1)]
        return ids

    def _generate_string_pool(self, generator_func, pool_size: int) -> List[str]:
        """Pre-generate a pool of fake values to sample from (much faster than per-row)."""
        return [generator_func() for _ in range(pool_size)]

    def _sample_from_pool(self, pool: List[str], row_count: int) -> np.ndarray:
        """Sample row_count values from a pre-generated pool."""
        return np.array([pool[i % len(pool)] for i in np.random.randint(0, len(pool), row_count)])

    def _generate_column_values(self, col: ColumnDefinition, row_count: int, schema: Schema) -> np.ndarray:
        """Generate realistic values based on column definition."""

        # Pool size: generate a small set of unique values, then sample
        # This avoids calling Faker thousands of times per column
        pool_size = min(500, row_count)

        if col.datatype == "string":
            if "name" in col.name.lower():
                pool = self._generate_string_pool(self.fake.name, pool_size)
                return self._sample_from_pool(pool, row_count)
            if "email" in col.name.lower():
                pool = self._generate_string_pool(self.fake.email, pool_size)
                return self._sample_from_pool(pool, row_count)
            if "address" in col.name.lower():
                pool = self._generate_string_pool(lambda: self.fake.address().replace('\n', ', '), pool_size)
                return self._sample_from_pool(pool, row_count)
            if "phone" in col.name.lower():
                pool = self._generate_string_pool(self.fake.phone_number, pool_size)
                return self._sample_from_pool(pool, row_count)
            pool = self._generate_string_pool(self.fake.word, pool_size)
            return self._sample_from_pool(pool, row_count)

        elif col.datatype == "integer":
            min_val = col.constraints.get("min", 0) if col.constraints else 0
            max_val = col.constraints.get("max", 1000) if col.constraints else 1000

            # 80% normal distribution, 20% uniform
            n_normal = int(row_count * NORMAL_DISTRIBUTION_PCT)
            n_uniform = row_count - n_normal

            mean = (min_val + max_val) / 2
            std = (max_val - min_val) / 6

            normal_vals = np.random.normal(mean, std, n_normal).clip(min_val, max_val).astype(int)
            uniform_vals = np.random.randint(min_val, max_val + 1, n_uniform)

            vals = np.concatenate([normal_vals, uniform_vals])
            np.random.shuffle(vals)
            return vals

        elif col.datatype == "float":
            min_val = col.constraints.get("min", 0.0) if col.constraints else 0.0
            max_val = col.constraints.get("max", 1000.0) if col.constraints else 1000.0

            vals = np.random.uniform(min_val, max_val, row_count).round(2)
            return vals

        elif col.datatype == "date" or col.datatype == "datetime":
            start_date = pd.Timestamp(schema.date_range_start)
            end_date = pd.Timestamp(schema.date_range_end)
            delta_days = (end_date - start_date).days

            # Vectorized date generation using pandas
            random_days = np.random.randint(0, delta_days + 1, row_count)
            dates = start_date + pd.to_timedelta(random_days, unit='D')

            if col.datatype == "date":
                return dates.date
            return dates.to_numpy()

        elif col.datatype == "category" or col.datatype == "boolean":
            choices = col.allowed_values or [True, False]
            # Use non-uniform distribution for realism
            if len(choices) > 1:
                # Pareto-like: first few choices are more common
                weights = [1.0 / (i + 1) for i in range(len(choices))]
                total_weight = sum(weights)
                probs = [w / total_weight for w in weights]
                return np.random.choice(choices, size=row_count, p=probs)
            return np.random.choice(choices, size=row_count)

        return np.array([None] * row_count)

    def _apply_business_rules(self, schema: Schema):
        """Apply cross-column and cross-table business logic."""
        for rule in schema.business_rules:
            if rule.rule_type == "calculated_field":
                self._apply_calculation_rule(rule)
            elif rule.rule_type == "status_transition":
                self._apply_status_rule(rule)
                
        # Apply event impacts
        self._apply_event_impacts(schema)

    def _apply_calculation_rule(self, rule: BusinessRule):
        """Handle rules like 'total = quantity * unit_price'."""
        target_table = rule.parameters.get("table")
        if target_table not in self.generated_data:
            return
            
        df = self.generated_data[target_table]
        formula = rule.parameters.get("formula") # e.g. "total_amount = quantity * unit_price"
        
        try:
            target_col, expr = formula.split('=')
            target_col = target_col.strip()
            # This is a very simple parser, in production we might use something more robust
            # But for educational datasets, simple math is usually enough
            df[target_col] = df.eval(expr.strip())
        except Exception as e:
            logger.warning(f"Failed to apply calculation rule: {rule.description}. Error: {e}")

    def _apply_status_rule(self, rule: BusinessRule):
        """Handle status transitions (placeholders for now)."""
        # Complex status transitions usually involve date sequencing too
        # For simplicity in Phase 1, we ensure random statuses match allowed values
        pass

    def _apply_event_impacts(self, schema: Schema):
        """Modify data to reflect historical events like COVID."""
        for impact in schema.event_impacts:
            start_date = datetime.strptime(impact.start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(impact.end_date, "%Y-%m-%d").date()
            magnitude = impact.impact_magnitude
            
            for table_name, df in self.generated_data.items():
                # Find date column
                date_cols = [c for c in df.columns if 'date' in c.lower()]
                if not date_cols:
                    continue
                    
                date_col = date_cols[0]
                mask = (df[date_col] >= start_date) & (df[date_col] <= end_date)
                
                for metric in impact.affected_metrics:
                    if metric in df.columns:
                        # Apply impact
                        df.loc[mask, metric] = df.loc[mask, metric] * (1 + magnitude)

    def _inject_quality_issues(self, schema: Schema):
        """Inject intentional data quality issues for learning."""
        for table_name, df in self.generated_data.items():
            # 1. Missing values
            cols_to_null = [c for c in df.columns if c != next(t.primary_key for t in schema.tables if t.name == table_name)]
            for col in cols_to_null:
                mask = np.random.random(len(df)) < INTENTIONAL_MISSING_VALUES_PCT
                if df[col].dtype == bool:
                    df[col] = df[col].astype(object)
                df.loc[mask, col] = np.nan
                
            # 2. Duplicates
            if len(df) > 100:
                n_dups = int(len(df) * INTENTIONAL_DUPLICATES_PCT)
                dup_indices = np.random.choice(df.index, size=n_dups)
                dups = df.loc[dup_indices].copy()
                # Append duplicates
                self.generated_data[table_name] = pd.concat([df, dups]).reset_index(drop=True)

            # 3. Format inconsistencies (dates or strings)
            # Placeholder: In production, we'd change format of some values

    def save_to_disk(self, output_dir: Path):
        """Save generated dataframes to CSV files."""
        output_dir.mkdir(parents=True, exist_ok=True)
        for table_name, df in self.generated_data.items():
            df.to_csv(output_dir / f"{table_name}.csv", index=False)
            logger.info(f"Saved {table_name}.csv to {output_dir}")
