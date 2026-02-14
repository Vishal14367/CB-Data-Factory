# Codebasics Data Factory - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install & Run Server

```bash
cd backend/src
python main.py
```

Server starts at: `http://127.0.0.1:8000`

### 2. Test Complete Workflow

```bash
python demo_complete_workflow.py
```

This will execute all 5 phases automatically and download a complete package.

---

## 📋 Quick API Reference

### Phase 1: Research & Problem
```bash
POST /api/challenge/phase1/research
POST /api/challenge/phase1/generate-problem?session_id=...
POST /api/challenge/phase1/approve?session_id=...
```

### Phase 2: Schema
```bash
POST /api/challenge/phase2/generate-schema?session_id=...
POST /api/challenge/phase2/approve?session_id=...
```

### Phase 3: Preview
```bash
POST /api/challenge/phase3/generate-preview?session_id=...
POST /api/challenge/phase3/approve?session_id=...
```

### Phase 4: Full Generation
```bash
POST /api/challenge/phase4/generate-full?session_id=...
     Body: {"dataset_size": 10000}
GET  /api/challenge/phase4/status/{session_id}
```

### Phase 5: Download
```bash
GET /api/challenge/phase5/prepare/{session_id}
GET /api/challenge/phase5/download/{session_id}
```

---

## 💡 Example Workflow

```python
import requests

BASE = "http://127.0.0.1:8000"

# Phase 1
r = requests.post(f"{BASE}/api/challenge/phase1/research", json={...})
session_id = r.json()["session_id"]

# Phase 2
requests.post(f"{BASE}/api/challenge/phase2/generate-schema?session_id={session_id}")
requests.post(f"{BASE}/api/challenge/phase2/approve?session_id={session_id}")

# Phase 3
requests.post(f"{BASE}/api/challenge/phase3/generate-preview?session_id={session_id}")
requests.post(f"{BASE}/api/challenge/phase3/approve?session_id={session_id}")

# Phase 4
requests.post(f"{BASE}/api/challenge/phase4/generate-full?session_id={session_id}",
              json={"dataset_size": 5000})

# Wait for completion (poll)
while True:
    r = requests.get(f"{BASE}/api/challenge/phase4/status/{session_id}")
    if r.json()["status"] == "completed":
        break
    time.sleep(2)

# Phase 5
requests.get(f"{BASE}/api/challenge/phase5/prepare/{session_id}")
r = requests.get(f"{BASE}/api/challenge/phase5/download/{session_id}")

# Save ZIP
with open("package.zip", "wb") as f:
    f.write(r.content)
```

---

## 📊 What You Get

### During Process:
- ✓ Research results (Phase 1)
- ✓ Problem statement with characters (Phase 1)
- ✓ Database schema (Phase 2)
- ✓ Preview data (Phase 3)
- ✓ Quality validation results (Phase 4)

### In Final Package:
- ✓ All CSV files (datasets)
- ✓ PDF quality report (12 visuals)
- ✓ Excel report with answers (charts included)
- ✓ Data dictionary
- ✓ README

---

## 🎯 Phase Details

### Phase 2: Schema
- Generates database schema from problem
- Validates can answer all questions
- Returns validation score (0-10)

### Phase 3: Preview
- Generates 30 sample rows per table
- Validates FK integrity
- Shows 10 rows for review

### Phase 4: Full Generation
- User chooses size (1K-100K rows)
- Runs in background
- Creates PDF + Excel reports
- Takes 30-120 seconds

### Phase 5: Download
- Creates comprehensive ZIP
- Includes all deliverables
- Ready for analysis

---

## 🔧 Common Issues

### Server won't start
- Check: `GROQ_API_KEY` in `.env`
- Check: `pip install -r requirements.txt`

### Generation fails
- Check: Dataset size (1K-100K only)
- Check: Previous phases approved
- Check: Server logs for errors

### Download not ready
- Check: Phase 4 completed
- Check: `/api/challenge/phase4/status/{session_id}`

---

## 📚 Documentation

- **PHASE_IMPLEMENTATION_GUIDE.md** - Complete technical details
- **API_REFERENCE.md** - Full API documentation
- **ARCHITECTURE_DIAGRAM.txt** - Visual architecture
- **demo_complete_workflow.py** - Working example

---

## ✅ Verification

To verify everything works:

1. Start server: `python backend/src/main.py`
2. Run demo: `python demo_complete_workflow.py`
3. Check output: `demo_output/` folder
4. Verify files:
   - `problem_statement.json`
   - `schema.json`
   - `preview_data.json`
   - `challenge_{session_id}.zip`
5. Unzip and verify package contents

---

## 🎉 Success!

If demo completes successfully, you're ready to integrate with frontend!

**Next Steps:**
1. Build frontend UI for each phase
2. Connect to these API endpoints
3. Display progress and results
4. Let users download final package

**Questions?**
- Check documentation files
- Review demo script
- Contact: codebasics.io

---

**Version:** 2.0.0  
**Status:** Production Ready ✓  
**Implementation:** Complete ✓
