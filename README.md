# Codebasics Data Challenge Generator

**Foundation Phase: Data Quality Engine + PDF Report**

A production-grade system that generates realistic, quality-validated synthetic datasets for data analytics training.

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

## 🚀 Quick Start (Local Docker)

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

## 📁 Project Structure

```
CB Data Factory/
├── backend/
│   ├── src/
│   │   ├── main.py                # FastAPI entry point
│   │   ├── config.py              # Configuration
│   │   ├── models.py              # Data models
│   │   ├── schema_generator.py   # AI schema generation
│   │   └── dataset_generator.py  # Data generation engine
│   ├── output/                    # Generated datasets & reports
│   └── requirements.txt           # Python dependencies
│
├── frontend_new/
│   ├── src/
│   │   ├── app/                   # Next.js App Router
│   │   └── components/            # React components
│   └── package.json               # Node dependencies
```

## 🎓 Quality Validation Framework

The system validates datasets across **6 categories** with weighted scoring:

| Category | Weight | Checks |
|----------|--------|--------|
| **Technical Integrity** | 25% | FK integrity, data types, nulls, uniqueness |
| **Business Logic** | 25% | Financial rules, status transitions, KPI alignment |
| **Realism & Distribution** | 20% | Normal dist, outliers, seasonality, events |
| **Learning Alignment** | 20% | Supports objectives, variety, edge cases |
| **Schema Validation** | 10% | Column counts, relationships, structure |

**Decision Rule:**
- ≥ 8.0 → ✅ **Approved**
- 6.0-7.9 → ⚠️ **Regenerate**
- < 6.0 → ❌ **Rejected**

## 📖 Documentation

- [Task Breakdown](task.md) - Atomic-level implementation tasks
- [PRD](dataset_factory_prd.md) - Full product requirements
- [Detailed Deployment Guide](DEPLOYMENT_GUIDE.md) - Troubleshooting & Manual steps

## 🤝 Contributing

This is a foundation phase implementation. Once core quality engine is validated, we'll expand to full multi-phase workflow.
