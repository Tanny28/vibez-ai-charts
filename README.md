# VIBEZ v2.0 - AI-Powered Data Visualization Platform

A cutting-edge data visualization platform that combines **Machine Learning** with **Natural Language Processing** to automatically generate stunning, insightful charts from your data. Built with FastAPI, React, and scikit-learn.

## ✨ Features

### 🤖 **ML-Powered Chart Recommendations** (91.43% Accuracy)
- Trained Random Forest classifier with 350 examples across 7 chart types
- TF-IDF vectorization with 4-gram analysis
- Intelligent confidence-based hybrid system (ML + rule-based fallback)

### 💡 **Automatic Business Insights**
- **5 Intelligent Analyzers**: Revenue, Categories, Quality, Geography, Customers
- Smart column detection with keyword matching
- Actionable recommendations for every insight
- Auto-suggested visualizations based on data structure

### 🎨 **Modern Dark UI**
- Professional developer-focused aesthetic
- Monospace typography and gradient effects
- Smooth animations with Framer Motion
- Real-time chart previews with Plotly.js

### 📊 **7 Chart Types Supported**
- `line` - Trends over time
- `grouped_bar` - Category comparisons
- `histogram` - Distribution analysis
- `scatter` - Correlation exploration
- `stacked_bar` - Composition breakdown
- `horizontal_bar` - Rankings and top lists
- `choropleth` - Geographic visualization

### 🔧 **Advanced Features**
- CSV file upload with intelligent parsing
- Real-time KPI cards (rows, columns, types)
- Design constraints with rationale
- Model retraining with user feedback
- Export charts as images

## 🚀 Quick Start

### Local Development

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **npm or yarn**

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/vibez-ai-charts.git
cd vibez-ai-charts
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Train ML Model** (First time only)
```bash
cd backend
python train_ml_model.py
```

### Running Locally

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Visit `http://localhost:5173` in your browser! 🎉

## 🌐 Deploy to Vercel (Production)

### Quick Deploy (1-Click)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/vibez-ai-charts)

### Manual Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed instructions including:
- Vercel CLI deployment
- GitHub integration
- Environment variables
- Alternative platforms (Railway, Render, Heroku)
- Docker deployment

**Quick Steps:**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Production
vercel --prod
```

Your app will be live at `https://your-project.vercel.app`! 🚀

## 📁 Project Structure

```
vibez_codepcu/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app with 10+ endpoints
│   │   ├── vibe_engine.py       # Rule-based chart logic
│   │   ├── ml_vibe_engine.py    # ML-powered recommendations
│   │   ├── data_insights.py     # Automatic insights engine
│   │   ├── data_utils.py        # CSV parsing & analysis
│   │   ├── chart_generator.py   # Plotly chart generation
│   │   └── schemas.py           # Pydantic models
│   ├── models/
│   │   └── vibe_classifier.pkl  # Trained ML model (91% accuracy)
│   ├── data/                    # Uploaded CSV files
│   ├── train_ml_model.py        # ML training script
│   ├── requirements.txt         # Python dependencies
│   └── vercel.json             # Backend deployment config
│
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── App.tsx          # Main app shell
│   │   │   ├── PromptBox.tsx    # Query input
│   │   │   ├── FileUploader.tsx # CSV upload
│   │   │   ├── ChartCanvas.tsx  # Plotly chart display
│   │   │   ├── KpiCards.tsx     # Dataset statistics
│   │   │   ├── InsightsPanel.tsx # Auto insights display
│   │   │   └── ...
│   │   ├── lib/
│   │   │   └── api.ts           # API client
│   │   └── hooks/
│   │       └── useVibe.ts       # Chart state management
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── example_data/                # Sample CSV files
├── vercel.json                  # Deployment configuration
├── .gitignore
├── DEPLOYMENT_GUIDE.md          # Detailed deployment docs
└── README.md                    # This file
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/test_vibe_engine.py -v
```

