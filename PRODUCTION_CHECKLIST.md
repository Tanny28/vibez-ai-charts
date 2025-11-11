# 🚀 Production Readiness Checklist

## ✅ Issues Fixed

### 1. **ML Model Path Issues** ✅ FIXED
**Problem**: Model saved to wrong location (`backend/backend/models/`)
**Solution**: Updated `ml_vibe_engine.py` to use absolute paths with `Path(__file__).parent.parent`
**Status**: Model now correctly loads from `backend/models/vibe_classifier.pkl`

### 2. **Scikit-Learn Version Mismatch** ✅ FIXED
**Problem**: Backend had scikit-learn 1.3.2, model trained with 1.7.2
**Solution**: Upgraded backend scikit-learn to 1.7.2
**Status**: Compatible versions across environments

### 3. **Working Directory Issues** ✅ FIXED
**Problem**: Backend failed to start when uvicorn run from wrong directory
**Solution**: Created `start.ps1` script that sets correct working directory
**Status**: Use `d:\vibez_codepcu\backend\start.ps1` to start server

---

## 🔍 Pre-Production Verification

### Backend Health Checks

#### ✅ 1. Server Startup
```powershell
cd d:\vibez_codepcu\backend
uvicorn app.main:app --reload --port 8000
```
**Expected**: `INFO: Application startup complete.`
**Status**: ✅ PASSING

#### ✅ 2. ML Model Loading
**Check logs for**:
```
Model loaded from backend/models/vibe_classifier.pkl
```
**NOT**:
```
No pre-trained model found. Use train() to create one.
```

Test with:
```powershell
curl http://localhost:8000/api/health
# Expected: {"status":"healthy"}
```

#### ✅ 3. ML Predictions Working
**Check logs for**:
```
🤖 ML predicted 'line' with 85.0% confidence for: 'show trends'
```
**NOT**:
```
📋 Rule-based matched 'line' for: 'show trends'
```

### Frontend Health Checks

#### ✅ 4. Frontend Builds
```powershell
cd d:\vibez_codepcu\frontend
npm run dev
```
**Expected**: `Local: http://localhost:5173/`
**Status**: ✅ PASSING

#### ✅ 5. API Connectivity
**Check browser console**: No CORS errors
**Check Network tab**: API calls return 200 OK
**Status**: ✅ PASSING

---

## 🛡️ Security Review

### ⚠️ CRITICAL - Update Before Production

#### 1. CORS Settings
**File**: `backend/app/main.py`
**Current**:
```python
allow_origins=["*"]  # ❌ ALLOWS ALL ORIGINS
```
**Fix for Production**:
```python
allow_origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]
```

#### 2. Environment Variables
**Current**: Hardcoded values ❌
**Needed**: Create `.env` file
```bash
# .env
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://yourdomain.com
```

Update `main.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","),
    ...
)
```

#### 3. File Upload Security
**Current**: No file size limits ⚠️
**Add to `main.py`**:
```python
from fastapi import File, UploadFile, HTTPException

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")
    
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only CSV files allowed")
```

#### 4. Rate Limiting
**Install**:
```powershell
pip install slowapi
```

**Add to `main.py`**:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/recommend")
@limiter.limit("20/minute")  # 20 requests per minute
async def recommend(request: Request, req: RecommendRequest):
    ...
```

---

## 📊 Performance Optimization

### 1. Add Response Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_ml_engine():
    return MLVibeEngine()
```
✅ Already implemented!

### 2. Enable Gzip Compression
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### 3. Database for File Storage
**Current**: Files stored in `backend/data/` ⚠️
**Production**: Use S3, Azure Blob Storage, or database

### 4. Async Database Queries
If adding database:
```python
from databases import Database

database = Database("postgresql://...")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
```

---

## 🐳 Docker Deployment

### 1. Build Images
```powershell
docker-compose build
```

### 2. Start Services
```powershell
docker-compose up -d
```

### 3. Health Check
```powershell
curl http://localhost:8000/api/health
curl http://localhost:3000
```

### 4. View Logs
```powershell
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

## 📝 Logging & Monitoring

### 1. Add Structured Logging
```python
import logging
from pythonjsonlogger import jsonlogger

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

