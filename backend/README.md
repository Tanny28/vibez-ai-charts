# Vibe-Code Backend

FastAPI backend for the Vibe-Code data visualization recommendation engine.

## Features

- 🎯 Smart chart type recommendation based on natural language prompts
- 📊 Dataset analysis and feature extraction
- 📁 CSV file upload and management
- 📈 Dynamic Plotly chart generation
- 🔄 Adaptive constraints based on data characteristics

## API Endpoints

### `POST /api/recommend`
Generate chart recommendation from a data goal prompt.

**Request:**
```json
{
  "goal": "Show revenue trend over 5 years",
  "insight": "Auto",
  "file_id": "optional-uuid"
}
```

**Response:**
```json
{
  "vibe": "line",
  "constraints": {
    "palette": "single_sequential",
    "axis": "time_x;linear_y;yearly_ticks",
    "labeling": "annotate_start_end;show_percent_change",
    "rationale": "Line charts show slope and trends over time."
  },
  "rationale": "Line charts show slope and trends over time.",
  "chart_spec": { ... }
}
```

### `POST /api/upload`
Upload a CSV file for analysis.

**Request:** Multipart form with file

**Response:**
```json
{
  "file_id": "uuid",
  "filename": "data.csv",
  "summary": {
    "num_rows": 100,
    "num_numeric": 3,
    "num_categorical": 2,
    "columns": [...]
  }
}
```

### `POST /api/preview`
Generate chart with specific column selections.

**Request:**
```json
{
  "file_id": "uuid",
  "vibe": "line",
  "x_col": "date",
  "y_col": "revenue"
}
```

### `GET /api/files/{file_id}`
Download an uploaded file.

### `DELETE /api/files/{file_id}`
Delete an uploaded file.

## Setup & Run

### Development

1. **Create virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run server:**
```bash
uvicorn app.main:app --reload --port 8000
```

Server will start at http://localhost:8000

4. **API documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker

```bash
docker build -t vibe-code-backend .
docker run -p 8000:8000 vibe-code-backend
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── vibe_engine.py       # Chart recommendation engine
│   ├── data_utils.py        # Data analysis utilities
│   ├── schemas.py           # Pydantic models
│   └── chart_generator.py  # Plotly chart generation
├── data/                    # Uploaded files (created at runtime)
├── requirements.txt
├── Dockerfile
└── README.md
```

## Environment Variables

- `PORT` - Server port (default: 8000)
- `DATA_DIR` - Directory for uploaded files (default: ./data)
- `CORS_ORIGINS` - Allowed CORS origins (default: *)

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Production Deployment

### Railway
```bash
railway up
```

### Render
Connect your Git repository and configure:
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Google Cloud Run
```bash
gcloud run deploy vibe-code-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## License

MIT
