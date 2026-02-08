# Start Educational Content Assistant Backend

Write-Host "🚀 Starting Educational Content Assistant..." -ForegroundColor Cyan

# Check if .env file exists
if (!(Test-Path "../.env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "Please create a .env file with your SCALEDOWN_API_KEY" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment and start server
.\venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

Write-Host "📡 Starting FastAPI server on http://localhost:8000" -ForegroundColor Cyan
python app.py
