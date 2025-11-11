# 🚀 Vibez AI - Local Quickstart Guide

## Running the Application Locally

### Option 1: Using Startup Scripts (RECOMMENDED)

1. **Start Backend Server** (Terminal 1):
   ```powershell
   .\START_BACKEND.ps1
   ```
   - Backend will run on: http://localhost:8000
   - API docs available at: http://localhost:8000/docs

2. **Start Frontend Server** (Terminal 2):
   ```powershell
   .\START_FRONTEND.ps1
   ```
   - Frontend will run on: http://localhost:5173

3. **Open Browser**:
   - Navigate to: http://localhost:5173
   - Upload a CSV file or use example data
   - Type a prompt like "Show sales by region as a bar chart"
   - Watch the AI generate visualizations!

---

### Option 2: Manual Setup

#### Backend Setup:
```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Train ML model (first time only)
python train_ml_model.py

# Start server
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup (in a new terminal):
```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

---

## 🧪 Testing the Application

1. **Upload Sample Data**:
   - Use files from `example_data/` folder
   - Try: `sales_by_region.csv`, `countries_gdp.csv`, `trend.csv`

2. **Try These Prompts**:
   - "Show me a bar chart of sales by region"
   - "Create a line chart showing trends over time"
   - "Display GDP as a pie chart"
   - "Show sales comparison as a grouped bar chart"

3. **Automatic Features**:
   - **Insights**: Automatic business insights appear after upload
   - **KPIs**: Key metrics displayed in cards
   - **ML Recommendations**: AI suggests best chart types

---

## 📊 ML Model Performance

- **Training Accuracy**: 97.14%
- **Validation Accuracy**: 91.43%
- **Confidence Threshold**: 35%
- **ML Usage Rate**: 71% of prompts

---

## 🛠️ Troubleshooting

### Backend Issues:

**Error: "No module named 'fastapi'"**
```powershell
# Make sure virtual environment is activated
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Error: "Model file not found"**
```powershell
# Train the ML model
python train_ml_model.py
```

**Port 8000 already in use:**
```powershell
# Kill existing process
Get-Process -Name python | Stop-Process -Force
# Or change port
uvicorn app.main:app --reload --port 8001
```

### Frontend Issues:

**Error: "Cannot find module"**
```powershell
# Reinstall dependencies
Remove-Item -Recurse -Force node_modules
npm install
```

**Port 5173 already in use:**
- Vite will automatically use the next available port (5174, 5175, etc.)
- Check the terminal output for the actual URL

---

## 🎯 Features Included

✅ **ML-Powered Chart Recommendations** (91.43% accuracy)  
✅ **Automatic Business Insights** (5 categories)  
✅ **Dark Developer Theme** (no emojis, professional)  
✅ **7 Chart Types** (bar, line, pie, scatter, area, funnel, heatmap)  
✅ **CSV File Upload** with preview  
✅ **JSON Export** for chart configs  
✅ **Real-time Data Validation**  
✅ **Interactive Plotly Charts**  

---

## 📁 Project Structure

```
vibez_codepcu/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── vibe_engine.py       # Rule-based engine
│   │   ├── ml_vibe_engine.py    # ML classifier
│   │   ├── data_insights.py     # Auto insights
│   │   └── ...
│   ├── models/
│   │   └── vibe_classifier.pkl  # Trained model
│   ├── requirements.txt
│   └── train_ml_model.py
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Main app
│   │   ├── components/          # UI components
│   │   ├── lib/
│   │   │   ├── api.ts           # API client
│   │   │   └── utils.ts         # Utilities
│   │   └── ...
│   └── package.json
│
├── START_BACKEND.ps1            # Backend startup script
├── START_FRONTEND.ps1           # Frontend startup script
└── example_data/                # Sample CSV files
```

---

## 🔗 Useful URLs

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

---

## 🎉 Next Steps

1. ✅ Run locally (you are here!)
2. 🚀 Deploy to Vercel (see `DEPLOYMENT_GUIDE.md`)
3. 📝 Customize UI theme (`frontend/src/index.css`)
4. 🤖 Improve ML model (`backend/train_ml_model.py`)
5. 📊 Add more chart types (`backend/app/chart_generator.py`)

---

**Need Help?** Check the logs in your terminal or visit http://localhost:8000/docs for API documentation.
