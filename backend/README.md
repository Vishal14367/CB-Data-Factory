# Data Challenge Generator - Backend

Foundation Phase implementation of the data quality engine.

## Setup

1. **Install Python 3.10+** (if not already installed)

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment:**
   - Copy `.env.example` to `.env`
   - Add your Anthropic API key to `.env`

6. **Run the server:**
   ```bash
   cd src
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   cd src
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

## API Endpoints

- `GET /` - Health check
- `POST /api/challenge/create` - Create new challenge (full pipeline)
- `GET /api/challenge/status/{session_id}` - Get generation progress
- `GET /api/challenge/result/{session_id}` - Get final results
- `GET /api/report/download/{session_id}` - Download PDF report
- `GET /api/data/download/{session_id}` - Download generated data

## Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models
│   ├── schema_generator.py  # AI-driven schema generation
│   ├── data_generator.py    # Data generation engine
│   ├── qa_validator.py      # Quality validation engine
│   └── pdf_report.py        # PDF report generation
├── tests/                   # Unit and integration tests
├── output/                  # Generated datasets and reports
└── requirements.txt         # Python dependencies
```

## Next Steps

1. Implement schema generation with Claude API
2. Build data generation engine
3. Create QA validation engine
4. Develop PDF report generator
5. Wire full pipeline
6. Add comprehensive testing
