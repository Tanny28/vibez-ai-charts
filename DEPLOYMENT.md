# Vibez AI - Deployment & Setup Guide

## 🚀 Quick Start (Docker)

**Recommended for production deployment**

```bash
# Clone or navigate to project root
cd vibez_codepcu

# Build and start all services
docker-compose up --build

# Access the application at http://localhost:3000
# Backend API at http://localhost:8000/docs
```

## 📦 Local Development Setup

### Prerequisites
- Node.js 18+
- Python 3.9+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend will be available at `http://localhost:5173`

## 🔌 API Endpoints

**POST** `/api/recommend` - Get chart recommendation
```json
{
  "goal": "Show sales trends",
  "insight": "trend",
  "file_id": "optional-uuid"
}
```

**POST** `/api/upload` - Upload CSV file

**GET** `/api/health` - Health check

**GET** `/docs` - Interactive API documentation (Swagger UI)

## 🐛 Troubleshooting

### CORS Errors
Ensure backend CORS settings allow frontend origin:
```python
# backend/app/main.py
origins = ["http://localhost:5173", "http://localhost:3000"]
```

### Port Conflicts
```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Module Not Found
```bash
# Frontend
cd frontend && npm install

# Backend
cd backend && pip install -r requirements.txt
```

## 📊 Sample Data

Example CSV files are in `example_data/`:
- `sales_by_region.csv` - Regional comparison
- `trend.csv` - Time series data
- `ages_distribution.csv` - Distribution data
- `countries_gdp.csv` - Geospatial data

## 🎨 Example Prompts

1. "Show me sales trends over time" → Line chart
2. "Compare revenue by region" → Grouped bar chart
3. "Distribution of customer ages" → Histogram
4. "GDP by country on map" → Choropleth

## 🏗️ Architecture

```
┌─────────────┐      HTTP      ┌──────────────┐
│   React     │ ────────────▶  │   FastAPI    │
│  Frontend   │    /api/*      │   Backend    │
│  (Port 5173)│ ◀────────────  │  (Port 8000) │
└─────────────┘                └──────────────┘
      │                              │
      │                              │
   Plotly.js                    vibe_engine.py
   Tailwind CSS                 Plotly specs
   Framer Motion                Pandas/NumPy
```

## 🔐 Production Checklist

- [ ] Set secure `ALLOWED_ORIGINS` in backend
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS with SSL certificates
- [ ] Configure proper CORS headers
- [ ] Set up logging and monitoring
- [ ] Use gunicorn with multiple workers
- [ ] Enable nginx gzip compression
- [ ] Set up database for file metadata (if needed)

## 📚 Documentation

- **Backend API**: `http://localhost:8000/docs` (Swagger UI)
- **Backend README**: `backend/README.md`
- **Frontend Components**: `frontend/src/components/`

## 🤝 Support

For issues or questions:
1. Check this deployment guide
2. Review API documentation at `/docs`
3. Check browser console for frontend errors
4. Check backend logs for API errors

---

**Happy Visualizing! 📊✨**
