# Quick Setup: Web Search Feature

## ⚡ 3-Step Setup

### Step 1: Install Requests Library
```bash
cd backend
pip install requests
```

**Verify installation:**
```bash
python -c "import requests; print('✅ requests library installed')"
```

### Step 2: Restart Backend Server
```bash
cd backend
python src/main.py
# Server starts on http://127.0.0.1:8000
```

### Step 3: Start Frontend & Test
```bash
cd frontend_new
npm run dev
# Opens on http://localhost:3000
```

---

## 🧪 Quick Test

### Test in Browser:
1. Go to `http://localhost:3000`
2. Enter:
   - **Domain**: E-Commerce
   - **Function**: Sales
   - **Problem Statement**: "We want to improve our sales forecasting"
   - **Difficulty**: Intermediate
3. Click "Start Phase 1: Research"
4. **Wait 5-10 seconds** for web search to complete
5. You should see **2-3 real case studies** with:
   - Real URLs from the internet
   - Key insights extracted from the sources
   - Relevance score (HIGH/MEDIUM)

---

## ✅ What You'll See

### Before (Old):
```
Research Sources:
- Latest E-Commerce Industry Report 2025
  https://industry-report.example.com/e-commerce
  [HIGH]
```

### After (New):
```
📚 Data Analytics Case Studies:

┌─────────────────────────────────────┐
│ Real Case Study: How Company X...   │ [HIGH]
│ https://realdomain.com/case-study   │
│                                     │
│ Key Insights:                       │
│ • Real sales forecasting methods    │
│ • Machine learning implementation   │
│ • Achieved 25% accuracy improvement │
└─────────────────────────────────────┘

[More case studies...]
```

---

## 🔍 How It Works (Behind the Scenes)

1. **User enters domain & function**
2. **Backend searches DuckDuckGo** for: `"{domain} {function} data analytics case study"`
3. **Extracts top 3 results** with real URLs
4. **Displays them beautifully** in the UI
5. **Problem statement** generated using real case study insights
6. **If search fails**: Automatically uses fallback sources (so app never breaks!)

---

## 🚨 Troubleshooting

### ❌ "No sources found" or taking too long?

**Check 1: Internet Connection**
```bash
ping google.com
# Should respond with packets
```

**Check 2: Requests Library**
```bash
pip list | grep requests
# Should show: requests 2.31.0+ (or similar)
```

**Check 3: Backend Logs**
Look in backend console for:
- `"Conducting research for E-Commerce - Sales"`
- `"Searching for case studies"`
- Should see either: `"Found X case studies"` or `"No web search results, using fallback"`

**Check 4: Try Different Domain**
Some domains might not return results:
- ✅ **Works well**: E-Commerce, Healthcare, Banking, Retail, Manufacturing
- ❓ **Try these first** if having issues

### ✅ If showing fallback sources:
- This is **normal and OK!**
- Application still works perfectly
- Fallback sources are realistic and useful
- Web search will work when connection is restored

---

## 📊 Example Domains to Try

```
✅ E-Commerce + Sales
✅ Healthcare + Operations
✅ Banking + Lending
✅ Retail + Inventory
✅ Manufacturing + Production
✅ Insurance + Claims
✅ Logistics + Distribution
✅ Finance + Risk Management
```

---

## 🎯 Key Files Changed

1. **Backend**: `backend/src/problem_generator.py`
   - Added `_search_case_studies()` method
   - Added `_parse_duckduckgo_results()` method
   - Added `_generate_fallback_sources()` method
   - Updated `conduct_research()` logic

2. **Frontend**: `frontend_new/src/app/page.tsx`
   - Enhanced research sources display
   - Better visual hierarchy for case studies
   - Added key insights section

---

## 📝 Dependencies

**New Dependency Added:**
```
requests==2.31.0+
```

**Already Installed:**
```
Groq SDK          (for AI)
FastAPI           (backend)
React/Next.js     (frontend)
```

---

## 🎉 You're Done!

Just run:
```bash
# Terminal 1: Backend
cd backend && python src/main.py

# Terminal 2: Frontend
cd frontend_new && npm run dev
```

Visit `http://localhost:3000` and start a challenge! 🚀

The web search will automatically fetch real case studies for your selected domain and function.

---

## 💡 Pro Tips

1. **Better Search Results**: Be specific with function names
   - ✅ "Sales" instead of "Revenue"
   - ✅ "Operations" instead of "Processes"

2. **Wait for Search**: First search might take 5-10 seconds (DuckDuckGo is responsive but needs time)

3. **Check Logs**: If uncertain, check backend console for search progress

4. **Network Issues**: If behind VPN/proxy, DuckDuckGo might block. Use fallback sources (automatic!)

---

**Enjoy your new research-driven data challenges with real web search!** 🎓
