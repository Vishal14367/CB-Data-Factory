# Demo Walkthrough - Step by Step

## What You're About to See

A complete end-to-end data generation pipeline that:
1. **Takes your problem** (domain, function, problem statement)
2. **Generates a database schema** using AI
3. **Creates realistic data** with proper relationships
4. **Validates quality** automatically
5. **Exports CSV files** you can use

All in **one simple Python script**. ⚡

---

## Step-by-Step Walkthrough

### Step 1: Start the Demo

**Double-click:** [RUN_DEMO.bat](RUN_DEMO.bat)

You'll see:
```
========================================
  Simple Demo - Data Challenge Generator
========================================

This will:
1. Auto-install required packages
2. Generate schema with AI
3. Create realistic dataset
4. Run quality checks
5. Save CSV files

Press any key to start...
```

Press any key to continue.

---

### Step 2: Enter Your Challenge Details

The script will prompt you:

```
======================================================================
  DATA CHALLENGE GENERATOR - SIMPLE DEMO
======================================================================

Enter your challenge details:
Domain (e.g., E-Commerce):
```

**You can:**
- Enter "E-Commerce" (or Banking, Healthcare, etc.)
- Press Enter to use the default

```
Function (e.g., Sales):
```

**You can:**
- Enter "Sales & Marketing" (or Operations, Finance, etc.)
- Press Enter to use the default

```
Problem (or press Enter for default):
```

**You can:**
- Enter a business problem description
- Or press Enter for the default (retail customer retention)

```
Number of rows (default 1000):
```

**You can:**
- Enter "5000" for more data
- Press Enter for 1,000 rows

**Example inputs:**
```
Domain: E-Commerce
Function: Sales & Marketing
Problem: [Enter - uses default]
Number of rows: [Enter - uses 1000]
```

---

### Step 3: Watch the Magic Happen

As the script runs, you'll see progress:

```
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
```

This takes **10-30 seconds** depending on your internet speed (Groq API call).

---

### Step 4: See Your Results

