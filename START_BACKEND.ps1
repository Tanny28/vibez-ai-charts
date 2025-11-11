# ========================================
# VIBEZ AI - Backend Startup Script
# ========================================

Write-Host "🚀 Starting Vibez AI Backend..." -ForegroundColor Cyan
Write-Host ""

# Navigate to backend directory
Set-Location -Path "$PSScriptRoot\backend"

# Check if virtual environment exists
if (-Not (Test-Path ".venv")) {
    Write-Host "📦 Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Virtual environment created!" -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "📚 Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✅ Dependencies installed!" -ForegroundColor Green
Write-Host ""

# Check if ML model exists
if (-Not (Test-Path "models\vibe_classifier.pkl")) {
    Write-Host "🤖 Training ML model (first time setup)..." -ForegroundColor Yellow
    python train_ml_model.py
    Write-Host "✅ ML model trained!" -ForegroundColor Green
    Write-Host ""
}

# Start the server
Write-Host "🌟 Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
Write-Host "📊 API Docs available at http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

uvicorn app.main:app --reload --port 8000
