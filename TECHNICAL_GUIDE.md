# 🎓 Vibez AI Charts - Technical Interview Guide

## 📋 Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Main Files Explained](#main-files-explained)
3. [How It Works (Flow Diagram)](#how-it-works)
4. [Common Interview Questions](#common-interview-questions)
5. [Technical Deep Dives](#technical-deep-dives)

---

## 🏗️ Architecture Overview

### **High-Level Architecture**
```
┌─────────────────────────────────────────────────────┐
│                    USER BROWSER                      │
│                  (http://localhost:5173)             │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP/REST API
┌──────────────────────▼──────────────────────────────┐
│               FRONTEND (React + Vite)                │
│  ┌────────────────────────────────────────────────┐ │
│  │  App.tsx (Main Component)                      │ │
│  │  ├── FileUploader → Upload CSV                 │ │
│  │  ├── PromptBox → User input                    │ │
│  │  ├── InsightsPanel → AI insights               │ │
│  │  ├── ChartCanvas → Plotly visualization        │ │
│  │  └── KpiCards → Key metrics                    │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
│  API Client (lib/api.ts)                            │
└──────────────────────┬──────────────────────────────┘
                       │ axios.post()
┌──────────────────────▼──────────────────────────────┐
│            BACKEND (FastAPI + Python)                │
│  ┌────────────────────────────────────────────────┐ │
│  │  main.py (API Routes)                          │ │
│  │  ├── POST /api/upload → Save CSV               │ │
│  │  ├── POST /api/recommend → Get chart           │ │
│  │  ├── POST /api/insights → Analyze data         │ │
│  │  └── GET /api/download → Export chart          │ │
│  └────────────────────────────────────────────────┘ │
│                       │                              │
│  ┌──────────────┬─────┴────────┬─────────────────┐ │
│  │              │              │                  │ │
│  ▼              ▼              ▼                  ▼ │
│  ml_vibe_      vibe_        data_            chart_ │
│  engine.py     engine.py    insights.py      generator│
│  (ML Model)    (Rules)      (Analytics)      (Plotly)│
│                                                      │
│  models/vibe_classifier.pkl (Trained Random Forest) │
└──────────────────────────────────────────────────────┘
```

---

## 📁 Main Files Explained

### **BACKEND FILES**

#### **1. `backend/app/main.py`** (277 lines) - API Server
**What it does:**
- The main FastAPI application entry point
- Defines all API endpoints (routes)
- Handles CORS for cross-origin requests
- Coordinates between different modules

**Key Endpoints:**
```python
POST /api/upload          # Upload CSV file
POST /api/recommend       # Get chart recommendation
POST /api/preview         # Preview data
POST /api/insights        # Get AI insights
GET  /api/download/{id}   # Download chart as JSON
GET  /api/health          # Health check
```

**Interview Answer:**
*"main.py is the FastAPI server that orchestrates all API requests. When a user uploads a CSV, it saves the file, generates a unique ID, and returns summary statistics. When they request a chart, it calls the ML engine for predictions, then the chart generator to create Plotly specs."*

---

#### **2. `backend/app/ml_vibe_engine.py`** (ML Classifier)
**What it does:**
- Loads the trained Random Forest model
- Predicts chart types from natural language prompts
- Uses TF-IDF vectorization for text processing
- Returns confidence scores

**Key Components:**
```python
class MLVibeEngine:
    def __init__(self):
        self.model = joblib.load('models/vibe_classifier.pkl')
        self.vectorizer = model['vectorizer']
        self.classifier = model['classifier']
    
    def predict(self, prompt: str):
        # TF-IDF vectorization
        features = self.vectorizer.transform([prompt])
        # Random Forest prediction
        probabilities = self.classifier.predict_proba(features)
        confidence = max(probabilities[0])
        prediction = self.classifier.predict(features)[0]
        return prediction, confidence
```

**Interview Answer:**
*"The ML engine uses a trained Random Forest classifier with 91.43% accuracy. It takes a user's natural language prompt, converts it to TF-IDF features (1000 dimensions, 1-4 grams), and predicts one of 7 chart types. If confidence is below 35%, we fall back to rule-based logic."*

---

#### **3. `backend/app/vibe_engine.py`** (Rule-Based Fallback)
**What it does:**
- Pattern-matching logic for chart recommendations
- Fallback when ML confidence is low
- Keyword-based classification

**Key Logic:**
```python
def vibe_code(goal: str, insight_type: str):
    goal_lower = goal.lower()
    
    # Temporal patterns
    if any(word in goal_lower for word in ['trend', 'over time', 'timeline']):
        return 'line'
    
    # Comparison patterns
    if any(word in goal_lower for word in ['compare', 'vs', 'versus']):
        return 'bar'
    
    # Distribution patterns
    if any(word in goal_lower for word in ['distribution', 'spread']):
        return 'histogram'
```

**Interview Answer:**
*"The vibe_engine is a rule-based system that uses keyword matching. It's our fallback when ML confidence is low. It looks for patterns like 'trend over time' → line chart, 'compare regions' → bar chart. It's simpler but more explainable than ML."*

---

#### **4. `backend/app/data_insights.py`** (287 lines) - Business Intelligence
**What it does:**
- Automatically analyzes CSV data
- Generates 5 types of insights
- No configuration needed

**5 Analyzers:**
```python
class DataInsightsEngine:
    def _analyze_revenue(self, df):
        # Growth trends, top performers
        
    def _analyze_categories(self, df):
        # Distribution, winners/losers
        
    def _analyze_quality(self, df):
        # Ratings, satisfaction
        
    def _analyze_geography(self, df):
        # Regional patterns
        
    def _analyze_customers(self, df):
        # RFM analysis, segmentation
```

**Interview Answer:**
*"data_insights.py implements automatic business intelligence. It detects data patterns—revenue columns, category columns, geographic data—and generates insights without any user configuration. For example, it automatically calculates growth rates, identifies top performers, and segments customers."*

---

#### **5. `backend/app/chart_generator.py`** - Plotly Spec Generator
**What it does:**
- Creates Plotly.js chart specifications
- Supports 7 chart types
- Generates interactive configs

**Chart Types:**
```python
def generate_plotly_spec(df, chart_type, x_col, y_col):
    if chart_type == 'bar':
        return {'data': [{'type': 'bar', 'x': x_data, 'y': y_data}]}
    elif chart_type == 'line':
        return {'data': [{'type': 'scatter', 'mode': 'lines'}]}
    elif chart_type == 'pie':
        return {'data': [{'type': 'pie', 'labels': labels}]}
    # ... 4 more types
```

**Interview Answer:**
*"chart_generator.py converts our prediction into actual Plotly JSON specs. It takes the chart type, data, and column mappings, then generates a complete Plotly configuration that the frontend can render directly. It handles all 7 chart types we support."*

---

#### **6. `backend/train_ml_model.py`** - ML Training Script
**What it does:**
- Trains the Random Forest classifier
- Creates TF-IDF vectorizer
- Saves model to disk

**Training Process:**
```python
# 1. Load training data (350 examples)
data = [
    ("show sales trends over time", "line"),
    ("compare revenue by region", "bar"),
    # ... 348 more examples
]

# 2. TF-IDF vectorization
vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1,4))

# 3. Train Random Forest
classifier = RandomForestClassifier(n_estimators=200, max_depth=15)

# 4. Save model
joblib.dump({'vectorizer': vectorizer, 'classifier': classifier}, 
            'models/vibe_classifier.pkl')
```

**Interview Answer:**
*"I wrote a custom training script that uses 350 labeled examples. It creates a TF-IDF vectorizer with 1000 features and 1-4 grams to capture multi-word patterns like 'over time'. Then trains a Random Forest with 200 trees. This achieved 91.43% validation accuracy."*

---

### **FRONTEND FILES**

#### **7. `frontend/src/App.tsx`** (Main React Component)
**What it does:**
- Root component that orchestrates the UI
- Manages application state
- Coordinates child components

**Key State:**
```typescript
const [fileId, setFileId] = useState<string>('');
const [summary, setSummary] = useState<any>(null);
const [insights, setInsights] = useState<any>(null);
const { loading, result, error, getRecommendation } = useVibe();
```

**Data Flow:**
```
1. User uploads CSV → FileUploader
2. handleUploadSuccess() → setFileId, setSummary
3. Auto-fetch insights → api.getInsights()
4. User types prompt → PromptBox
5. handlePromptSubmit() → useVibe hook
6. Result → ChartCanvas renders
```

**Interview Answer:**
*"App.tsx is the main React component. It manages state for uploaded files, insights, and chart results. When a file uploads, it automatically fetches AI insights. When a user submits a prompt, it calls the recommend API and displays the chart. It's a typical React state management pattern."*

---

#### **8. `frontend/src/lib/api.ts`** - API Client
**What it does:**
- Centralized API communication
- Type-safe requests with TypeScript
- Error handling

**Implementation:**
```typescript
const API_BASE = import.meta.env.VITE_API_BASE_URL || 
                 (import.meta.env.DEV ? 
                  'http://localhost:8000' : '/api');

export const api = {
    async recommend(req: RecommendRequest): Promise<RecommendResponse> {
        const { data } = await axios.post(`${API_BASE}/recommend`, req);
        return data;
    },
    
    async upload(file: File): Promise<UploadResponse> {
        const formData = new FormData();
        formData.append('file', file);
        const { data } = await axios.post(`${API_BASE}/upload`, formData);
        return data;
    },
    // ... more methods
};
```

**Interview Answer:**
*"api.ts is our API client layer. It abstracts all backend communication, provides type safety with TypeScript interfaces, and handles environment-specific base URLs. In development, it points to localhost:8000; in production, it uses relative paths for Vercel deployment."*

---

#### **9. `frontend/src/hooks/useVibe.ts`** - Custom React Hook
**What it does:**
- Encapsulates recommendation logic
- Manages loading/error states
- Reusable across components

**Implementation:**
```typescript
export const useVibe = () => {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<RecommendResponse | null>(null);
    const [error, setError] = useState<string | null>(null);
    
    const getRecommendation = async (req: RecommendRequest) => {
        setLoading(true);
        try {
            const data = await api.recommend(req);
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };
    
    return { loading, result, error, getRecommendation, reset };
};
```

**Interview Answer:**
*"useVibe is a custom React hook following best practices. It encapsulates the recommendation flow—loading state, API call, error handling, and result management. This keeps components clean and makes the logic reusable. It's a common pattern in modern React development."*

---

#### **10. `frontend/src/components/ChartCanvas.tsx`** - Chart Renderer
**What it does:**
- Renders Plotly charts
- Handles user interactions
- Export functionality

**Key Code:**
```typescript
import Plot from 'react-plotly.js';

export default function ChartCanvas({ spec, vibe }) {
    return (
        <div className="bg-gray-900 p-6 rounded-lg">
            <Plot
                data={spec.data}
                layout={{
                    ...spec.layout,
                    paper_bgcolor: '#111827',
                    plot_bgcolor: '#1f2937',
                    font: { color: '#e5e7eb' }
                }}
                config={{ responsive: true }}
            />
        </div>
    );
}
```

**Interview Answer:**
*"ChartCanvas takes the Plotly spec from the backend and renders it using react-plotly.js. I customized the theme to match our dark UI. It's a thin wrapper that adds export functionality and integrates with our design system."*

---

## 🔄 How It Works (Complete Flow)

### **User Journey Flow**

```
┌─────────────────────────────────────────────────────────┐
│ STEP 1: Upload CSV File                                 │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
    User drops sales_2024.csv into FileUploader
                         │
                         ▼
    FileUploader.tsx → api.upload(file)
                         │
                         ▼
    POST /api/upload (main.py)
                         │
                         ▼
    1. Generate UUID (e.g., "abc-123")
    2. Save to backend/data/abc-123.csv
    3. Load CSV with pandas
    4. Infer schema (columns, types)
    5. Calculate summary (rows, columns, preview)
                         │
                         ▼
    Return: {file_id: "abc-123", summary: {...}}
                         │
                         ▼
    App.tsx → handleUploadSuccess()
                         │
                         ▼
    Auto-trigger: api.getInsights(file_id)
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 2: Generate Insights                               │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
    POST /api/insights (main.py)
                         │
                         ▼
    DataInsightsEngine.generate_insights(df)
                         │
      ┌─────────────────┼─────────────────┐
      │                 │                 │
      ▼                 ▼                 ▼
   Analyze          Analyze          Analyze
   Revenue        Categories       Geography
      │                 │                 │
      └─────────────────┴─────────────────┘
                         │
                         ▼
    Return: {
        insights: [
            {category: "Revenue", summary: "Grew 24%"},
            {category: "Geography", summary: "NA leads"}
        ],
        auto_charts: ["Show sales trends", "Compare regions"]
    }
                         │
                         ▼
    InsightsPanel displays 5 insights + suggested charts
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 3: User Types Prompt                               │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
    User types: "show sales trends over time"
                         │
                         ▼
    PromptBox → handlePromptSubmit()
                         │
                         ▼
    useVibe.getRecommendation({
        goal: "show sales trends over time",
        file_id: "abc-123"
    })
                         │
                         ▼
    POST /api/recommend (main.py)
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 4: ML Prediction                                   │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
    ml_engine.predict("show sales trends over time")
                         │
      ┌─────────────────┴─────────────────┐
      │                                   │
      ▼                                   ▼
   TF-IDF Vectorization            Random Forest
   "show sales trends"    →        200 decision trees
   → [0.12, 0.0, 0.8, ...]         Vote on chart type
      │                                   │
      └─────────────────┬─────────────────┘
                         │
                         ▼
    Prediction: "line", Confidence: 0.87
                         │
                         ▼
    Confidence ≥ 35%? YES → Use ML prediction
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 5: Generate Chart Spec                             │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
    Load CSV: backend/data/abc-123.csv
                         │
                         ▼
    Detect temporal column (e.g., "date")
    Detect value column (e.g., "sales")
                         │
                         ▼
    chart_generator.generate_plotly_spec(
        df, 
        chart_type='line',
        x='date',
        y='sales'
    )
                         │
                         ▼
    Return: {
        vibe: "line",
        confidence: 0.87,
        chart_spec: {
            data: [{type: 'scatter', mode: 'lines', ...}],
            layout: {title: 'Sales Trends', ...}
        }
    }
                         │
                         ▼
    ChartCanvas receives spec → Plot renders
                         │
                         ▼
    ✅ User sees interactive line chart!
```

---

## ❓ Common Interview Questions

### **Q1: "Walk me through your architecture"**

**Answer:**
*"It's a full-stack application with a React frontend and FastAPI backend. The frontend is built with TypeScript, Vite, and Plotly for charts. Users upload CSVs and describe what they want to see in natural language.*

*The backend has three layers: First, the API layer (main.py) handles HTTP requests. Second, the intelligence layer has both ML (Random Forest with 91% accuracy) and rule-based engines. Third, the data layer generates Plotly specs and automatic insights.*

*When a user types 'show sales trends,' the prompt goes to the ML engine, which predicts 'line chart' with confidence. If confidence is high, we use that; otherwise, we fall back to keyword rules. Then we generate a Plotly JSON spec and send it back to render."*

---

### **Q2: "How does your ML model work?"**

**Answer:**
*"I trained a Random Forest classifier on 350 labeled examples. Each example is a natural language prompt paired with the correct chart type—7 types total: bar, line, pie, scatter, area, funnel, heatmap.*

*For text processing, I use TF-IDF vectorization with 1000 features and 1-4 grams. The n-grams capture phrases like 'over time' which strongly indicate temporal charts.*

*The Random Forest has 200 trees with max depth 15. I used 80/20 train-validation split and achieved 97% training accuracy, 91% validation accuracy. In production, I set a 35% confidence threshold—if the model is confident, use it; otherwise, fall back to rules. This gives us 71% ML usage rate."*

---

### **Q3: "How do you handle the frontend-backend communication?"**

**Answer:**
*"I use a centralized API client pattern. There's an api.ts file with typed functions for each endpoint—recommend, upload, insights, etc. All use axios for HTTP requests.*

*For type safety, I defined TypeScript interfaces that match the backend Pydantic schemas—RecommendRequest, RecommendResponse, etc. This catches errors at compile time.*

*For state management, I use React hooks. The useVibe custom hook encapsulates the recommendation flow with loading, error, and result states. Components just call the hook—no direct API calls in components."*

---

### **Q4: "What was the biggest technical challenge?"**

**Answer:**
*"The ML accuracy. Initially, I had only 70 training examples and got 50% validation accuracy—barely better than random.*

*I expanded to 350 examples and tuned hyperparameters: increased TF-IDF features from 500 to 1000, changed n-grams from 1-2 to 1-4, increased Random Forest trees from 100 to 200, and adjusted max depth from 10 to 15.*

*But the key insight was the confidence threshold. Instead of always using ML, I set a 35% threshold. This balanced accuracy with coverage—71% of prompts use ML at high confidence, the rest use reliable rule-based logic. That hybrid approach was the breakthrough."*

---

### **Q5: "How would you scale this system?"**

**Answer:**
*"Several strategies:*

*1. **Caching**: Add Redis to cache chart specs for common prompt+data combinations. ML inference is fast, but why recompute?*

*2. **Database**: Move from file storage to PostgreSQL. Store metadata (file_id, columns, stats) for faster lookups.*

*3. **Queue**: For large files, use Celery with Redis to process uploads asynchronously. Return a job_id, poll for status.*

*4. **Model Serving**: Move ML to a separate service (TensorFlow Serving or FastAPI microservice). Scale independently from main API.*

*5. **CDN**: Serve static frontend from Cloudflare. API stays on Vercel/AWS.*

*6. **Rate Limiting**: Add per-user API limits to prevent abuse."*

---

### **Q6: "Why did you choose these technologies?"**

**Answer:**
*"**FastAPI** because it's fast, has automatic OpenAPI docs, and native async support. Perfect for ML inference endpoints.*

***React + TypeScript** for type safety and component reusability. Vite for instant HMR during development.*

***scikit-learn** because I needed a lightweight, explainable model. Random Forest is interpretable—I can see feature importance. TensorFlow would be overkill.*

***Plotly** for interactive charts that work in browsers. No canvas rendering, just JSON specs.*

*The whole stack is modern, well-documented, and has great ecosystems."*

---

### **Q7: "How do you ensure data quality?"**

**Answer:**
*"Multiple validation layers:*

*1. **Upload validation**: Check file size (< 10MB), format (CSV), encoding (UTF-8).*

*2. **Schema inference**: Detect column types (numeric, temporal, categorical). Reject if < 2 columns.*

*3. **Data preview**: Show first 10 rows so users verify data loaded correctly.*

*4. **Constraint generation**: Auto-detect valid columns for x/y axes based on chart type.*

*5. **Error handling**: Graceful failures with specific messages—'No temporal column found for line chart'."*

---

### **Q8: "What would you add next?"**

**Answer:**
*"Three priorities:*

*1. **User feedback loop**: Add thumbs up/down on charts. Retrain model with user corrections. Active learning.*

*2. **OpenAI integration**: Generate natural language narratives from insights. 'Your sales grew 23% in Q4, driven by...'*

*3. **Real-time data**: WebSocket support for streaming data. Live updating dashboards."*

---

## 🔬 Technical Deep Dives

### **Deep Dive 1: Why Random Forest over Neural Networks?**

**Tradeoffs:**

| Aspect | Random Forest | Neural Network |
|--------|--------------|----------------|
| Training Time | 2 minutes | 30+ minutes |
| Inference | <50ms | ~100ms |
| Data Needed | 350 examples ✅ | 5000+ examples ❌ |
| Interpretability | High ✅ | Low ❌ |
| Model Size | 0.31 MB ✅ | 50+ MB ❌ |
| Overfitting Risk | Low ✅ | High ❌ |

**Decision:**
*"For 350 examples, Random Forest is optimal. Neural networks would overfit. I value speed and explainability over marginal accuracy gains."*

---

### **Deep Dive 2: TF-IDF Feature Engineering**

**Why TF-IDF?**
```python
TfidfVectorizer(
    max_features=1000,      # Top 1000 most informative terms
    ngram_range=(1, 4),     # Capture "over time" as one feature
    sublinear_tf=True,      # Log scaling for term frequency
    min_df=2,               # Ignore rare terms
    max_df=0.95             # Ignore common terms
)
```

**Example:**
```
Prompt: "show sales trends over time"

Unigrams: [show, sales, trends, over, time]
Bigrams:  [show sales, sales trends, trends over, over time]
Trigrams: [show sales trends, sales trends over, trends over time]
4-grams:  [show sales trends over, sales trends over time]

→ TF-IDF vector: [0.0, 0.3, 0.8, 0.0, 0.5, ...]
                     ↑ "over time" has high weight
                     
→ Random Forest sees this pattern → predicts "line"
```

**Why not word embeddings (Word2Vec)?**
*"TF-IDF is simpler, faster, and works well for keyword-heavy tasks. Embeddings are overkill for 7 classes."*

---

### **Deep Dive 3: Confidence Threshold Optimization**

**Experiment Results:**
| Threshold | ML Usage | Accuracy | Explanation |
|-----------|----------|----------|-------------|
| 0% (always ML) | 100% | 91.43% | Some mistakes |
| 25% | 85% | 94% | Better accuracy |
| **35%** | **71%** | **96%** | ✅ Optimal |
| 50% | 45% | 97% | Too conservative |
| 75% | 15% | 98% | Underutilizing ML |

**Analysis:**
*"35% threshold gives the best accuracy-coverage tradeoff. We use ML for 71% of prompts at high confidence, fall back to rules for ambiguous cases. This hybrid approach beats pure ML or pure rules."*

---

### **Deep Dive 4: React State Management Strategy**

**Why not Redux?**
*"For this app size, useState + custom hooks is sufficient. Redux adds boilerplate without benefits. Our state is simple:*
- *fileId (string)*
- *summary (object)*
- *insights (array)*
- *result (object)*

*No complex global state, no deeply nested data. React hooks are perfect."*

**Custom Hook Pattern:**
```typescript
// Encapsulation: Hide API logic
// Reusability: Use in multiple components
// Testability: Mock the hook easily

export const useVibe = () => {
    const [state, setState] = useState({...});
    
    const getRecommendation = async (req) => {
        // API call logic
    };
    
    return { ...state, getRecommendation };
};
```

---

## 🎯 Key Talking Points for Interviews

### **Achievements to Highlight:**

1. ✅ **91.43% ML accuracy** - Through systematic hyperparameter tuning
2. ✅ **Hybrid ML/Rule system** - 35% confidence threshold optimization
3. ✅ **Zero-config insights** - Automatic detection of 5 analysis types
4. ✅ **Full-stack ownership** - Designed, implemented, deployed end-to-end
5. ✅ **Production deployment** - Docker, Vercel, GitHub Actions
6. ✅ **Type-safe architecture** - TypeScript + Pydantic schemas
7. ✅ **Modern best practices** - React hooks, FastAPI async, modular design

### **Technical Skills Demonstrated:**

- **ML/AI**: scikit-learn, Random Forest, TF-IDF, hyperparameter tuning
- **Backend**: Python, FastAPI, pandas, async programming
- **Frontend**: React, TypeScript, Vite, custom hooks, Plotly
- **DevOps**: Docker, Git, Vercel, environment configs
- **Data**: CSV processing, schema inference, data validation
- **Architecture**: REST APIs, microservices, separation of concerns

---

## 📝 Quick Reference Card

**Elevator Pitch (30 seconds):**
*"I built Vibez AI Charts, an ML-powered data visualization tool. Users upload CSVs and describe what they want to see in natural language—'show sales trends'—and the app generates professional charts. I trained a Random Forest classifier on 350 examples achieving 91% accuracy. The full stack uses FastAPI backend, React frontend, with automatic business insights. It's deployed on Vercel with Docker configs."*

**If they ask about ML:**
*"Random Forest with TF-IDF features. 1000 dimensions, 1-4 grams to capture phrases. 91.43% validation accuracy on 7 chart types. 35% confidence threshold for hybrid ML/rule approach."*

**If they ask about architecture:**
*"React + TypeScript frontend, FastAPI backend. Custom hooks for state, api.ts for HTTP layer. Backend has ML engine, rule engine, chart generator, and insights analyzer. All type-safe with Pydantic schemas."*

**If they ask about scale:**
*"Currently file-based, but designed for scale. Add Redis caching, PostgreSQL storage, Celery queues, separate ML microservice. All stateless, horizontally scalable."*

---

## 🎓 Practice Scenarios

### **Scenario 1: Technical Walkthrough**
*"Tell me how a user's request flows through your system."*

**Your Answer:**
*"User uploads CSV → FileUploader calls api.upload() → POST /api/upload saves file, returns file_id → App.tsx auto-fetches insights → DataInsightsEngine analyzes → User types prompt → useVibe hook calls api.recommend() → ML engine predicts chart type → chart_generator creates Plotly spec → ChartCanvas renders → User sees chart."*

---

### **Scenario 2: Debugging Question**
*"User says 'chart isn't loading.' How do you debug?"*

**Your Answer:**
*"1. Check browser console for errors. 2. Verify file uploaded successfully (file_id exists). 3. Check network tab—did /api/recommend return 200? 4. Inspect response JSON—is chart_spec valid? 5. Check backend logs for ML errors. 6. Validate CSV has required columns. 7. Test with sample data to isolate issue."*

---

### **Scenario 3: Optimization Question**
*"App is slow for large files. How do you optimize?"*

**Your Answer:**
*"1. Add file size limit (current: 10MB). 2. Stream CSV parsing (don't load entire file). 3. Sample data for insights (analyze 10K rows, not 1M). 4. Cache Plotly specs. 5. Paginate data preview. 6. Add loading states. 7. Use web workers for client-side processing. 8. Implement lazy loading for charts."*

---

**Remember:** You built a sophisticated, production-ready ML application. Be confident! You understand every line of code. 🚀