```
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

### Step 5: Check the Generated Files

The script creates a new folder: **demo_output/**

You'll find:

**1. dim_customers.csv**
```
customer_id,customer_name,region,signup_date
CUST0001,Jennifer Smith,North,2019-03-15
CUST0002,Michael Johnson,South,2019-05-22
CUST0003,Sarah Williams,East,2019-07-10
...
```

**2. dim_products.csv**
```
product_id,product_name,category,price,stock
PROD0001,Laptop Computer,Electronics,899.99,150
PROD0002,Office Chair,Furniture,199.99,450
PROD0003,Desk Lamp,Furniture,45.99,1200
...
```

**3. fact_orders.csv**
```
order_id,customer_id,product_id,order_date,quantity,total_amount
ORD0001,CUST0001,PROD0001,2019-08-01,1,899.99
ORD0002,CUST0002,PROD0002,2019-08-02,2,399.98
ORD0003,CUST0003,PROD0003,2019-08-03,5,229.95
...
```

**4. schema.json**
```json
{
  "tables": [
    {
      "name": "dim_customers",
      "columns": [
        {
          "name": "customer_id",
          "type": "string",
          "is_pk": true
        },
        ...
      ]
    },
    ...
  ]
}
```

**5. summary.json**
```json
{
  "generated_at": "2025-02-06T15:30:45.123456",
  "quality_score": 9.2,
  "tables": {
    "dim_customers": 100,
    "dim_products": 150,
    "fact_orders": 1000
  },
  "total_rows": 1250
}
```

---

## What the Data Represents

This is a **realistic e-commerce scenario**:

- **dim_customers**: Customer master data (100 unique customers)
- **dim_products**: Product catalog (150 products)
- **fact_orders**: Customer transactions (1,000 orders)

**Key properties:**

✅ **Foreign Key Integrity**
- Every order.customer_id exists in dim_customers
- Every order.product_id exists in dim_products
- No orphan records

✅ **Realistic Distributions**
- Customer names are fictional but realistic
- Product prices vary realistically
- Order quantities follow real-world patterns (most 1-3 items)
- Dates spread across 2019-2024

✅ **Data Quality Issues** (intentional for learning)
- 3% missing values in optional columns
- 5% outliers (some very large orders)
- Occasional duplicate-looking records
- Some inconsistent formatting

✅ **Relationships**
- Customers can have multiple orders
- Products can appear in multiple orders
- Proper cardinality (1:N relationships)

---

## Quality Checks Performed

The demo automatically runs these checks:

1. **No Empty Tables** ✓
   - All tables have data

2. **Foreign Key Integrity** ✓
   - All child rows reference existing parents
   - Zero orphan records

3. **Null Percentages** ✓
   - Acceptable null counts (usually 0-5%)

4. **Duplicate Primary Keys** ✓
   - All primary keys are unique

---

## Quality Score Interpretation

The script calculates a **Quality Score from 0-10**:

| Score | Status | Meaning |
|-------|--------|---------|
| 8.0-10.0 | ✅ APPROVED | Ready to use |
| 6.0-7.9 | ⚠️ NEEDS REVIEW | Mostly good, minor issues |
| 0-5.9 | ❌ REJECTED | Has problems |

**Why you'll likely get 8-10:**
- Proper relationships
- No foreign key violations
- Acceptable null rates
- Realistic data

---

## Next: Use the Data!

Once you have the CSV files, you can:

✅ **Load into Excel** - Open `.csv` files directly
✅ **Import to SQL** - Load into PostgreSQL, MySQL, SQL Server
✅ **Analyze with Python** - Use pandas, numpy, etc.
✅ **Create in Power BI** - Import for dashboarding
✅ **Test queries** - Practice SQL on real schema
✅ **Create challenges** - Use as training datasets

---

## What Happens Behind the Scenes?

**For the curious:**

1. **Schema Generation (Groq AI)**
   - Your problem statement sent to Groq's API
   - AI generates appropriate tables, columns, relationships
   - JSON response parsed and validated
   - Takes ~5-10 seconds

2. **Data Generation**
   - For each table, generates rows
   - Respects primary key format (CUST0001, etc.)
   - Picks foreign key values from parent tables
   - Generates realistic values per datatype
   - Takes ~5 seconds

3. **Quality Validation**
   - Checks FK integrity (no orphans)
   - Validates null percentages
   - Checks for duplicate PKs
   - Calculates score
   - Takes ~1 second

4. **Export**
   - Converts to pandas DataFrames
   - Exports to CSV format
   - Saves schema and metadata
   - Takes ~1 second

---

## Troubleshooting

**"Python was not found"**
- Install from: https://www.python.org/downloads/
- During install, check ☑️ "Add Python to PATH"

**"ModuleNotFoundError"**
- Script auto-installs packages
- If it fails, check internet connection
- Or manually: `pip install groq faker pandas`

**"API key error"**
- Groq key is embedded in the script
- If error, check your internet connection
- Contact support if persistent

**"No CSV files generated"**
- Check the `demo_output/` folder exists
- Run demo again with verbose output

---

## What's Next?

### If you like the demo:

**Option A: Use as-is**
- CSV files are ready to use
- Import into your tools
- Create challenges from this template

**Option B: Build the Full Version**
- More advanced data generation
- 30+ quality validation checks
- 17-page PDF reports with charts
- Web UI for easy use
- See me to build this

### If you want improvements:

Tell me what you need:
- More rows of data? ✓
- Different domain/function? ✓
- More complex relationships? ✓
- Specific data quality issues? ✓
- Seasonal patterns? ✓
- Event impacts (like COVID)? ✓

I can customize the demo or build the full version!

---

## You're Ready! 🚀

**Everything is set up and ready to go.**

Just double-click [RUN_DEMO.bat](RUN_DEMO.bat) and see it work!

Let me know when you've tested it, and I can help with:
- Running the full application
- Customizing the data
- Building additional features
- Deploying for real use