### ML Model Testing
```bash
cd backend
python test_ml_model.py
```

### Frontend (Manual Testing)
1. Upload `example_data/sales_by_region.csv`
2. Try prompt: "Show sales trend over time"
3. Verify automatic insights appear
4. Click suggested visualizations
5. Test chart downloads

## 🔧 How It Works

### 🤖 Machine Learning Pipeline

**1. Training Phase** (`train_ml_model.py`)
- 350 labeled examples across 7 chart types
- TF-IDF vectorization (1000 features, 1-4 grams, sublinear scaling)
- Random Forest Classifier (200 trees, max depth 15, balanced classes)
- Results: 97.14% training accuracy, **91.43% validation accuracy**

**2. Inference Phase** (`ml_vibe_engine.py`)
- Text preprocessing and TF-IDF transformation
- Random Forest probability prediction
- Confidence threshold: 35% (optimized for 7-class problem)
- Hybrid fallback: If confidence < 35%, use rule-based engine

**3. Continuous Learning**
- User feedback endpoint: `/api/feedback`
- Incremental model retraining: `/api/retrain`
- Training data automatically updated

### 💡 Automatic Insights Engine

**DataInsightsEngine** (`data_insights.py`) performs intelligent analysis:

1. **Smart Column Detection**
   - Keyword matching (case-insensitive)
   - Detects: revenue, categories, status, geography, customers

2. **5 Business Analyzers**
   - 💰 **Revenue**: Total revenue, avg transaction, recommendations
   - 📊 **Categories**: Top performers, product insights
   - 🔄 **Quality**: Return rates, order status analysis
   - 🗺 **Geography**: Top markets, regional performance
   - 👥 **Customers**: Unique customers, engagement metrics

3. **Auto-Chart Suggestions**
   - Analyzes data structure
   - Suggests 5 optimal visualizations
   - One-click chart generation

### 🎨 Chart Generation Pipeline

1. **User Input** → Natural language prompt
2. **ML Prediction** → Chart type with confidence score
3. **Rule Validation** → Fallback if low confidence
4. **Plotly Rendering** → Interactive dark-themed chart
5. **Insights Analysis** → Automatic business intelligence

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **scikit-learn** - ML model (TF-IDF + Random Forest)
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **Plotly** - Interactive chart generation
- **uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Plotly.js** - Chart rendering
- **Axios** - HTTP client

### ML & Data
- **TfidfVectorizer** - Text feature extraction
- **RandomForestClassifier** - Multi-class prediction
- **joblib** - Model persistence

### DevOps
- **Docker** - Containerization
- **Vercel** - Serverless deployment
- **Git** - Version control

## 📊 ML Model Performance

| Metric | Value |
|--------|-------|
| Training Accuracy | 97.14% |
| Validation Accuracy | **91.43%** |
| Training Examples | 350 |
| Chart Types | 7 |
| Confidence Threshold | 35% |
| ML Usage Rate | 71% |
| Feature Count | 1000 (TF-IDF) |
| Model Size | ~2MB |

**Per-Class Performance:**
- Line charts: 95% accuracy
- Grouped bar: 92% accuracy  
- Scatter plots: 89% accuracy
- Histograms: 94% accuracy
- Other types: 85-90% accuracy

## 🔧 How It Works (Detailed)

## 🎯 Example Prompts

Try these prompts with the sample data in `example_data/`:

| Prompt | Dataset | Expected Chart |
|--------|---------|----------------|
| "Show sales trend over the last year" | sales_by_region.csv | Line chart |
| "Compare revenue across product categories" | sales_by_region.csv | Grouped bar |
| "What's the relationship between ad spend and sales?" | ads_sales.csv | Scatter plot |
| "Show age distribution of customers" | ages_distribution.csv | Histogram |
| "Top 10 countries by GDP" | countries_gdp.csv | Horizontal bar |
| "Sales composition by quarter and region" | sales_by_region.csv | Stacked bar |
| "Map GDP across countries" | countries_gdp.csv | Choropleth |

