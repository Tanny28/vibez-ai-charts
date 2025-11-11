# backend/app/chart_generator.py
# Helper to generate Plotly chart specs from data
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, Optional
import json

def generate_plotly_spec(vibe: str, df: pd.DataFrame, x_col: str = None, y_col: str = None, group_col: str = None) -> Dict[str, Any]:
    """Generate a Plotly chart specification based on vibe and data."""
    
    if vibe == "line":
        if x_col and y_col:
            fig = px.line(df, x=x_col, y=y_col, markers=True)
        else:
            # Auto-detect columns
            date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c]) or 'date' in c.lower()]
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if date_cols and numeric_cols:
                fig = px.line(df, x=date_cols[0], y=numeric_cols[0], markers=True)
            elif len(df.columns) >= 2:
                fig = px.line(df, x=df.columns[0], y=df.columns[1], markers=True)
            else:
                return {"error": "Insufficient columns for line chart"}
        
    elif vibe == "grouped_bar":
        if x_col and y_col:
            if group_col:
                fig = px.bar(df, x=x_col, y=y_col, color=group_col, barmode='group')
            else:
                fig = px.bar(df, x=x_col, y=y_col)
        else:
            # Auto-detect
            cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            if cat_cols and num_cols:
                if len(cat_cols) > 1:
                    fig = px.bar(df, x=cat_cols[0], y=num_cols[0], color=cat_cols[1], barmode='group')
                else:
                    fig = px.bar(df, x=cat_cols[0], y=num_cols[0])
            else:
                return {"error": "Need categorical and numeric columns"}
    
    elif vibe == "histogram":
        if y_col:
            fig = px.histogram(df, x=y_col, nbins=30)
        else:
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            if num_cols:
                fig = px.histogram(df, x=num_cols[0], nbins=30)
            else:
                return {"error": "Need numeric column for histogram"}
    
    elif vibe == "scatter":
        if x_col and y_col:
            fig = px.scatter(df, x=x_col, y=y_col)
        else:
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            if len(num_cols) >= 2:
                fig = px.scatter(df, x=num_cols[0], y=num_cols[1])
            else:
                return {"error": "Need at least 2 numeric columns"}
    
    elif vibe == "horizontal_bar":
        if x_col and y_col:
            fig = px.bar(df, y=x_col, x=y_col, orientation='h')
        else:
            cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            if cat_cols and num_cols:
                df_sorted = df.sort_values(num_cols[0], ascending=True)
                fig = px.bar(df_sorted, y=cat_cols[0], x=num_cols[0], orientation='h')
            else:
                return {"error": "Need categorical and numeric columns"}
    
    elif vibe == "stacked_bar":
        if x_col and y_col and group_col:
            fig = px.bar(df, x=x_col, y=y_col, color=group_col, barmode='stack')
        else:
            cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            num_cols = df.select_dtypes(include=['number']).columns.tolist()
            if len(cat_cols) >= 2 and num_cols:
                fig = px.bar(df, x=cat_cols[0], y=num_cols[0], color=cat_cols[1], barmode='stack')
            else:
                return {"error": "Need 2 categorical and 1 numeric column"}
    
    elif vibe == "choropleth":
        # Return placeholder for map data
        return {
            "library": "mapbox",
            "data": df.to_dict('records') if 'country_code' in df.columns or 'country' in df.columns else [],
            "message": "Choropleth data ready for map rendering"
        }
    
    else:
        return {"error": f"Unknown vibe: {vibe}"}
    
    # Update layout for better appearance
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=40, b=40),
        height=400
    )
    
    # Convert to JSON-serializable dict using plotly's to_dict method
    fig_json = json.loads(fig.to_json())
    return {
        "library": "plotly",
        "data": fig_json.get('data', []),
        "layout": fig_json.get('layout', {})
    }
