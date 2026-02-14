"""
Advanced PDF quality report generator with 12 mandatory visuals and 10-section structure.
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Non-interactive backend
import seaborn as sns
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
import pandas as pd
import numpy as np
import io
import logging
from pathlib import Path
from typing import Dict, List, Any

from models import QAResults, Schema, ChallengeInput
from config import BASE_DIR

logger = logging.getLogger(__name__)

LOGO_PATH = BASE_DIR / "assets" / "logo.png"

class QualityReportPDF:
    """Generate high-quality PDF reports with 12 mandatory data validation visuals."""

    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CenterTitle', parent=self.styles['Title'], alignment=1, fontSize=24,
            textColor=colors.HexColor("#181830"), spaceAfter=20
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeader', parent=self.styles['Heading2'], fontSize=16,
            textColor=colors.whitesmoke, backColor=colors.HexColor("#3B82F6"),
            spaceBefore=20, spaceAfter=12, leftIndent=0, rightIndent=0,
            borderPadding=5, borderRadius=3, alignment=0
        ))
        self.styles.add(ParagraphStyle(
            name='ScoreBadge', parent=self.styles['Normal'], alignment=1, fontSize=48,
            textColor=colors.whitesmoke, backColor=colors.HexColor("#20C997"),
            borderPadding=10, borderRadius=10
        ))

    def _sample_data(self, data: Dict[str, pd.DataFrame], max_rows: int = 2000) -> Dict[str, pd.DataFrame]:
        """Sample large dataframes for faster chart rendering."""
        sampled = {}
        for name, df in data.items():
            if len(df) > max_rows:
                sampled[name] = df.sample(n=max_rows, random_state=42)
            else:
                sampled[name] = df
        return sampled

    def generate(self, qa_results: QAResults, schema: Schema, data: Dict[str, pd.DataFrame], input_data: ChallengeInput):
        """Generate the full structured PDF report with conditional sections."""
        doc = SimpleDocTemplate(str(self.output_path), pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        elements = []

        # Sample data for chart rendering (full data not needed for visuals)
        chart_data = self._sample_data(data)

        # Section 1: Cover Page
        elements.extend(self._create_cover_page(qa_results, input_data))
        elements.append(PageBreak())

        # Section 2: Structural Integrity (uses full data for accurate row counts)
        struct_page = self._create_structural_integrity_page(schema, data)
        if len(struct_page) > 1:
            elements.extend(struct_page)
            elements.append(PageBreak())

        # Section 3: Completeness (uses full data for accurate null %)
        completeness_page = self._create_completeness_page(data)
        if len(completeness_page) > 1:
            elements.extend(completeness_page)
            elements.append(PageBreak())

        # Section 4: Duplicates (uses full data for accurate counts)
        dup_page = self._create_duplicate_page(data)
        if len(dup_page) > 1:
            elements.extend(dup_page)
            elements.append(PageBreak())

        # Section 5: Numeric Distributions (sampled - charts don't need all rows)
        num_page = self._create_numeric_distribution_page(chart_data)
        if len(num_page) > 1:
            elements.extend(num_page)
            elements.append(PageBreak())

        # Section 6: Category Distributions (sampled)
        cat_page = self._create_category_distribution_page(chart_data)
        if len(cat_page) > 1:
            elements.extend(cat_page)
            elements.append(PageBreak())

        # Section 7: Time-Series (sampled)
        ts_page = self._create_time_series_page(chart_data)
        if len(ts_page) > 1:
            elements.extend(ts_page)
            elements.append(PageBreak())

        # Section 8: Outliers (sampled)
        outlier_page = self._create_outlier_page(chart_data)
        if len(outlier_page) > 1:
            elements.extend(outlier_page)
            elements.append(PageBreak())

        # Section 9: Correlations (sampled)
        corr_page = self._create_correlation_page(chart_data)
        if len(corr_page) > 1:
            elements.extend(corr_page)
            elements.append(PageBreak())

        # Section 10: Score Breakdown
        elements.extend(self._create_score_page(qa_results))

        doc.build(elements, onFirstPage=self._add_footer, onLaterPages=self._add_footer)
        logger.info(f"Structured PDF report saved to {self.output_path}")

    def _add_footer(self, canvas, doc):
        """Add footer with page number and brand."""
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setStrokeColor(colors.lightgrey)
        canvas.line(40, 50, A4[0]-40, 50)
        
        # Page Number
        page_num = f"Page {doc.page}"
        canvas.drawRightString(A4[0]-40, 35, page_num)
        
        # Branding
        canvas.drawString(40, 35, "Codebasics Data Factory - Official Quality Verification")
        canvas.restoreState()

    def _plot_to_image(self, width=6, height=4):
        """Helper to convert current plt to reportlab Image."""
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png', bbox_inches='tight', dpi=80)
        img_data.seek(0)
        img = Image(img_data, width=width*inch, height=height*inch)
        plt.close()
        return img

    def _create_cover_page(self, qa_results: QAResults, input_data: ChallengeInput):
        elements = []
        
        # Logo
        if LOGO_PATH.exists():
            elements.append(Image(str(LOGO_PATH), width=2*inch, height=0.8*inch))
        else:
            elements.append(Paragraph("Codebasics Data Factory", self.styles['Heading1']))
            
        elements.append(Spacer(1, 1.5 * inch))
        elements.append(Paragraph("Data Quality Verification Report", self.styles['CenterTitle']))
        elements.append(Paragraph(f"Domain: {input_data.domain}", self.styles['Heading2']))
        elements.append(Paragraph(f"Function: {input_data.function}", self.styles['Heading3']))
        
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph(f"{qa_results.overall_score}", self.styles['ScoreBadge']))
        elements.append(Paragraph("Overall Quality Score", self.styles['Normal']))
        elements.append(Spacer(1, 1 * inch))
        
        detail_data = [
            ["Status:", qa_results.status],
            ["Difficulty:", input_data.difficulty.value],
            ["Structure:", input_data.data_structure.value],
            ["Generated At:", qa_results.generated_at.strftime("%Y-%m-%d %H:%M")]
        ]
        t = Table(detail_data, colWidths=[1.5*inch, 3*inch])
        t.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold')]))
        elements.append(t)
        return elements

    def _create_structural_integrity_page(self, schema: Schema, data: Dict[str, pd.DataFrame]):
        elements = [Paragraph("Section 2: Structural Integrity Summary", self.styles['SectionHeader'])]
        
        # 1. Row Count per Table (Bar Chart)
        table_names = list(data.keys())
        counts = [len(df) for df in data.values()]
        plt.figure(figsize=(6, 4))
        sns.barplot(x=table_names, y=counts, palette="viridis", hue=table_names, legend=False)
        plt.title("Row Count per Table")
        plt.xticks(rotation=45)
        elements.append(self._plot_to_image())
        
        # 2. Column Data Type Distribution (Bar Chart)
        types = []
        for df in data.values():
            types.extend(df.dtypes.astype(str).tolist())
        type_counts = pd.Series(types).value_counts()
        plt.figure(figsize=(6, 4))
        type_counts.plot(kind='bar', color='#3B82F6')
        plt.title("Column Data Type Distribution")
        elements.append(self._plot_to_image())
        
        return elements

    def _create_completeness_page(self, data: Dict[str, pd.DataFrame]):
        elements = [Paragraph("Section 3: Completeness Analysis", self.styles['SectionHeader'])]
        
        # 3. Null % per Column (Bar Chart)
        all_nulls = []
        for name, df in data.items():
            s = df.isnull().mean() * 100
            for col, val in s.items():
                all_nulls.append({'Table.Col': f"{name}.{col}", 'Null %': val})
        
        null_df = pd.DataFrame(all_nulls).sort_values('Null %', ascending=False).head(15)
        plt.figure(figsize=(6, 4))
        sns.barplot(data=null_df, x='Null %', y='Table.Col', palette='flare', hue='Table.Col', legend=False)
        plt.title("Top 15 Columns by Null %")
        elements.append(self._plot_to_image())
        
        return elements

    def _create_duplicate_page(self, data: Dict[str, pd.DataFrame]):
        elements = [Paragraph("Section 4: Duplicate Analysis", self.styles['SectionHeader'])]
        
        # 4. Duplicate Count Chart
        dup_counts = {name: df.duplicated().sum() for name, df in data.items()}
        plt.figure(figsize=(6, 4))
        plt.bar(dup_counts.keys(), dup_counts.values(), color='mediumpurple')
        plt.title("Duplicate Row Count per Table")
        plt.xticks(rotation=45)
        elements.append(self._plot_to_image())
        
        return elements

    def _create_numeric_distribution_page(self, data: Dict[str, pd.DataFrame]):
        # Find numeric columns
        num_cols = []
        for name, df in data.items():
            for col in df.select_dtypes(include=[np.number]).columns:
                num_cols.append((name, col))
        
        if not num_cols:
            return []

        elements = [Paragraph("Section 5: Numeric Distribution Analysis", self.styles['SectionHeader'])]
        # 5. Histogram for first 2 numeric columns
        for name, col in num_cols[:2]:
            plt.figure(figsize=(6, 3))
            sns.histplot(data[name][col].dropna(), kde=False, color='skyblue', bins=30)
            plt.title(f"Histogram: {name}.{col}")
            elements.append(self._plot_to_image(height=2.5))
        
        # 6. Boxplot for first numeric column
        name, col = num_cols[0]
        plt.figure(figsize=(6, 3))
        sns.boxplot(x=data[name][col], color='lightgreen')
        plt.title(f"Boxplot: {name}.{col}")
        elements.append(self._plot_to_image(height=2.5))
        
        # 10. Numeric Range Summary Table
        stats_rows = [["Table.Column", "Min", "Max", "Mean", "Std"]]
        for name, col in num_cols[:5]:
            s = data[name][col].describe()
            stats_rows.append([f"{name}.{col}", f"{s['min']:.1f}", f"{s['max']:.1f}", f"{s['mean']:.1f}", f"{s['std']:.1f}"])
        
        t = Table(stats_rows, colWidths=[2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lightgrey), ('GRID',(0,0),(-1,-1),1,colors.black)]))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(t)

        return elements

    def _create_category_distribution_page(self, data: Dict[str, pd.DataFrame]):
        cat_cols = []
        for name, df in data.items():
            cols = df.select_dtypes(include=['object', 'category', 'bool']).columns
            for c in cols:
                cat_cols.append((name, c))
        
        if not cat_cols:
            return []

        elements = [Paragraph("Section 6: Category Distribution Analysis", self.styles['SectionHeader'])]
        # 7. Category Frequency Distribution (Top 10)
        name, col = cat_cols[0]
        counts = data[name][col].value_counts().head(10)
        plt.figure(figsize=(6, 4))
        counts.plot(kind='barh', color='darkorange')
        plt.title(f"Top 10 Frequencies: {name}.{col}")
        elements.append(self._plot_to_image())
        
        # 8. Top 5 vs Bottom 5 Comparison
        if len(counts) > 5:
            top5 = counts.head(5)
            bot5 = data[name][col].value_counts().tail(5)
            plt.figure(figsize=(6, 4))
            plt.subplot(1,2,1); top5.plot(kind='bar', title='Top 5')
            plt.subplot(1,2,2); bot5.plot(kind='bar', title='Bottom 5')
            plt.tight_layout()
            elements.append(self._plot_to_image())

        # 12. Value Count for Boolean Columns
        bool_found = False
        for name, df in data.items():
            b_cols = df.select_dtypes(include=['bool']).columns
            if not b_cols.empty:
                col = b_cols[0]
                counts = df[col].value_counts()
                plt.figure(figsize=(6, 3))
                counts.plot(kind='pie', autopct='%1.1f%%', colors=['#3B82F6', '#EF4444'])
                plt.title(f"Boolean Ratio: {name}.{col}")
                elements.append(self._plot_to_image(height=3))
                bool_found = True
                break

        return elements

    def _create_time_series_page(self, data: Dict[str, pd.DataFrame]):
        elements = []
        
        # 9. Time-Series Trend Chart (Records per Month)
        ts_found = False
        for name, df in data.items():
            date_cols = [c for c in df.columns if 'date' in c.lower()]
            if date_cols:
                if not ts_found:
                    elements.append(Paragraph("Section 7: Time-Series Analysis", self.styles['SectionHeader']))
                    ts_found = True
                d_col = date_cols[0]
                dates = pd.to_datetime(df[d_col], errors='coerce')
                ts = dates.groupby(dates.dt.to_period('M')).size()
                plt.figure(figsize=(6, 4))
                ts.plot(marker='o', color='teal')
                plt.title(f"Monthly Records Trend ({name})")
                elements.append(self._plot_to_image())
                break
        return elements

    def _create_outlier_page(self, data: Dict[str, pd.DataFrame]):
        # Check if numeric columns exist
        has_numeric = False
        for df in data.values():
            if not df.select_dtypes(include=[np.number]).columns.empty:
                has_numeric = True
                break
        
        if not has_numeric:
            return []

        elements = [Paragraph("Section 8: Outlier Analysis", self.styles['SectionHeader'])]
        # Outlier count summary
        outlier_data = [["Table.Column", "Outlier Count", "Percentage"]]
        for name, df in data.items():
            num_cols = df.select_dtypes(include=[np.number]).columns
            for col in num_cols[:2]: # limit
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                count = len(df[(df[col] < (q1 - 1.5 * iqr)) | (df[col] > (q3 + 1.5 * iqr))])
                outlier_data.append([f"{name}.{col}", str(count), f"{count/len(df)*100:.1f}%"])
        
        t = Table(outlier_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),1,colors.black),('BACKGROUND',(0,0),(-1,0),colors.whitesmoke)]))
        elements.append(t)
        return elements

    def _create_correlation_page(self, data: Dict[str, pd.DataFrame]):
        elements = []
        
        # 11. Correlation Heatmap
        corr_found = False
        for name, df in data.items():
            num_df = df.select_dtypes(include=[np.number])
            if len(num_df.columns) >= 2:
                if not corr_found:
                    elements.append(Paragraph("Section 9: Correlation Analysis", self.styles['SectionHeader']))
                    corr_found = True
                plt.figure(figsize=(6, 5))
                sns.heatmap(num_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
                plt.title(f"Correlation Heatmap: {name}")
                elements.append(self._plot_to_image())
                break
        return elements

    def _create_score_page(self, qa_results: QAResults):
        elements = [Paragraph("Section 10: Final Score Breakdown", self.styles['SectionHeader'])]
        score_data = [["Category", "Score", "Weight", "Contribution"]]
        from config import SCORING_WEIGHTS
        for cat, weight in SCORING_WEIGHTS.items():
            score = qa_results.category_scores.get(cat, 0.0)
            score_data.append([cat.replace('_',' ').title(), f"{score:.1f}", f"{weight*100}%", f"{score*weight:.2f}"])
        score_data.append(["TOTAL", f"{qa_results.overall_score}", "100%", f"{qa_results.overall_score}"])
        
        t = Table(score_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1.2*inch])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor("#181830")),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold')]))
        elements.append(t)
        return elements
