# backend/app/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.vibe_engine import vibe_code, get_constraints, sample_data_for_vibe
from app.data_utils import infer_schema_from_df, load_csv
from app.schemas import RecommendRequest, RecommendResponse, UploadResponse, PreviewRequest, PreviewResponse
from app.chart_generator import generate_plotly_spec
from app.ml_vibe_engine import get_ml_engine
from app.data_insights import DataInsightsEngine
from app.ai_storyteller import get_storyteller
from app.data_qa import create_qa_engine
import uuid
import os
import pandas as pd
from pathlib import Path
from pydantic import BaseModel

app = FastAPI(title="Vibe-Code API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Vibe-Code API", "version": "1.0.0", "status": "running"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/recommend", response_model=RecommendResponse)
async def recommend(req: RecommendRequest):
    """
    Generate chart recommendation based on user's data goal.
    Uses ML-based prediction with rule-based fallback.
    Optionally uses uploaded file data for adaptive constraints.
    """
    try:
        # Try ML prediction first
        ml_engine = get_ml_engine()
        ml_prediction = None
        confidence = 0.0
        
        if ml_engine.is_trained:
            result = ml_engine.predict(req.goal)
            ml_prediction = result['chart_type']
            confidence = result['confidence']
        
        # Use ML prediction if confidence is high enough, otherwise fallback to rule-based
        # Threshold lowered to 35% because Random Forest spreads probability across classes
        if ml_prediction and confidence > 0.35:
            vibe = ml_prediction
            print(f"🤖 ML predicted '{vibe}' with {confidence:.1%} confidence for: '{req.goal}'")
        else:
            vibe = vibe_code(req.goal)
            print(f"📋 Rule-based matched '{vibe}' for: '{req.goal}'")
        
        # Load file data if provided
        dataset_features = None
        df = None
        if req.file_id:
            file_path = DATA_DIR / f"{req.file_id}.csv"
            if file_path.exists():
                df = pd.read_csv(file_path)
                # Sample if too large
                if len(df) > 5000:
                    df = df.sample(n=5000, random_state=42)
                dataset_features = infer_schema_from_df(df)
        
        # Get constraints
        constraints = get_constraints(vibe, dataset_features)
        
        # Generate sample chart spec
        if df is not None:
            chart_spec = generate_plotly_spec(vibe, df)
        else:
            # Use synthetic sample data
            sample_df = sample_data_for_vibe(vibe)
            chart_spec = generate_plotly_spec(vibe, sample_df)
        
        return RecommendResponse(
            vibe=vibe,
            constraints=constraints,
            rationale=constraints.get("rationale", ""),
            chart_spec=chart_spec
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a CSV file and return dataset summary.
    """
    try:
        # Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")
        
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        file_path = DATA_DIR / f"{file_id}.csv"
        
        # Save file
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Analyze file
        df = pd.read_csv(file_path)
        summary = infer_schema_from_df(df)
        
        # Add column info
        summary["columns"] = [
            {
                "name": col,
                "dtype": str(df[col].dtype),
                "sample_values": df[col].head(3).tolist()
            }
            for col in df.columns
        ]
        
        return UploadResponse(
            file_id=file_id,
            filename=file.filename,
            summary=summary
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/preview", response_model=PreviewResponse)
async def preview_chart(req: PreviewRequest):
    """
    Generate a chart preview with specific column selections.
    """
    try:
        # Load data
        if req.file_id:
            file_path = DATA_DIR / f"{req.file_id}.csv"
            if not file_path.exists():
                raise HTTPException(status_code=404, detail="File not found")
            df = pd.read_csv(file_path)
            # Sample if large
            if len(df) > 5000:
                df = df.sample(n=5000, random_state=42)
        else:
            # Use sample data
            df = sample_data_for_vibe(req.vibe)
        
        # Generate chart spec
        chart_spec = generate_plotly_spec(
            req.vibe,
            df,
            x_col=req.x_col,
            y_col=req.y_col,
            group_col=req.group_col
        )
        
        return PreviewResponse(
            chart_spec=chart_spec,
            library=chart_spec.get("library", "plotly")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/{file_id}")
async def download_file(file_id: str):
    """
    Download a previously uploaded file.
    """
    file_path = DATA_DIR / f"{file_id}.csv"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type="text/csv",
        filename=f"data_{file_id}.csv"
    )

@app.delete("/api/files/{file_id}")
async def delete_file(file_id: str):
    """
    Delete an uploaded file.
    """
    file_path = DATA_DIR / f"{file_id}.csv"
    if file_path.exists():
        os.remove(file_path)
        return {"message": "File deleted successfully"}
    raise HTTPException(status_code=404, detail="File not found")

@app.post("/api/feedback")
async def submit_feedback(prompt: str, predicted_vibe: str, correct_vibe: str):
    """
    Submit user feedback to improve ML model.
    This collects corrections when the model predicts incorrectly.
    """
    try:
        ml_engine = get_ml_engine()
        ml_engine.add_feedback(prompt, correct_vibe)
        return {
            "message": "Feedback recorded successfully",
            "prompt": prompt,
            "predicted": predicted_vibe,
            "corrected_to": correct_vibe
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/retrain")
async def retrain_model():
    """
    Retrain the ML model using collected feedback.
    Should be called periodically (e.g., after collecting 50+ feedback examples).
    """
    try:
        ml_engine = get_ml_engine()
        accuracy = ml_engine.retrain_from_feedback()
        
        if accuracy is not None:
            return {
                "message": "Model retrained successfully",
                "new_accuracy": f"{accuracy:.1%}",
                "status": "success"
            }
        else:
            return {
                "message": "No feedback data available for retraining",
                "status": "skipped"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/insights/{file_id}")
async def get_insights(file_id: str):
    """
    Generate automatic business insights from uploaded data.
    Returns 5 key insights, recommendations, and suggested visualizations.
    NOW WITH AI-POWERED STORYTELLING!
    """
    try:
        file_path = DATA_DIR / f"{file_id}.csv"
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Load data
        df = pd.read_csv(file_path)
        
        # Generate insights
        engine = DataInsightsEngine(df)
        analysis = engine.analyze()
        
        # Generate AI story from insights
        storyteller = get_storyteller()
        ai_story = None
        ai_suggestions = []
        
        if storyteller:
            try:
                # Create data summary for AI
                data_summary = {
                    'total_rows': len(df),
                    'total_columns': len(df.columns),
                    'columns': list(df.columns)
                }
                
                # Generate compelling narrative
                ai_story = storyteller.generate_story(
                    analysis['insights'], 
                    data_summary
                )
                
                # Get AI-powered suggestions
                ai_suggestions = storyteller.suggest_next_analysis(
                    analysis['insights']
                )
                
            except Exception as e:
                print(f"AI storytelling failed: {e}")
                # Continue without AI features
        
        return {
            "file_id": file_id,
            "insights": analysis['insights'],
            "recommendations": analysis['recommendations'],
            "auto_charts": analysis['auto_charts'],
            "statistics": analysis['statistics'],
            "ai_story": ai_story,  # NEW: AI-generated narrative
            "ai_suggestions": ai_suggestions  # NEW: Smart follow-up questions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insights generation failed: {str(e)}")

# Q&A Request Model
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    file_id: str
    question: str

@app.post("/api/ask")
async def ask_question(req: QuestionRequest):
    """
    Answer natural language questions about the data using Gemini AI.
    Examples:
    - "What are the top 5 products by sales?"
    - "Which region has the highest revenue?"
    - "Show me sales trends over time"
    - "What's the average order value?"
    """
    try:
        file_path = DATA_DIR / f"{req.file_id}.csv"
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Load data
        df = pd.read_csv(file_path)
        
        # Create Q&A engine
        qa_engine = create_qa_engine(df)
        
        # Answer the question
        result = qa_engine.ask(req.question)
        
        return {
            "question": req.question,
            "answer": result['answer'],
            "success": result['success'],
            "data_summary": result.get('data_summary', {})
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
