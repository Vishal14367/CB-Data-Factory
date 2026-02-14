# Phase 1 Testing & Demo Guide
**Ready to Test:** ✅ YES
**Version:** 2.0.0
**Last Updated:** February 6, 2025

---

## Quick Test Scenarios

### Scenario 1: E-Commerce Sales Challenge

**Phase 0: Configuration**
```
Domain: E-Commerce
Function: Sales & Marketing
Problem Context: Our online store has been losing repeat customers.
We need to understand why retention is declining and what we can do about it.
Skill Level: Intermediate
Dataset Size: 10,000 rows
Data Structure: Normalized (3-5 tables)
Primary Questions: Which customer segments are most likely to churn?
What patterns predict a customer's first repeat purchase?
```

**Expected Results:**
- ✅ Phase 0 validation passes (domain + function + 100+ char context)
- ✅ "Start Phase 1: Research" button enabled
- ✅ Click triggers research API call
- ✅ Research shows E-Commerce + Sales sources
- ✅ Problem statement generated with:
  - Company name (e.g., "ShopSphere")
  - 300-400 word problem description
  - **ALL THREE CHARACTER MENTIONS** (Peter, Tony, Bruce) with highlights
  - 6 analytical questions
  - Ends with "Imagine yourself as Peter Pandey..."
- ✅ Character highlighting visible in green/blue/purple
- ✅ "Approve & Continue" button transitions to Phase 2

---

### Scenario 2: Healthcare Operations Challenge

**Phase 0: Configuration**
```
Domain: Healthcare
Function: Operations
Problem Context: Hospital readmission rates are higher than industry benchmarks.
We need to identify at-risk patients and improve discharge procedures.
Skill Level: Beginner
Dataset Size: 5,000 rows
Data Structure: Denormalized (single table)
Primary Questions: What are the main risk factors for readmission?
```

**Expected Results:**
- ✅ Research finds Healthcare + Operations sources
- ✅ Problem mentions healthcare-specific KPIs
- ✅ Fewer columns (Beginner = 15)
- ✅ Single denormalized table structure
- ✅ 5 questions (Beginner level)
- ✅ Character highlighting works the same

---

### Scenario 3: Banking Finance Challenge

**Phase 0: Configuration**
```
Domain: Banking & Finance
Function: Finance & Accounting
Problem Context: Loan default rates increasing in commercial portfolio.
Need to predict defaults early and improve risk assessment.
Skill Level: Advanced
Dataset Size: 25,000 rows
Data Structure: Normalized (3-5 tables)
```

**Expected Results:**
- ✅ Research finds Banking + Finance trends
- ✅ Problem complex with financial constraints
- ✅ More columns (Advanced = 30)
- ✅ 7 questions (Advanced level)
- ✅ References to recent banking regulations

---

## Manual Testing Checklist

### ✅ Frontend UI Testing

#### Phase 0: Configuration
- [ ] Domain field accepts text input
- [ ] Function field accepts text input
- [ ] Problem Context field shows character count
- [ ] Problem Context field requires minimum 100 chars
- [ ] Skill level selector shows 3 options
- [ ] Dataset size selector shows 5 options
- [ ] Data structure shows 2 options
- [ ] "Start Phase 1" button disabled until valid
- [ ] "Start Phase 1" button enabled when valid

#### Phase Progress Bar
- [ ] Shows all 6 phases in order
- [ ] Phase 0 highlighted in blue
- [ ] Current phase number shown
- [ ] Completed phases show checkmarks
- [ ] Bar is sticky (stays visible when scrolling)
- [ ] Can click previous phases to navigate back

#### Phase 1: Research Display
- [ ] Research section shows sources
- [ ] Each source shows title, URL, relevance badge
- [ ] Key insights listed for each source
- [ ] KPI count displayed
- [ ] Domain insights displayed
- [ ] Loading state shows while generating

