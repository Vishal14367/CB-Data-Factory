# 🚀 Simple Demo - No Setup Required!

## What This Is

A **single-file Python script** that demonstrates the core Data Challenge Generator functionality:

✅ AI-powered schema generation (using Groq)
✅ Realistic data generation with FK integrity
✅ Quality validation checks
✅ CSV export

**No complex setup. No frontend. No backend servers. Just one script.**

---

## How to Run

### Option 1: Double-Click (Easiest)

1. **Double-click:** [RUN_DEMO.bat](RUN_DEMO.bat)
2. Enter your challenge details (or press Enter for defaults)
3. Wait 10-30 seconds
4. Check `demo_output/` folder for CSV files!

### Option 2: Command Line

```bash
python demo_simple.py
```

---

## What It Does

```
1️⃣ You enter:
   • Domain (e.g., "E-Commerce")
   • Function (e.g., "Sales & Marketing")
   • Problem statement
   • Number of rows

2️⃣ AI generates database schema:
   • 3-4 related tables
   • Columns with proper types
   • Foreign key relationships
   • Business rules

3️⃣ System generates realistic data:
   • FK integrity (no orphans)
   • Realistic distributions (not uniform)
   • 5% outliers
   • 3% missing values
   • Weighted categories

4️⃣ Quality checks run automatically:
   • FK integrity validation
   • Null percentage checks
   • Duplicate PK detection
   • Calculates quality score (0-10)

5️⃣ Outputs saved to demo_output/:
   • {table_name}.csv for each table
   • schema.json
   • summary.json
```

---

## Example Output

```
demo_output/
├── dim_customers.csv        (100 rows × 4 columns)
├── dim_products.csv         (150 rows × 5 columns)
├── fact_orders.csv          (1,000 rows × 8 columns)
├── schema.json              (Database structure)
└── summary.json             (Quality score, metadata)
```

**Quality Score:** 8.7 / 10 ✅ APPROVED

---

## Requirements

**Only Python 3.8+ is needed.** Everything else auto-installs.

The script will automatically install:
- `groq` (AI API)
- `faker` (realistic fake data)
- `pandas` (data manipulation)

---

## Sample Run

```
======================================================================
  DATA CHALLENGE GENERATOR - SIMPLE DEMO
======================================================================

Enter your challenge details:
Domain (e.g., E-Commerce): E-Commerce
Function (e.g., Sales): Sales & Marketing
Problem (or press Enter for default): [Enter]
Number of rows (default 1000): [Enter]

======================================================================

📋 Generating database schema with AI...
✅ Generated 3 tables

📊 Generating 1,000 rows of data...
  - Generating dim_customers...
  - Generating dim_products...
  - Generating fact_orders...
✅ Generated 1,250 total rows

🔍 Running quality checks...
✅ All checks passed!

💾 Saving results to demo_output/...
  ✅ dim_customers.csv (100 rows)
  ✅ dim_products.csv (150 rows)
  ✅ fact_orders.csv (1000 rows)

📁 All files saved to: C:\...\CB Data Factory\demo_output\

======================================================================
  RESULTS
======================================================================
✅ Quality Score: 9.2 / 10
🎉 Status: APPROVED

📊 Generated 3 tables
   • dim_customers: 100 rows × 4 columns
   • dim_products: 150 rows × 5 columns
   • fact_orders: 1,000 rows × 8 columns

======================================================================
Demo complete! Check the demo_output/ folder for CSV files.
======================================================================
```

---

## What's Different from Full Version?

This demo shows **core functionality only**:

| Feature | Demo | Full Version |
|---------|------|--------------|
| Schema Generation | ✅ | ✅ |
| Data Generation | ✅ (simplified) | ✅ (advanced) |
| Quality Checks | ✅ (4 checks) | ✅ (30+ checks) |
| PDF Report | ❌ | ✅ (17 pages with charts) |
| Web UI | ❌ | ✅ (React frontend) |
| Intentional Issues | ❌ | ✅ (controlled anomalies) |
| Event Simulation | ❌ | ✅ (COVID dips, etc.) |
| KPI Tracking | ❌ | ✅ |
| Chatbot Refinement | ❌ | ✅ |

---

## Troubleshooting

**"Python was not found"**
- Install Python from: https://www.python.org/downloads/
- During install, check ☑️ "Add Python to PATH"
- Restart terminal/IDE

**"ModuleNotFoundError"**
- The script auto-installs packages
- If it fails, manually run: `pip install groq faker pandas`

**"API key error"**
- The Groq API key is embedded in the script
- If it stops working, get a free key at: https://console.groq.com/

**"Generation failed"**
- Check your internet connection (needs to call Groq API)
- Try again with a simpler problem statement

---

## Next Steps

Once you see this demo working, we can:

1. **Build the full version** with PDF reports and web UI
2. **Add more sophisticated data generation** (events, trends, seasonality)
3. **Implement the complete QA framework** (30+ validation checks)
4. **Create the 17-page PDF report** with visualizations

But this demo proves the core concept works! 🎉

---

## Files in This Demo

- `demo_simple.py` - Single-file implementation (all code)
- `RUN_DEMO.bat` - Double-click runner (Windows)
- `demo_output/` - Generated CSV files (created after first run)

That's it! No complex setup, no multiple servers, no configuration files.
