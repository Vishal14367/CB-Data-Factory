# 👋 START HERE

## What You Have

You have **TWO versions** of the Data Challenge Generator:

---

## 🟢 Option 1: Simple Demo (RECOMMENDED TO START)

**Perfect for:** Testing the concept immediately with minimal setup

**Requirements:** Just Python

**How to run:**
1. Double-click [RUN_DEMO.bat](RUN_DEMO.bat)
2. Enter your domain/function/problem
3. Get CSV files in `demo_output/` folder

**Read:** [DEMO_README.md](DEMO_README.md)

**What it does:**
- ✅ AI schema generation (Groq)
- ✅ Realistic data with FK integrity
- ✅ Basic quality checks
- ✅ CSV export

**What it doesn't have:**
- ❌ PDF reports
- ❌ Web UI
- ❌ Advanced QA (30+ checks)
- ❌ Event simulation

---

## 🔵 Option 2: Full Application (Production Version)

**Perfect for:** Complete quality validation with PDF reports

**Requirements:** Python + Node.js

**How to run:**
1. Double-click [INSTALL_AND_RUN.bat](INSTALL_AND_RUN.bat)
2. Wait for auto-setup
3. Use web interface at http://localhost:3000

**Read:** [README.md](README.md) or [SETUP_GUIDE.md](SETUP_GUIDE.md)

**What it does:**
- ✅ Everything from Simple Demo, PLUS:
- ✅ 17-page PDF quality report
- ✅ Web UI (React + FastAPI)
- ✅ 30+ validation checks across 6 categories
- ✅ Event simulation (COVID dips, seasonality)
- ✅ Intentional quality issues for learning
- ✅ Comprehensive QA scoring

---

## 🎯 Recommended Path

### Step 1: Try the Simple Demo
- Fastest way to see it work
- No complex setup
- Proves the core concept

### Step 2: Review the Output
- Check `demo_output/*.csv` files
- Verify data looks realistic
- Check `schema.json` structure

### Step 3: If satisfied, move to Full Version
- Install Python + Node.js
- Run [INSTALL_AND_RUN.bat](INSTALL_AND_RUN.bat)
- Get PDF reports and full QA

---

## Quick Decision Guide

**Just want to see if this works?**
→ Use **Simple Demo** ([RUN_DEMO.bat](RUN_DEMO.bat))

**Need PDF reports for actual use?**
→ Use **Full Application** ([INSTALL_AND_RUN.bat](INSTALL_AND_RUN.bat))

**Want to understand the code?**
→ Read [task.md](task.md) for full breakdown

**Having issues?**
→ Check troubleshooting in [DEMO_README.md](DEMO_README.md) or [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## Files Overview

```
📁 CB Data Factory/
│
├── 🟢 SIMPLE DEMO
│   ├── RUN_DEMO.bat          ← Double-click to start
│   ├── demo_simple.py         ← All code in one file
│   ├── DEMO_README.md         ← Instructions
│   └── demo_output/           ← Generated CSV files
│
├── 🔵 FULL APPLICATION
│   ├── INSTALL_AND_RUN.bat   ← Auto-setup + start
│   ├── backend/               ← Python FastAPI server
│   ├── frontend/              ← React web interface
│   ├── README.md              ← Full docs
│   └── SETUP_GUIDE.md         ← Detailed setup
│
├── 📋 DOCUMENTATION
│   ├── START_HERE.md          ← You are here!
│   ├── task.md                ← Task breakdown
│   └── dataset_factory_prd.md ← Full PRD
│
└── 📂 OUTPUT (created after running)
    ├── demo_output/           ← Simple demo files
    └── backend/output/        ← Full app sessions
```

---

## Current Status

### ✅ What's Built

**Simple Demo:**
- [x] Complete and ready to run
- [x] Schema generation (AI)
- [x] Data generation
- [x] Basic QA
- [x] CSV export

**Full Application:**
- [x] Backend structure
- [x] Frontend UI
- [x] Schema generation (AI)
- [x] API endpoints
- [ ] Data generation engine (in progress)
- [ ] Full QA engine (in progress)
- [ ] PDF report generator (in progress)

### 🚧 What's Next

If you want to continue development:
1. Data generation engine (advanced)
2. QA validation engine (30+ checks)
3. PDF report generator (17 pages + charts)
4. End-to-end integration

---

## Need Help?

**Can't run Simple Demo:**
- Make sure Python is installed: `python --version`
- Install Python from: https://www.python.org/downloads/
- Check [DEMO_README.md](DEMO_README.md) troubleshooting

**Can't run Full Application:**
- Need both Python + Node.js
- See [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step
- Or just use Simple Demo for now!

**Want to understand how it works:**
- Read [task.md](task.md) - atomic task breakdown
- Read [dataset_factory_prd.md](dataset_factory_prd.md) - full requirements
- Check code comments in `demo_simple.py` or `backend/src/`

---

## 🎉 You're Ready!

**Quickest way to see this work:**

1. Double-click [RUN_DEMO.bat](RUN_DEMO.bat)
2. Press Enter a few times (uses defaults)
3. Check `demo_output/` folder
4. Open the CSV files

That's it! You'll have AI-generated realistic data in 30 seconds.
