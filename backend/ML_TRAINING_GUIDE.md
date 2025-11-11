# ML-Based Chart Recommendation System

## Overview

The Vibez AI system now supports **machine learning-based chart recommendations** that can be trained on real user data for improved accuracy.

## Quick Start

### 1. Install ML Dependencies

```bash
cd backend
pip install scikit-learn>=1.3.0
```

### 2. Train the Initial Model

```bash
cd backend
python train_ml_model.py
```

This will:
- Train a Random Forest classifier on 80+ example prompts
- Save the model to `backend/models/vibe_classifier.pkl`
- Show training and validation accuracy
- Test the model with sample predictions

Expected output:
```
Training Accuracy: 95-100%
Validation Accuracy: 85-95%
```

### 3. Use ML Model in API

Update `backend/app/main.py` to use the ML engine:

```python
from app.ml_vibe_engine import get_ml_engine

@app.post("/api/recommend")
async def recommend_chart(request: RecommendRequest):
    # Get ML prediction
    ml_engine = get_ml_engine()
    prediction = ml_engine.predict(request.goal, get_probabilities=True)
    
    # Use ML prediction
    vibe = prediction['chart_type']
    confidence = prediction['confidence']
    
    # ... rest of your code
```

## Training on Your Own Data

### Method 1: Add to Training Script

Edit `backend/train_ml_model.py` and add your examples:

```python
TRAINING_DATA = [
    ("your custom prompt", "grouped_bar"),
    ("another prompt", "line"),
    # ... add more
]
```

Then retrain:
```bash
python train_ml_model.py
```

### Method 2: Collect User Feedback

Add a feedback mechanism in your UI that records which chart types work best:

```python
from app.ml_vibe_engine import get_ml_engine

# When user confirms a chart worked well
ml_engine = get_ml_engine()
ml_engine.add_feedback(
    prompt="show sales trends",
    correct_chart_type="line"
)
```

Then retrain from feedback:
```python
ml_engine.retrain_from_feedback("backend/data/user_feedback.jsonl")
```

### Method 3: Import Real Dataset

If you have a CSV with labeled data:

```python
import pandas as pd
from app.ml_vibe_engine import MLVibeEngine

# Load your dataset
df = pd.read_csv("your_labeled_data.csv")
# Expected columns: 'prompt', 'chart_type'

# Convert to training format
training_data = list(zip(df['prompt'], df['chart_type']))

# Train
engine = MLVibeEngine()
engine.train(training_data)
```

## Dataset Format

Your training data should be a list of tuples:

```python
[
    ("user prompt 1", "chart_type"),
    ("user prompt 2", "chart_type"),
    ...
]
```

Supported chart types:
- `line` - Time series, trends
- `grouped_bar` - Comparisons
- `histogram` - Distributions
- `scatter` - Correlations
- `stacked_bar` - Compositions
- `horizontal_bar` - Rankings
- `choropleth` - Geographic data

## Model Performance

### Current Baseline (Rule-Based)
- Accuracy: ~70-80% on structured prompts
- Limitations: Requires exact keyword matches

### With ML Model (Trained)
- Training Accuracy: 95-100%
- Validation Accuracy: 85-95%
- Benefits:
  - Handles variations in phrasing
  - Learns from user patterns
  - Provides confidence scores
  - Improves over time

## Advanced: Continuous Learning

### Step 1: Add Feedback Endpoint

```python
# In main.py
@app.post("/api/feedback")
async def record_feedback(
    prompt: str,
    chart_type: str,
    helpful: bool
):
    if helpful:
        ml_engine = get_ml_engine()
        ml_engine.add_feedback(prompt, chart_type)
    return {"status": "recorded"}
```

### Step 2: Add UI Feedback Buttons

```tsx
// In ChartCanvas.tsx
<button onClick={() => sendFeedback(true)}>
  👍 This chart works great
</button>
<button onClick={() => sendFeedback(false)}>
  👎 Try different chart
</button>
```

### Step 3: Periodic Retraining

Set up a cron job or scheduled task:

```bash
# Retrain weekly with new feedback
0 0 * * 0 cd /app/backend && python -c "
from app.ml_vibe_engine import get_ml_engine
engine = get_ml_engine()
engine.retrain_from_feedback()
"
```

## Integration with Current System

### Hybrid Approach (Recommended)

Use ML as primary, fallback to rules:

```python
def get_vibe(prompt: str):
    ml_engine = get_ml_engine()
    
    if ml_engine.is_trained:
        result = ml_engine.predict(prompt)
        if result['confidence'] > 0.7:  # High confidence
            return result['chart_type']
    
    # Fallback to rule-based
    return vibe_code(prompt)  # Original function
```

## Troubleshooting

**Model not loading:**
- Ensure `backend/models/vibe_classifier.pkl` exists
- Run `python train_ml_model.py` to create it

**Low accuracy:**
- Add more training examples (aim for 100+ per chart type)
- Collect real user feedback
- Balance dataset across all chart types

**Import errors:**
- Install scikit-learn: `pip install scikit-learn`
- Check Python version (requires 3.9+)

## Next Steps

1. ✅ Train initial model with sample data
2. ✅ Integrate into API
3. 🔄 Collect user feedback for 1-2 weeks
4. 🔄 Retrain with real usage data
5. 🔄 Monitor accuracy improvements
6. 🔄 Expand training dataset to 500+ examples

---

**Pro Tip:** Start with the hybrid approach to ensure reliability while collecting training data!
