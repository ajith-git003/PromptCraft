# Enhanced Intent Classification - Quick Start Guide

## What Changed?

Your PromptCraft tool now has **enhanced intent classification** that provides:
- 🎯 **Sub-intent detection** (e.g., "reporting" vs "strategy" vs "optimization")
- 📊 **Data context awareness** (knows if you have data or need to collect it)
- 👥 **Stakeholder detection** (identifies recipients like "manager")
- 💡 **Smart suggestions** tailored to your specific use case
- 📈 **Confidence scoring** for classification accuracy

## Quick Test

### 1. Test the Intent Classifier
```powershell
python backend/app/intent_classifier.py
```
This will run test cases and show you how different queries are classified.

### 2. Test the Enhanced Prompt Engine
```powershell
python backend/test_enhanced_intent.py
```
Shows how the enhanced system generates different STOK outputs.

### 3. Run Comprehensive Comparison
```powershell
python backend/test_comparison.py
```
Displays all improvements and validates test cases.

## Start Your Server

```powershell
cd backend
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## Test with Real Query

Open PowerShell and run:
```powershell
$body = @{
    prompt = "create a report from this data for meta ads so I can send it to my manager"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/generate" -Method Post -Body $body -ContentType "application/json"
```

### Expected Output:
```json
{
  "original_prompt": "create a report from this data for meta ads so I can send it to my manager",
  "intent": "marketing",
  "sub_intent": "reporting",
  "confidence_score": 0.9,
  "context": {
    "has_data": true,
    "stakeholder": "manager",
    "query_length": 17
  },
  "suggestions": [
    "Specify key metrics to analyze",
    "Define the reporting time period",
    "Mention comparison benchmarks"
  ],
  "enhanced_prompt": "...",
  "structured_prompt": { ... }
}
```

## Example Use Cases

### 1. Marketing Report (with data)
**Query:** "create a report from this data for meta ads so I can send it to my manager"

**Detection:**
- Intent: marketing
- Sub-intent: reporting
- Has Data: ✓
- Stakeholder: manager

**Output:** Tailored STOK for creating a report from existing data

---

### 2. Audience Targeting
**Query:** "who should be my target audience for fitness supplements"

**Detection:**
- Intent: marketing
- Sub-intent: audience_targeting
- Has Data: ✗

**Output:** STOK for creating detailed audience personas

---

### 3. Campaign Optimization
**Query:** "how do I optimize my facebook ad campaign to reduce CPA"

**Detection:**
- Intent: marketing
- Sub-intent: optimization

**Output:** STOK focused on optimization strategies and A/B testing

---

### 4. Marketing Strategy
**Query:** "what's the best marketing strategy for launching a new product"

**Detection:**
- Intent: marketing
- Sub-intent: strategy

**Output:** Comprehensive strategic planning STOK

## Files You Can Explore

1. **`backend/app/intent_classifier.py`** - The enhanced classifier logic
2. **`backend/app/prompt_engine.py`** - Updated prompt generation with sub-intents
3. **`backend/test_comparison.py`** - See before/after comparison
4. **`ENHANCED_INTENT_IMPLEMENTATION.md`** - Full technical documentation

## Frontend Integration (Optional)

If you want to display the new information in your frontend, update your UI to show:

```javascript
// In your frontend code
const result = await generatePrompt(userQuery);

// New fields available:
console.log(result.sub_intent);        // e.g., "reporting"
console.log(result.confidence_score);  // e.g., 0.9
console.log(result.context);           // { has_data: true, stakeholder: "manager", ... }

// Display sub-intent badge
<Badge>Sub-intent: {result.sub_intent}</Badge>

// Show confidence indicator
<ProgressBar value={result.confidence_score * 100} />

// Display context insights
{result.context.has_data && <Tag>Has Data</Tag>}
{result.context.stakeholder && <Tag>For: {result.context.stakeholder}</Tag>}
```

## Troubleshooting

### Issue: Import Error
```
ModuleNotFoundError: No module named 'app.intent_classifier'
```
**Solution:** Make sure you're running from the correct directory:
```powershell
cd backend
python -m app.intent_classifier  # Use module syntax
```

### Issue: Server Won't Start
```
ERROR:    Error loading ASGI app...
```
**Solution:** Check that all imports are working:
```powershell
cd backend
python -c "from app.main import app; print('OK')"
```

### Issue: Old Confidence Score Type
If frontend expects integer confidence but gets float, update your frontend:
```javascript
// Old
const confidence = result.confidence_score; // int (0-100)

// New
const confidence = Math.round(result.confidence_score * 100); // convert to percentage
```

## What's Next?

1. ✅ **Test the implementation** - Run all test scripts
2. ✅ **Start the server** - Verify API works
3. ✅ **Try different queries** - See how sub-intents are detected
4. 📱 **Update frontend** (optional) - Display new classification info
5. 📊 **Monitor results** - Compare with reference tool outputs

## Need Help?

Check these files:
- `ENHANCED_INTENT_IMPLEMENTATION.md` - Full technical details
- `backend/test_comparison.py` - See working examples
- `OUTPUT_COMPARISON.md` - Original requirements

## Success Metrics

Your implementation is working correctly if:
- ✓ Intent classifier detects "reporting" for report-related queries
- ✓ Data context is detected when phrases like "from this data" are used
- ✓ Stakeholder is extracted from "send to my manager"
- ✓ Different STOK templates are generated for different sub-intents
- ✓ All test cases pass

---

**🎉 Congratulations!** Your PromptCraft tool now has enhanced intent classification that provides more accurate and contextual prompt improvements.
