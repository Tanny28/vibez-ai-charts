# backend/app/data_utils.py
# Ported from root data_utils.py
import pandas as pd
import numpy as np

def infer_schema_from_df(df: pd.DataFrame) -> dict:
    """Extract dataset features from a DataFrame for adaptive constraint generation."""
    num_rows = len(df)
    num_numeric = sum(pd.api.types.is_numeric_dtype(dt) for dt in df.dtypes)
    num_categorical = sum(pd.api.types.is_object_dtype(dt) or pd.api.types.is_categorical_dtype(dt) for dt in df.dtypes)
    has_date = False
    date_col = None
    time_gran = None
    for col in df.columns:
        try:
            ser = pd.to_datetime(df[col], errors="coerce")
            pct_non_null = ser.notnull().sum() / len(ser)
            if pct_non_null > 0.6:
                has_date = True
                date_col = col
                # estimate granularity
                rng = ser.dropna()
                if len(rng) > 1:
                    if (rng.dt.day == 1).all():
                        time_gran = "monthly"
                    else:
                        time_gran = "daily"
                break
        except Exception:
            continue
    max_cardinality = max((df[col].nunique(dropna=True) for col in df.columns), default=0)
    median_missing_pct = df.isnull().mean().median()
    numeric_cols = df.select_dtypes(include=[np.number])
    ratio = 1.0
    if not numeric_cols.empty:
        min_v = numeric_cols.min().min()
        max_v = numeric_cols.max().max()
        if min_v is None or pd.isna(min_v) or max_v is None or pd.isna(max_v):
            ratio = 1.0
        elif min_v == 0:
            ratio = float("inf") if max_v != 0 else 1.0
        else:
            ratio = abs(max_v / (min_v if min_v != 0 else 1))
    lat_lon_present = any(c.lower() in ("lat","latitude","lon","longitude") for c in df.columns)
    country_code_present = any(c.lower() in ("country","country_code","iso3") for c in df.columns)

    return {
        "num_rows": num_rows,
        "num_numeric": int(num_numeric),
        "num_categorical": int(num_categorical),
        "has_date": bool(has_date),
        "date_col": date_col,
        "time_granularity": time_gran,
        "max_cardinality": int(max_cardinality),
        "median_missing_pct": float(median_missing_pct),
        "ratio_max_min": float(ratio if np.isfinite(ratio) else 1.0),
        "lat_lon_present": lat_lon_present,
        "country_code_present": country_code_present
    }

def load_csv(path: str, nrows: int = None):
    """Safely load a CSV file."""
    try:
        df = pd.read_csv(path, nrows=nrows)
        return df
    except Exception as e:
        raise ValueError(f"Failed to load CSV: {str(e)}")
