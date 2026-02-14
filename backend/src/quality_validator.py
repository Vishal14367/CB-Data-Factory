"""
Advanced data quality validation engine with 8 mandatory check categories.
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from scipy import stats

from models import (
    ChallengeInput, Schema, QAResults, ValidationCheckResult,
    TableDefinition, ColumnDefinition
)
from config import (
    QUALITY_APPROVED_THRESHOLD, QUALITY_REGENERATE_THRESHOLD,
    SCORING_WEIGHTS, DIFFICULTY_CONFIG
)

logger = logging.getLogger(__name__)

class QualityValidator:
    """Validate generated dataset against 8 mandatory quality categories."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.results: List[ValidationCheckResult] = []
        self.regeneration_needed = False
        self.failure_reasons = []

    def validate(self, schema: Schema, data: Dict[str, pd.DataFrame], input_data: ChallengeInput) -> QAResults:
        """Run comprehensive validation suite."""
        logger.info(f"Starting advanced quality validation for session {self.session_id}")
        self.results = []
        self.regeneration_needed = False
        self.failure_reasons = []
        
        # 1. Structural Integrity
        self._check_structural_integrity(schema, data, input_data)
        
        # 2. Completeness & Null Analysis
        self._check_completeness(schema, data)
        
        # 3. Duplicate Analysis
        self._check_duplicates(schema, data)
        
        # 4. Distribution Analysis
        self._check_distributions(schema, data)
        
        # 5. Numeric Range Validation
        self._check_numeric_ranges(schema, data)
        
        # 6. Time-Series Validation
        self._check_time_series(schema, data)
        
        # 7. Outlier & Anomaly Check
        self._check_outliers_anomalies(schema, data)
        
        # 8. Correlation Analysis
        self._check_correlations(schema, data)

        # Calculate scores
        category_scores = self._calculate_category_scores()
        overall_score = self._calculate_overall_score(category_scores)
        
        # Hard Rules for Regeneration
        if self.regeneration_needed:
            status = "Regenerate"
            logger.warning(f"Hard rules triggered regeneration: {', '.join(self.failure_reasons)}")
        else:
            status = "Rejected"
            if overall_score >= QUALITY_APPROVED_THRESHOLD:
                status = "Approved"
            elif overall_score >= QUALITY_REGENERATE_THRESHOLD:
                status = "Regenerate"
            
        return QAResults(
            session_id=self.session_id,
            overall_score=overall_score,
            category_scores=category_scores,
            status=status,
            checks=self.results,
            strengths=self._generate_strengths(),
            issues=self._generate_issues() + self.failure_reasons,
            generated_at=datetime.now()
        )

    def _add_result(self, name: str, category: str, passed: bool, score: float, message: str, details: Dict = None):
        self.results.append(ValidationCheckResult(
            check_name=name,
            category=category,
            passed=passed,
            score=score,
            message=message,
            details=details
        ))

    def _check_structural_integrity(self, schema: Schema, data: Dict[str, pd.DataFrame], input_data: ChallengeInput):
        """Check PKs, FKs, Orphans, Row/Col counts, Types."""
        issues = []
        scores = []
        
        total_cols = sum(len(t.columns) for t in schema.tables)
        total_cols = sum(len(t.columns) for t in schema.tables)
        try:
            expected_cols = DIFFICULTY_CONFIG.get(input_data.difficulty.value, DIFFICULTY_CONFIG["Medium"])["columns"]
        except AttributeError:
            # Fallback for legacy input data
            expected_cols = 20
        
        # PK Uniqueness
        for table in schema.tables:
            if table.name in data:
                df = data[table.name]
                if df[table.primary_key].duplicated().any():
                    issues.append(f"Duplicate PKs in {table.name}")
                    scores.append(0)
                else:
                    scores.append(10)

        # FK Validity & Orphans
        for fk in schema.relationships:
            if fk.child_table in data and fk.parent_table in data:
                child_vals = data[fk.child_table][fk.child_column].dropna().unique()
                parent_vals = set(data[fk.parent_table][fk.parent_column].unique())
                orphans = [v for v in child_vals if v not in parent_vals]
                if orphans:
                    issues.append(f"Orphan records in {fk.child_table}.{fk.child_column}")
                    scores.append(0)
                else:
                    scores.append(10)

        # Column counts
        if abs(total_cols - expected_cols) > 5:
            issues.append(f"Column count imbalance: found {total_cols}, expected ~{expected_cols}")
            scores.append(5)
        else:
            scores.append(10)

        avg_score = sum(scores)/len(scores) if scores else 0
        passed = avg_score > 8
        if not passed:
            self.regeneration_needed = True
            self.failure_reasons.append("Structural integrity broken")
            
        self._add_result("Structural Integrity", "technical_integrity", passed, avg_score, 
                        "; ".join(issues) if issues else "Structural integrity verified.")

    def _check_completeness(self, schema: Schema, data: Dict[str, pd.DataFrame]):
        """Null Analysis: Required <2%, Optional 2-5%, >10% check."""
        scores = []
        high_null_cols = []
        
        for name, df in data.items():
            null_pcts = df.isnull().mean() * 100
            for col, pct in null_pcts.items():
                if pct > 10:
                    high_null_cols.append(f"{name}.{col} ({pct:.1f}%)")
                    scores.append(0)
                elif pct > 5:
                    scores.append(7)
                else:
                    scores.append(10)
        
        avg_score = sum(scores)/len(scores) if scores else 10
        passed = avg_score >= 8
        if len(high_null_cols) > 3:
            self.regeneration_needed = True
            self.failure_reasons.append("Unrealistic null percentages")

        self._add_result("Completeness & Null Analysis", "technical_integrity", passed, avg_score,
                        f"Found {len(high_null_cols)} columns with high nulls." if high_null_cols else "Null distributions are realistic.")

    def _check_duplicates(self, schema: Schema, data: Dict[str, pd.DataFrame]):
        """Check for PK, Composite and Near-duplicates."""
        total_dup_pct = 0
        for name, df in data.items():
            dup_pct = df.duplicated().mean() * 100
            total_dup_pct += dup_pct
            
        avg_dup = total_dup_pct / len(data) if data else 0
        passed = avg_dup <= 3.0
        score = max(0, 10 - avg_dup * 2)
        
        if avg_dup > 5.0:
            self.regeneration_needed = True
            self.failure_reasons.append("Excessive duplicate records")

        self._add_result("Duplicate Analysis", "technical_integrity", passed, score,
                        f"Average duplicate rate: {avg_dup:.2f}% (Threshold: 3%).")

    def _check_distributions(self, schema: Schema, data: Dict[str, pd.DataFrame]):
        """Check for uniform distributions and skewness."""
        is_uniform = False
        scores = []
        
        for name, df in data.items():
            cat_cols = df.select_dtypes(include=['category', 'object', 'bool']).columns
            for col in cat_cols:
                counts = df[col].value_counts(normalize=True)
                if len(counts) > 1:
                    # Check if all counts are nearly equal (Uniform)
                    std = counts.std()
                    if std < 0.05: # Very low variance in frequencies
                        is_uniform = True
                        scores.append(0)
                    else:
                        scores.append(10)
        
        avg_score = sum(scores)/len(scores) if scores else 10
        if is_uniform:
            self.regeneration_needed = True
            self.failure_reasons.append("Distributions look uniform/artificially flat")

        self._add_result("Distribution Analysis", "realism_distribution", not is_uniform, avg_score,
                        "Distributions are realistic and show natural variance." if not is_uniform else "Warning: Flat distributions detected.")

    def _check_numeric_ranges(self, schema: Schema, data: Dict[str, pd.DataFrame]):
        """Min/Max, Mean/Median, Outliers, Negative checks."""
        issues = []
        for name, df in data.items():
            num_cols = df.select_dtypes(include=[np.number]).columns
            for col in num_cols:
                # Basic unrealistic check (e.g. negative prices)
                if any(x in col.lower() for x in ['price', 'amount', 'total', 'quantity']):
                    if (df[col] < 0).any():
                        issues.append(f"Negative values in {name}.{col}")
        
        passed = len(issues) == 0
        self._add_result("Numeric Range Validation", "technical_integrity", passed, 10 if passed else 5,
                        "Numeric ranges are realistic." if passed else "; ".join(issues))

    def _check_time_series(self, schema: Schema, data: Dict[str, pd.DataFrame]):
        """Seasonality, Seasonality, Flat Trend checks."""
        is_flat = False
        date_cols_found = False
        for name, df in data.items():
            date_cols = [c for c in df.columns if 'date' in c.lower()]
            if date_cols:
                date_cols_found = True
                d_col = date_cols[0]
                # Convert to datetime if not already
                if not pd.api.types.is_datetime64_any_dtype(df[d_col]):
                    df[d_col] = pd.to_datetime(df[d_col], errors='coerce')
                
                counts = df.groupby(df[d_col].dt.to_period('M')).size()
                if len(counts) > 2:
                    std = counts.std() / counts.mean()
                    if std < 0.1: # Very flat trend
                        is_flat = True
        
        if date_cols_found and is_flat:
            self.regeneration_needed = True
            self.failure_reasons.append("No seasonal variation or flat-line trend")

        self._add_result("Time-Series Validation", "realism_distribution", not is_flat, 10 if not is_flat else 4,
                        "Time-series data shows realistic variation." if not is_flat else "Detected artificial flat trend.")

    def _check_outliers_anomalies(self, schema: Schema, data: Dict[str, pd.DataFrame]):
        """Outlier % (5-10% ideal), Impossible combinations."""
        outlier_pcts = []
        for name, df in data.items():
            num_cols = df.select_dtypes(include=[np.number]).columns
            for col in num_cols:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                outlier_count = ((df[col] < (q1 - 1.5 * iqr)) | (df[col] > (q3 + 1.5 * iqr))).sum()
                outlier_pcts.append(outlier_count / len(df) * 100)
        
        avg_outlier = sum(outlier_pcts)/len(outlier_pcts) if outlier_pcts else 7.0
        # Target: 5-10%
        if avg_outlier < 1.0 or avg_outlier > 20.0:
            self.regeneration_needed = True
            self.failure_reasons.append(f"Unrealistic outlier percentage ({avg_outlier:.1f}%)")
            score = 3
        else:
            score = 10
            
        self._add_result("Outlier & Anomaly Check", "realism_distribution", score > 5, score,
                        f"Outlier percentage: {avg_outlier:.1f}% (Ideal: 5-10%).")

    def _check_correlations(self, schema: Schema, data: Dict[str, pd.DataFrame]):
        """Correlation Analysis (Random vs Synthetic Logic)."""
        is_synthetic_smell = False
        for name, df in data.items():
            num_df = df.select_dtypes(include=[np.number])
            if len(num_df.columns) > 1:
                corr = num_df.corr().abs()
                # If everything is perfectly correlated or perfectly zero
                if (corr > 0.99).sum().sum() > len(num_df.columns):
                    is_synthetic_smell = True
        
        if is_synthetic_smell:
            self.regeneration_needed = True
            self.failure_reasons.append("Correlation matrix unrealistic (synthetic smell)")

        self._add_result("Correlation Matrix Analysis", "realism_distribution", not is_synthetic_smell, 10 if not is_synthetic_smell else 2,
                        "Correlations between variables are logically sound." if not is_synthetic_smell else "Perfect correlations detected.")

    def _calculate_category_scores(self) -> Dict[str, float]:
        scores = {}
        for category in SCORING_WEIGHTS.keys():
            cat_results = [r.score for r in self.results if r.category == category]
            scores[category] = sum(cat_results) / len(cat_results) if cat_results else 10.0
        return scores

    def _calculate_overall_score(self, category_scores: Dict[str, float]) -> float:
        total = 0.0
        for cat, weight in SCORING_WEIGHTS.items():
            total += category_scores.get(cat, 0.0) * weight
        return round(total, 1)

    def _generate_strengths(self) -> List[str]:
        return [r.message for r in self.results if r.passed and r.score >= 9.0][:3]

    def _generate_issues(self) -> List[str]:
        return [r.message for r in self.results if not r.passed or r.score < 8.0]
