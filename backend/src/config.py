"""
Configuration management for the Data Challenge Generator.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# Note: API key validation happens at runtime when the API is called

# AI Model Configuration
AI_MODEL = "llama-3.3-70b-versatile"  # Groq's fast model

# Server Configuration
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))

# Research API Keys
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY", "pub_e438d98854874fd2a3f8df81bf56ab02")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "bdfd54b3163f478c9e928ece3720f3c8")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "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")

# Generation Defaults
DEFAULT_DIFFICULTY = os.getenv("DEFAULT_DIFFICULTY", "Medium")
DEFAULT_DATA_STRUCTURE = os.getenv("DEFAULT_DATA_STRUCTURE", "Normalized")

# Data Generation Constants
DATE_RANGE_START = "2019-01-01"
DATE_RANGE_END = "2024-12-31"

# Auto-Configuration by Difficulty
DIFFICULTY_CONFIG = {
    "Easy": {
        "rows": 5000, 
        "normalized_tables": 5, 
        "columns": 15, 
        "questions": 4, 
        "preview_rows": 10
    },
    "Medium": {
        "rows": 10000, 
        "normalized_tables": 8, 
        "columns": 22, 
        "questions": 5, 
        "preview_rows": 20
    },
    "Difficult": {
        "rows": 20000, 
        "normalized_tables": 12, 
        "columns": 30, 
        "questions": 6, 
        "preview_rows": 30
    }
}

# Table counts by structure
DENORMALIZED_TABLES = 1

# Quality thresholds
QUALITY_APPROVED_THRESHOLD = 8.0
QUALITY_REGENERATE_THRESHOLD = 6.0
MAX_REGENERATION_ITERATIONS = 3

# Intentional issue percentages
INTENTIONAL_MISSING_VALUES_PCT = 0.03  # 3%
INTENTIONAL_FORMAT_INCONSISTENCY_PCT = 0.02  # 2%
INTENTIONAL_DUPLICATES_PCT = 0.01  # 1%
INTENTIONAL_OUTLIERS_PCT = 0.025  # 2.5%

# Distribution settings
NORMAL_DISTRIBUTION_PCT = 0.80  # 80% of data follows normal distribution
OUTLIER_PCT_MIN = 0.05  # 5% minimum outliers
OUTLIER_PCT_MAX = 0.10  # 10% maximum outliers

# Scoring weights
SCORING_WEIGHTS = {
    "technical_integrity": 0.25,
    "business_logic": 0.25,
    "realism_distribution": 0.20,
    "learning_alignment": 0.20,
    "documentation_schema": 0.10
}

# PDF settings
PDF_MIN_VISUALS_DENORMALIZED = 8
PDF_MIN_VISUALS_NORMALIZED = 10
PDF_PAGE_SIZE = "A4"
PDF_FONT_FAMILY = "Helvetica"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
