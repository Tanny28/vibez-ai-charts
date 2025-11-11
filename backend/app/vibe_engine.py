# backend/app/vibe_engine.py
# Ported from root vibe_engine.py for backend use
import csv
import os
import json
from typing import Optional, Dict
import pandas as pd
import numpy as np

# Load mapping_table into memory
MAP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "mapping_table.csv")
_mapping = []
if os.path.exists(MAP_PATH):
    with open(MAP_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, fieldnames=["goal_keyword","chart_type","palette","axis_rule","label_rule","rationale"])
        next(reader)  # Skip header
        for row in reader:
            _mapping.append(row)

# keyword sets
KEYWORDS = {
    "comparison": ["compare","across","vs","versus","difference","broken down by","per region","per category"],
    "trend": ["trend","over time","year","monthly","weekly","daily","growth","increase","decrease","time series","period"],
    "distribution": ["distribution","histogram","spread","density","ages","frequency","distribution of"],
    "correlation": ["relationship","correlation","affect","impact","scatter"],
    "composition": ["share","composition","part of","percentage","market share","proportion"],
    "ranking": ["top","ranking","rank","best","worst","top selling","top performers"],
    "geospatial": ["map","country","state","lat","lon","longitude","latitude","choropleth"]
}

def vibe_code(goal_text: str) -> str:
    """Determine the recommended chart type based on the user's data goal."""
    t = goal_text.lower()
    # priority checks
    if any(k in t for k in KEYWORDS["trend"]):
        return "line"
    if any(k in t for k in KEYWORDS["comparison"]):
        return "grouped_bar"
    if any(k in t for k in KEYWORDS["distribution"]):
        return "histogram"
    if any(k in t for k in KEYWORDS["correlation"]):
        return "scatter"
    if any(k in t for k in KEYWORDS["composition"]):
        return "stacked_bar"
    if any(k in t for k in KEYWORDS["ranking"]):
        return "horizontal_bar"
    if any(k in t for k in KEYWORDS["geospatial"]):
        return "choropleth"
    # fallback: try mapping_table keywords
    for row in _mapping:
        key = row.get("goal_keyword") or ""
        if key and key in t:
            return row.get("chart_type","grouped_bar")
    # default
    return "grouped_bar"

def get_constraints(vibe: str, dataset_features: Optional[Dict]=None) -> Dict:
    """Get design constraints (palette, axis, labeling) for a given vibe code."""
    # default constraints
    constraints = {
        "grouped_bar": {
            "palette":"qualitative_max6",
            "axis":"y_start_zero;integer_ticks;sort_desc",
            "labeling":"value_labels_on_bars;highlight_top",
            "rationale":"Bars make magnitude comparison immediate; sorting guides the eye."
        },
        "line": {
            "palette":"single_sequential",
            "axis":"time_x;linear_y;yearly_ticks",
            "labeling":"annotate_start_end;show_percent_change",
            "rationale":"Line charts show slope and trends over time."
        },
        "histogram": {
            "palette":"neutral_sequential",
            "axis":"equal_bin_width;show_counts",
            "labeling":"label_mean_median;highlight_outliers",
            "rationale":"Histogram reveals distribution and density."
        },
        "scatter": {
            "palette":"diverging_for_trend",
            "axis":"linear_both;fit_line_optional",
            "labeling":"annotate_trendline;highlight_outliers",
            "rationale":"Scatter plots show relationships between two numeric variables."
        },
        "stacked_bar": {
            "palette":"qualitative_distinct",
            "axis":"y_start_zero;percent_stack_optional",
            "labeling":"show_percentage_labels;limit_categories",
            "rationale":"Stacked bars show parts of whole; use percentages for clarity."
        },
        "horizontal_bar": {
            "palette":"qualitative_max12",
            "axis":"x_start_zero;sort_desc",
            "labeling":"show_value_labels;bold_top3",
            "rationale":"Horizontal bars work well for long category names and rankings."
        },
        "choropleth":{
            "palette":"sequential_for_values",
            "axis":"use_legend;bin_ranges",
            "labeling":"tooltip_values;annotate_top_countries",
            "rationale":"Choropleth reveals geographic variation clearly."
        },
        "boxplot": {
            "palette":"neutral_sequential",
            "axis":"show_outliers;equal_spacing",
            "labeling":"label_median;annotate_outliers",
            "rationale":"Box plot shows distribution summary statistics."
        }
    }
    base = constraints.get(vibe, constraints["grouped_bar"]).copy()
    # adapt using dataset_features if present
    if dataset_features:
        max_card = dataset_features.get("max_cardinality", 0)
        ratio = dataset_features.get("ratio_max_min", 1)
        if max_card > 20 and vibe in ("grouped_bar","stacked_bar"):
            base["labeling"] += ";suggest_aggregate_or_dotplot"
            base["rationale"] += " Note: many categories — consider aggregation or dot plot."
        if ratio and ratio > 1000:
            base["axis"] += ";consider_log_scale"
            base["rationale"] += " Large dynamic range suggests using log scale."
        if dataset_features.get("has_date") and vibe == "line":
            base["axis"] = "time_x;linear_y;show_year_ticks"
    return base

def sample_data_for_vibe(vibe: str):
    """Generate synthetic sample data for a given chart type."""
    if vibe == "line":
        dates = pd.date_range("2018-01-01", periods=12, freq="M")
        return pd.DataFrame({"date": dates, "value": np.round(np.linspace(100,500,12) + np.random.randn(12)*20,0)})
    if vibe == "grouped_bar":
        df = pd.DataFrame({
            "region":["North","South","East","West"]*2,
            "product":["A","A","A","A","B","B","B","B"],
            "sales":[100,90,120,80,110,95,130,85]
        })
        return df
    if vibe == "histogram":
        return pd.DataFrame({"value": (np.random.randn(1000)*15 + 50).astype(int)})
    if vibe == "scatter":
        x = np.random.rand(200)*100
        y = x*0.7 + np.random.randn(200)*10
        return pd.DataFrame({"x":x,"y":y})
    if vibe == "stacked_bar":
        df = pd.DataFrame({
            "quarter":["Q1","Q2","Q3","Q4"]*3,
            "category":["A","A","A","A","B","B","B","B","C","C","C","C"],
            "value":[100,120,110,130,90,95,105,115,80,85,90,95]
        })
        return df
    if vibe == "horizontal_bar":
        df = pd.DataFrame({
            "product":["Product Alpha","Product Beta","Product Gamma","Product Delta","Product Epsilon"],
            "sales":[450,380,520,290,410]
        })
        return df.sort_values("sales", ascending=True)
    if vibe == "choropleth":
        df = pd.DataFrame({
            "country_code":["USA","CHN","JPN","DEU","GBR","FRA","IND","BRA","CAN","AUS"],
            "value":[100,95,88,82,78,75,72,68,65,62]
        })
        return df
    # fallback
    return sample_data_for_vibe("grouped_bar")
