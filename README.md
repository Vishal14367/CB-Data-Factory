# Codebasics Data Challenge Generator

**Foundation Phase: Data Quality Engine + PDF Report**

A production-grade system that generates realistic, quality-validated synthetic datasets for data analytics training.

---

## 🌍 Live Deployment (Get your own URL)

Want to get a live link that anyone can access? Click the button below to deploy this project for **FREE** on Render:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Vishal14367/CB-Data-Factory)

**Deployment Steps:**
1. Click the button above.
2. Link your GitHub account.
3. In the **`GROQ_API_KEY`** field, enter your actual Groq API key.
4. Click **Apply**.
5. Once building finishes (about 5-10 mins), Render will give you a live URL (e.g., `https://cb-data-factory.onrender.com`).

---

## 🚀 **NEW: Simple Demo Available!**

**Want to try it NOW without any setup?**

👉 **See [DEMO_README.md](DEMO_README.md)** for a single-file demo that requires only Python!

Or just double-click: [RUN_DEMO.bat](RUN_DEMO.bat)

---

## 🎯 What This Does

1. **User enters:** Domain + Function + Problem Statement
2. **AI generates:** Complete data schema (tables, columns, relationships, business rules)
3. **System creates:** Realistic dataset with:
   - FK integrity (zero orphans)
   - Realistic distributions (not uniform)
   - Seasonal patterns
   - Intentional quality issues (for learning)
   - Event impacts (COVID dips, etc.)
4. **QA validates:** 6 categories of checks (technical, business, realism, learning, edge cases, schema)
5. **Outputs:** 17-page PDF quality report with 10-15 visualizations

## 🚀 Quick Start (Choose One)

### Option 1: Docker (Easiest - Runs everywhere)
If you have **Docker Desktop** installed, this is the fastest way:

1. **Clone/Download** this repository.
2. In the project root, create/verify `backend/.env` with your key:
   ```text
   GROQ_API_KEY=your_key_here
   ```
3. Run the following command:
   ```bash
   docker-compose up --build
   ```
4. Open your browser: **`http://localhost:3000`**

---

### Option 2: Manual Setup (Local Development)

#### Prerequisites
- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Groq API Key** - [Get one here](https://console.groq.com/)

#### Setup
1. **Clone/Download** this repository.
2. **Configure API Key:**
   ```bash
   cd backend
   copy .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```
3. **Start Backend:**
   ```bash
   cd backend
   # Run the start script
   start.bat
   ```
   *Backend: `http://127.0.0.1:8000`*
4. **Start Frontend (in new terminal):**
   ```bash
   cd frontend_new
   # Run the start script
   start.bat
   ```
   *Frontend: `http://localhost:3000`*
5. **Open your browser:** `http://localhost:3000`

## 📁 Project Structure

```
CB Data Factory/
├── backend/
│   ├── src/
│   │   ├── main.py                # FastAPI entry point
│   │   ├── config.py              # Configuration
│   │   ├── models.py              # Data models
│   │   ├── schema_generator.py   # AI schema generation
│   │   ├── data_generator.py     # Data generation engine
│   │   ├── qa_validator.py       # Quality validation
│   │   └── pdf_report.py         # PDF report generation
│   ├── output/                    # Generated datasets & reports
│   └── requirements.txt           # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Main React component
│   │   └── main.jsx               # React entry point
│   └── package.json               # Node dependencies
│
└── task.md                        # Implementation task breakdown
```

## 🎓 Quality Validation Framework

The system validates datasets across **6 categories** with weighted scoring:

| Category | Weight | Checks |
|----------|--------|--------|
| **Technical Integrity** | 25% | FK integrity, data types, nulls, uniqueness |
| **Business Logic** | 25% | Financial rules, status transitions, KPI alignment |
| **Realism & Distribution** | 20% | Normal dist, outliers, seasonality, events |
| **Learning Alignment** | 20% | Supports objectives, variety, edge cases |
| **Edge Cases** | - | Failed transactions, reversals, duplicates |
| **Schema Validation** | 10% | Column counts, relationships, structure |

**Decision Rule:**
- ≥ 8.0 → ✅ **Approved**
- 6.0-7.9 → ⚠️ **Regenerate**
- < 6.0 → ❌ **Rejected**

## 📊 PDF Report Contents (17 Pages)

1. Cover page with quality score
2. Executive summary
3. Dataset overview
4-5. Schema validation (with ERD)
6-7. Technical integrity (with charts)
8-9. Business logic validation
10-11. Realism & distribution
12. Edge case validation
13. Learning objective alignment
14. Quality score breakdown
15. Issues & regeneration log
16. Appendix (data dictionary)
17. **Visual summary dashboard** (one-glance approval)

**Minimum visuals:** 10-15 charts/diagrams

## 🔧 Current Status

### ✅ Completed
- [x] Backend project setup
- [x] Frontend minimal UI
- [x] API endpoint structure
- [x] Configuration management
- [x] Data models (Pydantic)

### 🚧 In Progress
- [ ] Schema generation (Claude API)
- [ ] Data generation engine
- [ ] QA validation engine
- [ ] PDF report generation
- [ ] End-to-end pipeline

### 📋 Next Steps
1. Implement AI-driven schema generator
2. Build data generation engine with all value generators
3. Create comprehensive QA validation engine
4. Develop PDF report with matplotlib charts
5. Test with 3+ domain scenarios
6. Validate against quality checklist

## 🎯 Foundation Phase Goals

This phase focuses on **nailing the data quality engine**. Once approved:
- Quality is reproducible
- Validation is comprehensive
- PDF reports are professional
- Foundation is solid for full application build-out

## 📝 API Documentation

When backend is running, visit: `http://127.0.0.1:8000/docs`

Key endpoints:
- `POST /api/challenge/create` - Generate dataset + validate
- `GET /api/challenge/status/{id}` - Check progress
- `GET /api/report/download/{id}` - Download PDF

## 🆘 Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (need 3.10+)
- Ensure `.env` file exists with valid API key
- Try: `pip install -r requirements.txt` manually

**Frontend won't start:**
- Check Node version: `node --version` (need 18+)
- Try: `npm install` manually
- Clear cache: `npm cache clean --force`

**API key errors:**
- Verify key in `.env` is correct
- No quotes needed around the key
- No spaces before/after

## 📖 Documentation

- [Task Breakdown](task.md) - Atomic-level implementation tasks
- [PRD](dataset_factory_prd.md) - Full product requirements

## 🤝 Contributing

This is a foundation phase implementation. Once core quality engine is validated, we'll expand to full multi-phase workflow.