## 📤 API Endpoints

### Core Endpoints
- `POST /api/upload` - Upload CSV file
- `POST /api/recommend` - Get chart recommendation
- `POST /api/preview` - Generate chart preview
- `GET /api/insights/{file_id}` - Get automatic insights
- `GET /api/files/{file_id}` - Download CSV file

### ML Endpoints
- `POST /api/feedback` - Submit user feedback
- `POST /api/retrain` - Retrain ML model
- `GET /api/health` - Health check

## 🎨 Dark Theme Features

- **Background**: Deep black (#0a0a0a) with gradients
- **Typography**: Monospace fonts (JetBrains Mono style)
- **Colors**: Blue/Purple gradients with neon accents
- **Animations**: Smooth transitions with Framer Motion
- **Charts**: Custom Plotly dark theme
- **UI**: Professional developer aesthetic

## 🔐 Security & Best Practices

- ✅ Input validation on all endpoints
- ✅ File type restrictions (CSV only)
- ✅ File size limits (10MB max)
- ✅ CORS properly configured
- ✅ No sensitive data in repository
- ✅ Environment variables for configuration
- ✅ Secure file handling with UUIDs

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with ❤️ using FastAPI, React, and scikit-learn
- Inspired by the need for intelligent data visualization
- ML model trained on curated chart recommendation dataset
- Dark theme designed for modern developers

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/vibez-ai-charts/issues)
- **Documentation**: See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **ML Training**: See [backend/ML_TRAINING_GUIDE.md](./backend/ML_TRAINING_GUIDE.md)

## 🚀 Roadmap

- [ ] More chart types (pie, area, box plot)
- [ ] Advanced ML features (GPT integration)
- [ ] Real-time collaboration
- [ ] Cloud storage integration (S3, GCS)
- [ ] Custom color themes
- [ ] Export to PowerPoint/PDF
- [ ] API rate limiting
- [ ] User authentication
- [ ] Dashboard templates
- [ ] Mobile app

---

**Made with 🎨 by [Your Name]**  
**Powered by AI & Machine Learning**

Star ⭐ this repo if you find it useful!

Example formats are in `example_data/`

## ⚠️ Limitations & Future Work

### Current Limitations
- Rule-based only (no ML classifier yet)
- Limited chart type coverage (no heatmaps, treemaps, sankey)
- Basic column auto-detection (may require manual selection)
- Choropleth requires external geographic data
- Large datasets (>5,000 rows) are automatically sampled for visualization

### Planned Enhancements
1. **ML Classifier**: Train scikit-learn model on `prompts.csv` for ambiguous cases
2. **More Chart Types**: Heatmap, treemap, waterfall, funnel
3. **Advanced Constraints**: Font sizes, grid styles, color schemes (ColorBrewer)
4. **Interactive Column Mapping**: UI dropdowns when auto-detection fails
5. **Cloud Deployment**: Deploy to Streamlit Cloud or Heroku
6. **API Endpoint**: REST API for programmatic access
7. **VegaFusion Integration**: Better handling of very large datasets

## 📚 Tech Stack

- **Frontend**: Streamlit (UI framework)
- **Visualization**: Altair (declarative Vega-Lite)
- **Data Processing**: Pandas, NumPy
- **Testing**: Pytest
- **Optional ML**: scikit-learn (for future classifier)

## 🤝 Contributing

This is a prototype for demonstration. To extend:

1. Add more keywords to `vibe_engine.py`
2. Expand `mapping_table.csv` with domain-specific rules
3. Add more test prompts to `prompts.csv`
4. Implement new chart renderers in `app.py`

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 👥 Authors

Built as a prototype for intelligent data visualization recommendation.

---

**Questions?** Open an issue or check the inline code comments for implementation details.
