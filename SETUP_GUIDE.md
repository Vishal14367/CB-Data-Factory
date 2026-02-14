# Setup Guide - Foundation Phase

## Step 1: Install Python

1. **Download Python 3.10 or higher:**
   - Go to: https://www.python.org/downloads/
   - Download the latest Python 3.10+ installer for Windows
   - **IMPORTANT:** During installation, check "Add Python to PATH"

2. **Verify installation:**
   ```bash
   python --version
   ```
   Should show: `Python 3.10.x` or higher

## Step 2: Install Node.js

1. **Download Node.js 18 or higher:**
   - Go to: https://nodejs.org/
   - Download the LTS version
   - Run the installer (all defaults are fine)

2. **Verify installation:**
   ```bash
   node --version
   npm --version
   ```

## Step 3: Backend Setup

1. **Open terminal/command prompt in the `backend` folder**

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   venv\Scripts\activate
   ```
   You should see `(venv)` in your prompt

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Verify .env file exists with Groq API key:**
   - File should already exist at `backend/.env`
   - Should contain: `GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE`

## Step 4: Test Schema Generation

1. **Run the test script:**
   ```bash
   python test_schema.py
   ```

2. **Expected output:**
   ```
   ============================================================
   SCHEMA GENERATION TEST
   ============================================================
   Domain: E-Commerce
   Function: Sales & Marketing
   ...
   Generating schema with Groq AI...

   ============================================================
   SCHEMA GENERATED SUCCESSFULLY!
   ============================================================

   Tables: 4
     - dim_customers: 6 columns, PK=customer_id
     - dim_products: 5 columns, PK=product_id
     - dim_dates: 3 columns, PK=date_id
     - fact_orders: 10 columns, PK=order_id

   Relationships: 3
     - fact_orders.customer_id -> dim_customers.customer_id (1:N)
     ...

   ✅ Schema saved to: backend/output/test_schema.json
   ```

3. **If successful**, you'll see a `test_schema.json` file in `backend/output/` folder

## Step 5: Start Backend Server

1. **In backend folder (with venv activated):**
   ```bash
   cd src
   python main.py
   ```

   OR use the batch file:
   ```bash
   start.bat
   ```

2. **Expected output:**
   ```
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

3. **Test the API:**
   - Open browser: http://127.0.0.1:8000
   - You should see: `{"status":"healthy","service":"Data Challenge Generator",...}`
   - API docs: http://127.0.0.1:8000/docs

## Step 6: Frontend Setup

1. **Open NEW terminal/command prompt in the `frontend` folder**

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start dev server:**
   ```bash
   npm run dev
   ```

   OR use the batch file:
   ```bash
   start.bat
   ```

4. **Expected output:**
   ```
   VITE v6.0.3  ready in xxx ms

   ➜  Local:   http://localhost:3000/
   ➜  press h + enter to show help
   ```

## Step 7: Test End-to-End

1. **Open browser:** http://localhost:3000

2. **Fill in the form:**
   - Domain: E-Commerce
   - Function: Sales & Marketing
   - Problem Statement: (paste a business problem - minimum 100 characters)
   - Click "Generate & Validate"

3. **Expected flow:**
   - Form submits → Loading spinner appears
   - After 10-20 seconds → Results show:
     - Quality Score: 8.5 / 10
     - Status: ✅ Approved
     - Download PDF Report button

4. **Check backend logs:**
   - You should see schema generation logs
   - Check `backend/output/` folder for session files

## Troubleshooting

### Python not found
- Reinstall Python and CHECK "Add to PATH"
- Restart terminal after installation
- Try `py` instead of `python`

### pip install fails
- Make sure virtual environment is activated (`(venv)` in prompt)
- Try: `python -m pip install --upgrade pip` first
- Then retry: `pip install -r requirements.txt`

### Groq API error
- Check `.env` file has correct API key
- No quotes, no spaces around the key
- Check internet connection

### Frontend won't start
- Make sure Node.js is installed: `node --version`
- Delete `node_modules` folder and `package-lock.json`
- Retry: `npm install`

### Backend/Frontend can't connect
- Make sure backend is running on port 8000
- Check backend terminal for errors
- CORS is configured for localhost:3000

## What's Working Now

✅ **Backend:**
- FastAPI server with CORS
- Schema generation with Groq AI
- API endpoints for challenge creation
- Background task processing
- Session management

✅ **Frontend:**
- Input form with validation
- API integration
- Progress display
- Results display
- Clean UI with brand colors

🚧 **In Progress:**
- Data generation engine
- QA validation engine
- PDF report generation

## Next Development Steps

1. **Data Generator** - Create realistic datasets from schemas
2. **QA Validator** - Run 6 categories of quality checks
3. **PDF Report** - Generate 17-page report with charts
4. **End-to-End Pipeline** - Wire everything together

## Files Overview

```
backend/
├── .env                    # ✅ Has Groq API key
├── requirements.txt        # ✅ Updated for Groq
├── test_schema.py         # ✅ Test script
├── start.bat              # ✅ Quick start script
└── src/
    ├── main.py            # ✅ FastAPI app with pipeline
    ├── config.py          # ✅ Updated for Groq
    ├── models.py          # ✅ All data models
    ├── schema_generator.py # ✅ NEW - AI schema generation
    ├── data_generator.py   # 🚧 TODO
    ├── qa_validator.py     # 🚧 TODO
    └── pdf_report.py       # 🚧 TODO

frontend/
├── package.json           # ✅ React + Vite
├── start.bat             # ✅ Quick start script
└── src/
    ├── App.jsx           # ✅ Complete input form + results
    └── main.jsx          # ✅ React entry
```

## Quick Commands Reference

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python test_schema.py      # Test schema generation
cd src && python main.py   # Start server

# Frontend
cd frontend
npm install
npm run dev               # Start dev server

# Check what's running
# Backend: http://127.0.0.1:8000
# Frontend: http://localhost:3000
# API Docs: http://127.0.0.1:8000/docs
```
