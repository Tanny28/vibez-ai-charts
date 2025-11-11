# backend/app/schemas.py
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class RecommendRequest(BaseModel):
    goal: str
    insight: str = "Auto"
    file_id: Optional[str] = None

class RecommendResponse(BaseModel):
    vibe: str
    constraints: Dict[str, str]
    rationale: str
    chart_spec: Dict[str, Any]

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    summary: Dict[str, Any]

class PreviewRequest(BaseModel):
    file_id: Optional[str] = None
    vibe: str
    x_col: Optional[str] = None
    y_col: Optional[str] = None
    group_col: Optional[str] = None
    options: Optional[Dict[str, Any]] = {}

class PreviewResponse(BaseModel):
    chart_spec: Dict[str, Any]
    library: str  # "plotly" or "vega"
