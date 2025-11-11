# VIBEZ Deployment Guide

## 🚀 Quick Deploy to Vercel

### Prerequisites
- GitHub account
- Vercel account (free tier works!)
- Node.js 18+ and Python 3.11+

### Option 1: Deploy via Vercel CLI (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from project root**
   ```bash
   vercel
   ```

4. **Follow the prompts:**
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N**
   - Project name: `vibez-ai-charts` (or your choice)
   - Directory: `./` (current directory)
   - Override settings? **N**

5. **Deploy to production**
   ```bash
   vercel --prod
   ```

### Option 2: Deploy via GitHub + Vercel Dashboard

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: VIBEZ AI Chart Generator"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/vibez-ai-charts.git
   git push -u origin main
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Configure project:
     - **Framework Preset:** Other
     - **Root Directory:** `./`
     - **Build Command:** `cd frontend && npm install && npm run build`
     - **Output Directory:** `frontend/dist`
     - **Install Command:** `cd backend && pip install -r requirements.txt && cd ../frontend && npm install`

3. **Environment Variables (Optional)**
   Add these in Vercel dashboard under Settings > Environment Variables:
   ```
   PYTHONPATH=backend
   ```

4. **Deploy!**
   Click "Deploy" - your app will be live in ~2 minutes!

## 🔧 Configuration

### Frontend API URL
Update the API base URL in `frontend/src/lib/api.ts` for production:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
  (import.meta.env.PROD ? '/api' : 'http://localhost:8000');
```

### Backend CORS
The backend is already configured for CORS. For production, update `backend/app/main.py`:

```python
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://your-domain.vercel.app",  # Add your Vercel domain
    "https://*.vercel.app",  # Allow all Vercel preview deployments
]
```

## 📦 Build Commands

### Frontend Build
```bash
cd frontend
npm install
npm run build
```

### Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

## 🌐 Alternative Deployment Platforms

### Railway.app
1. Connect GitHub repository
2. Add two services:
   - **Backend:** Python service pointing to `backend/`
   - **Frontend:** Static site pointing to `frontend/dist/`
3. Set environment variables
4. Deploy!

### Render.com
1. Create Web Service for backend (Python)
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. Create Static Site for frontend
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

### Heroku
1. Create `Procfile` in root:
   ```
   web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

2. Add buildpacks:
   ```bash
   heroku buildpacks:add heroku/python
   heroku buildpacks:add heroku/nodejs
   ```

3. Deploy:
   ```bash
   git push heroku main
   ```

## 🐳 Docker Deployment

### Build and Run
```bash
docker-compose up -d
```

### Deploy to Cloud (AWS, GCP, Azure)
```bash
# Build images
docker-compose build

# Tag for registry
docker tag vibez-backend:latest your-registry/vibez-backend:latest
docker tag vibez-frontend:latest your-registry/vibez-frontend:latest

# Push to registry
docker push your-registry/vibez-backend:latest
docker push your-registry/vibez-frontend:latest
```

## ✅ Post-Deployment Checklist

- [ ] Test file upload functionality
- [ ] Test ML chart recommendations
- [ ] Verify automatic insights generation
- [ ] Test all chart types (line, bar, scatter, etc.)
- [ ] Check responsive design on mobile
- [ ] Verify API endpoints are accessible
- [ ] Test with different CSV files
- [ ] Enable analytics (optional)
- [ ] Set up custom domain (optional)
- [ ] Configure CDN for faster load times (optional)

## 🔍 Troubleshooting

### Build Fails
- Check Node.js version (18+)
- Check Python version (3.11+)
- Clear caches: `rm -rf node_modules frontend/dist backend/__pycache__`

### API Not Connecting
- Verify CORS settings in `backend/app/main.py`
- Check API_BASE_URL in frontend
- Ensure both services are running

### ML Model Not Loading
- Ensure `backend/models/vibe_classifier.pkl` is committed to git
- Check file size limits (max 50MB on Vercel)
- Verify scikit-learn version matches training environment

### File Upload Issues
- Check `/tmp` directory permissions (serverless limitation)
- Consider using cloud storage (S3, GCS) for production
- Implement cleanup for old files

## 📊 Performance Optimization

### Frontend
- Enable gzip compression
- Use CDN for static assets
- Implement lazy loading for charts
- Cache API responses

### Backend
- Add Redis for caching insights
- Use database for file metadata
- Implement rate limiting
- Enable response compression

## 🔐 Security Best Practices

1. **Environment Variables:** Never commit `.env` files
2. **API Keys:** Use environment variables for sensitive data
3. **File Uploads:** Validate file types and sizes
4. **CORS:** Restrict to specific domains in production
5. **Rate Limiting:** Implement request throttling
6. **Input Validation:** Sanitize all user inputs

## 📈 Monitoring

- **Vercel Analytics:** Built-in for Vercel deployments
- **Error Tracking:** Consider Sentry integration
- **Logs:** Use Vercel logs or integrate LogRocket
- **Uptime:** Set up monitoring with UptimeRobot

## 🎉 You're Live!

Your VIBEZ AI Chart Generator is now deployed and ready to use!

**Example URLs:**
- Frontend: `https://your-project.vercel.app`
- API: `https://your-project.vercel.app/api/health`

Share your deployment URL and start generating beautiful charts! 🚀📊
