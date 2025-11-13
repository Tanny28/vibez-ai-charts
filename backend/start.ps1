# Start the FastAPI backend server
Set-Location -Path $PSScriptRoot

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Start the server
uvicorn app.main:app --reload --port 8000