#### Phase 1: Problem Statement Display
- [ ] Company name shows in header
- [ ] Problem title displays
- [ ] Full problem statement visible
- [ ] **Character highlighting visible**:
  - [ ] Peter Pandey in green (#20C997)
  - [ ] Tony Sharma in blue (#3B82F6)
  - [ ] Bruce Hariyali in purple (#6F53C1)
- [ ] Analytical questions numbered 1-7
- [ ] "Regenerate" button available
- [ ] "Approve & Continue" button available

#### Phase 1: User Actions
- [ ] Click "Regenerate" remakes problem statement
- [ ] Loading spinner shows during regeneration
- [ ] "Approve & Continue" locks problem
- [ ] Transitioning to Phase 2 shows placeholder
- [ ] Can navigate back to Phase 0 or 1

---

### ✅ Backend API Testing

#### Test 1: Research Endpoint
```bash
curl -X POST http://localhost:8000/api/challenge/phase1/research \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "E-Commerce",
    "function": "Sales & Marketing",
    "problem_statement": "Our online store has been losing repeat customers over the past year. We need comprehensive data to analyze retention trends and identify what factors influence repeat purchases.",
    "skill_level": "Intermediate",
    "dataset_size": 10000,
    "data_structure": "Normalized",
    "primary_questions": "Which customer segments are most likely to churn?"
  }'
```

**Expected Response:**
```json
{
  "session_id": "uuid-string",
  "status": "research_complete",
  "research": {
    "domain": "E-Commerce",
    "function": "Sales & Marketing",
    "sources": [
      {
        "title": "...",
        "url": "...",
        "relevance": "high",
        "key_insights": [...]
      }
    ],
    "domain_insights": [...],
    "identified_kpis": [...]
  }
}
```

#### Test 2: Problem Generation Endpoint
```bash
SESSION_ID="<from-test-1>"
curl -X POST "http://localhost:8000/api/challenge/phase1/generate-problem?session_id=${SESSION_ID}" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "E-Commerce",
    "function": "Sales & Marketing",
    "problem_statement": "...",
    "skill_level": "Intermediate",
    "dataset_size": 10000,
    "data_structure": "Normalized",
    "primary_questions": "..."
  }'
```

**Expected Response:**
```json
{
  "session_id": "uuid",
  "status": "problem_generated",
  "problem_statement": {
    "company_name": "ShopSphere",
    "title": "Reversing the Retention Crisis",
    "statement": "...(includes Peter Pandey, Tony Sharma, Bruce Hariyali mentions)...",
    "character_positions": {
      "Peter Pandey": [10, 245, 523],
      "Tony Sharma": [145, 367],
      "Bruce Hariyali": [280]
    },
    "analytical_questions": [...]
  }
}
```

**Validation:**
- ✅ Verify all 3 characters mentioned (use character_positions)
- ✅ Count analytical questions (5-7 expected)
- ✅ Check statement length (300-400 words)
- ✅ Verify ends with "Imagine yourself as Peter Pandey..."

#### Test 3: Approval Endpoint
```bash
SESSION_ID="<from-test-2>"
curl -X POST "http://localhost:8000/api/challenge/phase1/approve?session_id=${SESSION_ID}"
```

**Expected Response:**
```json
{
  "session_id": "uuid",
  "status": "phase1_approved",
  "message": "Problem statement approved. Ready for Phase 2: Schema Generation.",
  "next_phase": "phase2"
}
```

#### Test 4: Status Endpoint
```bash
SESSION_ID="<any-session>"
curl -X GET "http://localhost:8000/api/challenge/phase1/status/${SESSION_ID}"
```

**Expected Response:**
```json
{
  "session_id": "uuid",
  "phase": "phase1",
  "status": "problem_generated",
  "problem_approved": true/false,
  "has_research": true/false,
  "has_problem": true/false
}
```

---

## Character Highlighting Validation

### How to Verify Character Highlighting

1. **Generate a problem statement** (Phase 1B)
2. **Check the HTML/DOM** for character names:
   ```javascript
   // In browser console:
   document.querySelectorAll('span[style*="font-weight: 700"]')
   ```
3. **Verify each character appears** with correct styling:
   - Peter Pandey: background-color rgb(32, 201, 151) [green]
   - Tony Sharma: background-color rgb(59, 130, 246) [blue]
   - Bruce Hariyali: background-color rgb(111, 83, 193) [purple]

4. **Test case-insensitivity**:
   - Should match "peter pandey", "PETER PANDEY", "Peter Pandey"

5. **Count occurrences**:
   - Use `character_positions` in API response
   - Verify each character appears at least once

---

## Performance Testing

### Measure API Response Times

```bash
# Time the research endpoint
time curl -X POST http://localhost:8000/api/challenge/phase1/research \
  -H "Content-Type: application/json" \
  -d '{...}'

# Expected: 5-10 seconds (includes web search)
```

```bash
# Time the problem generation endpoint
time curl -X POST http://localhost:8000/api/challenge/phase1/generate-problem \
  -H "Content-Type: application/json" \
  -d '{...}'

# Expected: 3-5 seconds
```

**Targets:**
- Research API: < 10 seconds ✅
- Problem generation: < 5 seconds ✅
- Character detection: < 100ms ✅
- Frontend rendering: < 200ms ✅

---

## Error Scenario Testing

### Test 1: Missing Session
```bash
curl -X GET "http://localhost:8000/api/challenge/phase1/status/invalid-session-id"
```
**Expected:** 404 error with "Session not found"

### Test 2: Invalid Domain
```bash
curl -X POST http://localhost:8000/api/challenge/phase1/research \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "",
    "function": "Sales",
    ...
  }'
```
**Expected:** Frontend validation blocks submission

### Test 3: Problem Not Found
```bash
SESSION_ID="<fresh-session-with-no-problem>"
curl -X POST "http://localhost:8000/api/challenge/phase1/approve?session_id=${SESSION_ID}"
```
**Expected:** 400 error with "No problem statement found"

---

## Browser Console Testing

### Check for Console Errors
```javascript
// Should be no errors in console
console.log('Check browser developer tools console for errors');
```

### Verify Session Persistence
```javascript
// Check if session ID is maintained
const sessionId = new URLSearchParams(window.location.search).get('sessionId');
console.log('Current Session ID:', sessionId);
```

---

## Regression Testing (After Future Changes)

### Checklist for Phase 2+ Development

- [ ] Phase 1 research still returns correct sources
- [ ] Character highlighting still works after any text changes
- [ ] Phase progress bar still shows all phases
- [ ] Can still approve Phase 1 and proceed
- [ ] Session data not corrupted by new phases
- [ ] Old sessions still accessible
- [ ] No breaking changes to Phase 1 APIs

---

## Demo Script (for User Walkthrough)

### 1. Opening & Setup (2 min)
- Open http://localhost:3000
- Show Phase progress bar (all 6 phases visible)
- Explain current phase (Phase 0: Configuration)

### 2. Phase 0 Configuration (3 min)
- Fill in Domain: "E-Commerce"
- Fill in Function: "Sales & Marketing"
- Fill in Problem Context: "Online store losing repeat customers..."
- Select Skill Level: "Intermediate"
- Select Dataset Size: "10,000 rows"
- Select Data Structure: "Normalized"
- Show "Start Phase 1" button is now enabled

### 3. Phase 1A: Research (2-3 min)
- Click "Start Phase 1: Research"
- Show loading spinner
- Explain what's happening: "Finding domain-specific research..."
- Wait for research results to display
- Point out 3 research sources with key insights
- Highlight identified KPIs and industry challenges

### 4. Phase 1B: Problem Generation (2-3 min)
- Wait for problem statement to generate (or click "Regenerate" if needed)
- Show generated problem statement
- **Highlight the three character names** with their color coding:
  - Green: Peter Pandey
  - Blue: Tony Sharma
  - Purple: Bruce Hariyali
- Show 6 analytical questions
- Explain these questions match skill level (Intermediate)

### 5. Phase 1C: Approval (1 min)
- Click "Approve & Continue"
- Show transition to Phase 2 placeholder
- Explain Phase 2 is coming next (Schema Generation)

### 6. Wrap-up (1 min)
- Summarize Phase 1 accomplishments
- Explain next phases in roadmap
- Answer questions

**Total Demo Time: ~10-15 minutes**

---

## Known Issues & Workarounds

### Issue 1: Character highlighting not showing in some fonts
**Workaround:** Font doesn't support styling, use system font
**Fix:** Verify font is loaded correctly in CSS

### Issue 2: Web search returns same results every time
**Expected:** Mock data is being used (not real web search)
**Fix:** Replace with real web search in production

### Issue 3: Session disappears after server restart
**Expected:** In-memory storage (development behavior)
**Fix:** Use Redis/database in production

---

## Success Criteria

Phase 1 is considered **successfully tested** when:

- ✅ All 4 API endpoints respond correctly
- ✅ Research returns 3+ sources
- ✅ Problem statement includes all 3 characters
- ✅ Character positions correctly identified
- ✅ Character highlighting displays in correct colors
- ✅ Approval gate works (locks problem)
- ✅ Session management works (data persists)
- ✅ Error handling works (graceful failures)
- ✅ Frontend UI displays all phases correctly
- ✅ E2E flow works (Phase 0 → Phase 1 approval)

---

## Next Testing (Phase 2)

When ready to implement Phase 2 (Schema Generation):

1. Create new endpoints:
   - `POST /api/challenge/phase2/generate-schema`
   - `POST /api/challenge/phase2/validate-schema`
   - `POST /api/challenge/phase2/approve`

2. Add schema visualization component (ERD)

3. Test E2E from Phase 0 through Phase 2

---

**END OF TESTING GUIDE**