@app.post("/api/recommend")
async def recommend(req: RecommendRequest):
    logger.info("recommendation_request", extra={
        "prompt": req.goal,
        "file_id": req.file_id,
        "timestamp": datetime.now().isoformat()
    })
    ...
```

### 2. Add Error Tracking
**Install Sentry**:
```powershell
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

### 3. Add Analytics
Track ML prediction accuracy:
```python
@app.post("/api/recommend")
async def recommend(req: RecommendRequest):
    prediction, confidence = ml_engine.predict(req.goal)
    
    # Log metrics
    logger.info("ml_prediction", extra={
        "chart_type": prediction,
        "confidence": confidence,
        "used_ml": confidence > 0.5
    })
```

---

## 🧪 Testing

### 1. Backend Tests
```powershell
cd backend
pytest tests/ -v --cov=app
```

### 2. API Integration Tests
Create `tests/test_api.py`:
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_recommend():
    response = client.post("/api/recommend", json={
        "goal": "show sales trends"
    })
    assert response.status_code == 200
    assert "vibe" in response.json()
```

### 3. Load Testing
```powershell
pip install locust
```

Create `locustfile.py`:
```python
from locust import HttpUser, task, between

class VibeUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def recommend_chart(self):
        self.client.post("/api/recommend", json={
            "goal": "show sales trends"
        })
```

Run:
```powershell
locust -f locustfile.py --host=http://localhost:8000
```

---

## 📦 Dependency Management

### 1. Pin Versions
**Update `requirements.txt`**:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pandas==2.1.3
numpy==1.26.2
plotly==5.18.0
scikit-learn==1.7.2  # ✅ Updated
pydantic==2.5.0
python-multipart==0.0.6
```

### 2. Vulnerability Scanning
```powershell
pip install safety
safety check --file requirements.txt
```

---

## 🚀 Deployment Checklist

### Before Deploying:

- [ ] Update CORS origins to production domains
- [ ] Add environment variables (.env file)
- [ ] Enable rate limiting
- [ ] Add file size validation
- [ ] Set up error tracking (Sentry)
- [ ] Configure logging
- [ ] Run security scan (`safety check`)
- [ ] Run tests (`pytest`)
- [ ] Build Docker images
- [ ] Test Docker deployment locally
- [ ] Set up SSL certificates (Let's Encrypt)
- [ ] Configure reverse proxy (nginx)
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Create backup strategy
- [ ] Document API endpoints (OpenAPI/Swagger)
- [ ] Set up CI/CD pipeline

### Environment-Specific Settings:

#### Development
- Debug mode: ON
- Logging: DEBUG level
- CORS: localhost allowed
- File cleanup: Manual

#### Production
- Debug mode: OFF
- Logging: INFO/WARNING level
- CORS: Specific domains only
- File cleanup: Automatic (cron job)
- HTTPS: Required
- Rate limiting: Strict

---

## 📋 Current Status Summary

### ✅ WORKING
- Backend API (9 endpoints)
- Frontend React app
- File upload/download
- Chart generation (Plotly)
- ML model training
- ML predictions
- Feedback collection
- Docker configs
- Basic error handling

### ⚠️ NEEDS ATTENTION BEFORE PRODUCTION
- CORS configuration (currently allows all origins)
- Environment variables (hardcoded values)
- File upload limits (no size restrictions)
- Rate limiting (not implemented)
- Error tracking (no Sentry)
- SSL certificates (HTTP only)
- Database (using file system)
- Automated tests (minimal coverage)
- Load testing (not performed)
- Security audit (needed)

### 🎯 RECOMMENDED NEXT STEPS
1. **Immediate**: Fix CORS settings
2. **High Priority**: Add rate limiting
3. **High Priority**: Set up environment variables
4. **Medium**: Add comprehensive tests
5. **Medium**: Implement error tracking
6. **Low**: Migrate to database storage

---

## 🎉 Production Deploy Commands

Once checklist complete:

```powershell
# 1. Build for production
cd frontend
npm run build

# 2. Start Docker containers
cd ..
docker-compose up -d

# 3. Verify
curl https://your domain.com/api/health

# 4. Monitor logs
docker-compose logs -f
```

---

**Last Updated**: November 11, 2025
**Current Version**: 1.0.0 (Development)
**Ready for Production**: ⚠️ NO - Address security items first
