# PromptCraft Startup Script
# Run this to start both backend and frontend

Write-Host "🚀 Starting PromptCraft..." -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
$projectRoot = "C:\Users\ajith\OneDrive\Desktop\AIMLproject\promptcraft"
if (-not (Test-Path $projectRoot)) {
    Write-Host "❌ Error: Project directory not found!" -ForegroundColor Red
    exit 1
}

Set-Location $projectRoot

# Start Backend
Write-Host "📡 Starting Backend API..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\backend'; .\venv\Scripts\Activate.ps1; Write-Host '✅ Backend starting on http://localhost:8000' -ForegroundColor Green; Write-Host '📖 API Docs: http://localhost:8000/docs' -ForegroundColor Yellow; uvicorn app.main:app --reload"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "🎨 Starting Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\frontend'; Write-Host '✅ Frontend starting on http://localhost:3000' -ForegroundColor Green; npm start"

Write-Host ""
Write-Host "✨ PromptCraft is starting!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access the app at: http://localhost:3000" -ForegroundColor Yellow
Write-Host "📖 API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop the servers" -ForegroundColor Gray
