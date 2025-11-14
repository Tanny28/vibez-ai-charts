# Render Deployment Configuration for Vibez AI Charts

## 🚀 Backend Deployment (Web Service)

### Service Configuration
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment**: `Python 3.11`
- **Dockerfile**: Use root `Dockerfile` (recommended) or `backend/Dockerfile`

### Environment Variables (REQUIRED)
Add these in Render dashboard under "Environment":
```
GEMINI_API_KEY=your_google_gemini_api_key_here
PYTHONUNBUFFERED=1
```

### Health Check Endpoint
- **Path**: `/api/health`
- **Expected Response**: `200 OK`

---

## 🎨 Frontend Deployment (Static Site)

### Build Configuration
- **Build Command**: `cd frontend && npm install && npm run build`
- **Publish Directory**: `frontend/dist`
- **Environment**: `Node 18`

### Environment Variables
```
VITE_API_URL=https://your-backend-url.onrender.com
```

---

## 📋 Deployment Steps

### Option 1: Using Root Dockerfile (Recommended for Backend)

1. **Create New Web Service** on Render
2. **Connect GitHub Repository**: `https://github.com/Tanny28/vibez-ai-charts`
3. **Configure Service**:
   - Name: `vibez-backend`
   - Environment: `Docker`
   - Dockerfile Path: `./Dockerfile`
   - Instance Type: Free or Starter
4. **Add Environment Variables**:
   - `GEMINI_API_KEY` = Your Google Gemini API key
5. **Deploy**

### Option 2: Manual Commands (Alternative)

**Backend:**
```bash
# Build Command
pip install -r backend/requirements.txt

# Start Command
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Frontend:**
```bash
# Build Command
cd frontend && npm install && npm run build

# Publish Directory
frontend/dist
```

---

## 🔧 Troubleshooting

### Backend Not Starting
- ✅ Verify `GEMINI_API_KEY` is set in environment variables
- ✅ Check that `backend/models/vibe_classifier.pkl` exists
- ✅ Review Render logs for Python errors

### Frontend Can't Connect to Backend
- ✅ Set `VITE_API_URL` to your backend URL (e.g., `https://vibez-backend.onrender.com`)
- ✅ Ensure CORS is enabled in backend (already configured in `main.py`)
- ✅ Check backend health endpoint: `https://your-backend.onrender.com/api/health`

### Build Failures
- ✅ Ensure all dependencies are in `requirements.txt` or `package.json`
- ✅ Check Python version is 3.11 in Render settings
- ✅ Verify Node version is 18 for frontend

---

## 📊 Expected Render URLs

After deployment:
- **Backend API**: `https://vibez-backend.onrender.com`
- **Frontend**: `https://vibez-ai-charts.onrender.com`
- **Health Check**: `https://vibez-backend.onrender.com/api/health`
- **API Docs**: `https://vibez-backend.onrender.com/docs`

---

## 🎯 Quick Start Checklist

- [ ] Get Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- [ ] Create Render account at [render.com](https://render.com)
- [ ] Connect GitHub repository to Render
- [ ] Deploy backend as Web Service (Docker)
- [ ] Add `GEMINI_API_KEY` environment variable
- [ ] Deploy frontend as Static Site
- [ ] Update `VITE_API_URL` in frontend environment
- [ ] Test `/api/health` endpoint
- [ ] Upload CSV and test chart generation

---

## 💡 Performance Tips

- Use **Starter** plan for faster cold starts (free tier has 50s spin-down)
- Enable **Auto-Deploy** for automatic deployments on git push
- Monitor **Logs** in Render dashboard for debugging
- Use **Custom Domain** for production (optional)

---

## 🔐 Security Notes

- Never commit `.env` files to GitHub
- Use Render's environment variables for secrets
- GEMINI_API_KEY should only be set in Render dashboard
- Frontend environment variables are baked into build (public)
