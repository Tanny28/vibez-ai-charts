# Start the FastAPI backend server
Set-Location -Path $PSScriptRoot
uvicorn app.main:app --reload --port 8000
