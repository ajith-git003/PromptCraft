# 🧪 Testing Your PromptCraft Application

## ✅ What We Just Built

### **Frontend (Complete!)**
- ✅ Beautiful UI with Tailwind CSS
- ✅ API integration with axios
- ✅ Real-time prompt analysis
- ✅ Loading states & error handling
- ✅ Score visualization
- ✅ Issues display with severity badges
- ✅ Suggestions list
- ✅ Metrics dashboard
- ✅ Optimized prompt display

### **Backend (Already Complete!)**
- ✅ FastAPI server with CORS
- ✅ spaCy NLP analysis
- ✅ Pydantic validation
- ✅ Dockerized

---

## 🚀 Test Locally (Option 1: Without Docker)

### **Step 1: Start Backend**

Open PowerShell/Terminal #1:
```powershell
cd C:\Users\ajith\OneDrive\Desktop\AIMLproject\promptcraft\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Test it: Open http://localhost:8000/docs in browser

---

### **Step 2: Start Frontend**

Open PowerShell/Terminal #2:
```powershell
cd C:\Users\ajith\OneDrive\Desktop\AIMLproject\promptcraft\frontend
npm start
```

Browser should auto-open to http://localhost:3000

---

### **Step 3: Test the Application**

1. **Enter a simple prompt:**
   ```
   Write a story
   ```
   Expected: Low scores, issues detected

2. **Enter a detailed prompt:**
   ```
   Write a 500-word science fiction story about a robot learning to understand human emotions, set in the year 2150. The story should be written in third-person narrative with a hopeful tone.
   ```
   Expected: High scores, fewer issues

3. **Check all features work:**
   - ✅ Loading spinner appears
   - ✅ Overall score displays
   - ✅ Score breakdown shows
   - ✅ Issues appear (if any)
   - ✅ Suggestions list shows
   - ✅ Metrics display correctly
   - ✅ Optimized prompt appears

---

## 🐳 Test with Docker (Option 2: Production-like)

### **Prerequisites**
- Install Docker Desktop: https://www.docker.com/products/docker-desktop/
- Restart computer after installation

### **Run Everything**

```powershell
cd C:\Users\ajith\OneDrive\Desktop\AIMLproject\promptcraft
docker-compose up --build
```

**First build takes ~5-10 minutes** (downloads dependencies)

Access:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

Stop with: `Ctrl+C` then `docker-compose down`

---

## 🐛 Troubleshooting

### **Frontend Error: "Failed to analyze prompt"**

**Problem**: Backend not running or wrong URL

**Fix**:
1. Check backend is running at http://localhost:8000
2. Visit http://localhost:8000/docs - should show API docs
3. Check browser console for errors (F12)

---

### **Backend Error: "Module not found: spacy"**

**Problem**: Dependencies not installed

**Fix**:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

### **CORS Error in Browser Console**

**Problem**: Backend CORS not allowing frontend

**Fix**: Backend `app/main.py` should have:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### **Frontend Won't Start: Port 3000 in use**

**Fix**:
```powershell
# Kill process using port 3000
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F

# Or use different port
set PORT=3001 && npm start
```

---

## ✨ Example Test Prompts

### **Poor Quality (Low Scores)**
```
Write something
Tell me about AI
Make a story
```

### **Good Quality (High Scores)**
```
Write a 300-word blog post explaining the benefits of electric vehicles to a general audience. Include 3 main points and use a friendly, conversational tone.

Create a step-by-step tutorial for beginners on how to set up a React development environment on Windows 11, including Node.js installation and creating a first project.

Explain the concept of machine learning to a 10-year-old using simple analogies and examples from everyday life. Keep it under 200 words.
```

---

## 📊 Expected Results

### **Poor Prompt Analysis**
- Overall Score: 30-50
- Issues: High severity
- Suggestions: Multiple improvements needed
- Metrics: Few words, low complexity

### **Good Prompt Analysis**
- Overall Score: 70-95
- Issues: Few or none
- Suggestions: Minor refinements
- Metrics: Good word count, clear structure

---

## 🎯 Success Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads in browser
- [ ] Can enter and submit prompts
- [ ] Loading spinner shows during analysis
- [ ] Results display correctly
- [ ] All score cards render
- [ ] Issues appear with severity badges
- [ ] Suggestions list populates
- [ ] Metrics show correct counts
- [ ] Optimized prompt displays
- [ ] Error messages work (test by stopping backend)

---

## 📸 What You Should See

### **1. Initial Page**
- Large hero title "✨ PromptCraft"
- Text input area
- "Analyze Prompt" button
- 3 feature cards at bottom

### **2. During Analysis**
- Button shows "Analyzing..." with spinner
- Input area disabled

### **3. Results Page**
- Large overall score (colored)
- 4 score breakdown cards
- Issues section (if any)
- Suggestions with checkmarks
- Metrics (3 columns)
- Optimized prompt in gradient box

---

## 🚀 Next Steps After Testing

Once local testing works:

1. **Push to GitHub**
   ```powershell
   git init
   git add .
   git commit -m "Complete PromptCraft application"
   git push origin main
   ```

2. **Deploy to Railway** (See DEPLOYMENT.md)
   - Takes 5-10 minutes
   - Free tier available
   - Automatic HTTPS

3. **Share your live app!** 🎉

---

## 💡 Tips

- Use Ctrl+Shift+I (F12) to open browser DevTools
- Check Network tab to see API calls
- Console shows any JavaScript errors
- Backend logs show in terminal

---

**Your app is production-ready! Time to deploy! 🚀**
