# 🚀 GitHub & Deployment Quick Start Guide

## Step 1: Create GitHub Repository

1. **Go to GitHub** → https://github.com/new

2. **Create New Repository:**
   - **Repository name:** `vibez-ai-charts` (or your choice)
   - **Description:** AI-Powered Data Visualization Platform with ML-driven chart recommendations
   - **Visibility:** Public (or Private)
   - ⚠️ **DO NOT** initialize with README, .gitignore, or license (we already have these)

3. **Click "Create repository"**

## Step 2: Push to GitHub

Copy and run these commands in your terminal:

```powershell
# Set your GitHub username (replace YOUR_USERNAME)
$GITHUB_USER = "YOUR_USERNAME"
$REPO_NAME = "vibez-ai-charts"

# Add remote origin
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"

# Rename branch to main (GitHub's default)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Alternative: If you prefer SSH:**
```powershell
git remote add origin git@github.com:YOUR_USERNAME/vibez-ai-charts.git
git branch -M main
git push -u origin main
```

## Step 3: Verify Upload

Visit: `https://github.com/YOUR_USERNAME/vibez-ai-charts`

You should see all your files! ✅

## Step 4: Deploy to Vercel (FREE!)

### Option A: One-Click Deploy

1. **Go to Vercel:** https://vercel.com/new

2. **Import Git Repository**
   - Click "Import Git Repository"
   - Select your GitHub account
   - Choose `vibez-ai-charts` repository
   - Click "Import"

3. **Configure Project:**
   - **Framework Preset:** Other
   - **Root Directory:** `./` (leave as default)
   - **Build Command:** Leave empty or use: `cd frontend && npm install && npm run build`
   - **Output Directory:** `frontend/dist`
   - **Install Command:** Leave empty

4. **Environment Variables (Optional):**
   Click "Environment Variables" and add:
   ```
   PYTHONPATH=backend
   ```

5. **Click "Deploy"** 🚀

   Wait 2-3 minutes... Your app will be live!

### Option B: Vercel CLI (Faster for updates)

```powershell
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy (follow prompts)
cd d:\vibez_codepcu
vercel

# For production deployment
vercel --prod
```

**Prompts you'll see:**
- Set up and deploy? → **Y**
- Which scope? → Select your account
- Link to existing project? → **N**
- What's your project's name? → `vibez-ai-charts`
- In which directory is your code located? → `./`
- Want to override settings? → **N**

## Step 5: Update Frontend API URL (Important!)

After deployment, Vercel will give you a URL like:
`https://vibez-ai-charts-xyz123.vercel.app`

### For Vercel deployments:
The frontend is already configured to use relative paths (`/api`) in production, so **no changes needed**! ✨

The magic happens in `frontend/src/lib/api.ts`:
```typescript
const API_BASE = import.meta.env.VITE_API_BASE_URL || 
  (import.meta.env.PROD ? '/api' : 'http://localhost:8000');
```

## Step 6: Test Your Deployment

1. **Visit your Vercel URL:** `https://your-project.vercel.app`

2. **Test the app:**
   - ✅ Upload a CSV file (use `example_data/sales_by_region.csv`)
   - ✅ Type a prompt: "Show sales trend over time"
   - ✅ Verify automatic insights appear
   - ✅ Click suggested visualizations
   - ✅ Check chart renders properly

3. **Check API health:**
   Visit: `https://your-project.vercel.app/api/health`
   
   Should return: `{"status": "healthy"}`

## 🔧 Troubleshooting

### Build Fails on Vercel

**Issue:** Frontend build fails
**Solution:** 
1. Check Node.js version (should be 18+)
2. In Vercel dashboard → Settings → General
3. Set Node.js Version: `18.x`

**Issue:** Python dependencies fail
**Solution:**
1. Ensure `backend/requirements.txt` is properly formatted
2. Check scikit-learn version compatibility
3. Vercel has 50MB Lambda limit - our model is ~2MB ✅

### API Returns 404

**Issue:** `/api/*` routes not working
**Solution:**
1. Check `vercel.json` exists in root
2. Verify routes configuration:
```json
"routes": [
  { "src": "/api/(.*)", "dest": "backend/app/main.py" },
  { "src": "/(.*)", "dest": "frontend/$1" }
]
```

### CORS Errors

**Issue:** "CORS policy blocked" errors
**Solution:**
1. Update `backend/app/main.py` CORS origins:
```python
origins = [
    "https://your-project.vercel.app",
    "https://*.vercel.app",  # All preview deployments
]
```
2. Redeploy: `vercel --prod`

### ML Model Not Loading

**Issue:** 500 error when making predictions
**Solution:**
1. Check `backend/models/vibe_classifier.pkl` is in git
2. Verify file size: `ls -lh backend/models/` (should be ~2MB)
3. Check scikit-learn version matches training:
   ```
   pip list | grep scikit-learn  # Should be 1.7.2
   ```

### File Uploads Failing

**Issue:** CSV upload returns error
**Solution:**
1. Serverless functions have `/tmp` directory limits
2. For production, consider:
   - AWS S3 integration
   - Cloudinary for file storage
   - Redis for temporary storage

## 🔄 Making Updates

### Update Code & Redeploy

```powershell
# Make your changes...

# Stage changes
git add .

# Commit
git commit -m "Your update message"

# Push to GitHub
git push origin main

# Vercel will automatically deploy! 🎉
```

**Vercel auto-deploys** when you push to GitHub!

### Manual Redeploy

```powershell
vercel --prod
```

## 🌐 Custom Domain (Optional)

1. **In Vercel Dashboard:**
   - Go to your project
   - Click "Settings" → "Domains"
   - Add your domain (e.g., `vibez.yourdomain.com`)

2. **Update DNS:**
   - Add CNAME record pointing to Vercel
   - Wait for propagation (5-60 minutes)

3. **SSL Certificate:**
   - Vercel automatically provisions SSL ✅

## 📊 Monitor Your App

### Vercel Analytics (Built-in)
- Go to your project → Analytics
- See page views, performance, errors

### Error Tracking
Add Sentry integration:
```powershell
npm install @sentry/react
```

Update `frontend/src/main.tsx`:
```typescript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  environment: import.meta.env.MODE,
});
```

## 🎉 You're Live!

**Your URLs:**
- **Frontend:** `https://your-project.vercel.app`
- **API Health:** `https://your-project.vercel.app/api/health`
- **GitHub Repo:** `https://github.com/YOUR_USERNAME/vibez-ai-charts`

### Share Your Project! 🌟

Add a nice badge to your README:

```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/vibez-ai-charts)

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://your-project.vercel.app)
```

## 📱 Next Steps

1. ⭐ **Star** your own repo to show it in your profile
2. 📝 Update README with your deployed URL
3. 🎨 Customize the app with your branding
4. 📊 Add analytics tracking
5. 🔐 Add authentication (optional)
6. 💾 Set up database for persistence (optional)
7. 🤖 Integrate GPT-4 for advanced insights (optional)

## 🆘 Need Help?

- **Vercel Docs:** https://vercel.com/docs
- **GitHub Issues:** https://github.com/YOUR_USERNAME/vibez-ai-charts/issues
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **React Docs:** https://react.dev

---

**Congratulations! Your AI-powered data viz platform is now live! 🚀📊**

Remember to update this guide with your actual GitHub username and Vercel URL!
