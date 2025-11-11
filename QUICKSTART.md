# Quick Start Guide - Vibe-Code

## 🚀 Getting Started (5 minutes)

### 1. Install Dependencies
```powershell
cd d:\vibez_codepcu
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the App
```powershell
streamlit run app.py
```

The app will open at **http://localhost:8501**

### 3. Try These Examples

#### Example 1: Trend Analysis
1. **Prompt:** "Show quarterly revenue growth over 3 years"
2. **Upload:** `example_data/trend.csv`
3. **Expected:** Line chart with time on X-axis

#### Example 2: Sales Comparison
1. **Prompt:** "Compare sales across regions by product"
2. **Upload:** `example_data/sales_by_region.csv`
3. **Expected:** Grouped bar chart

#### Example 3: Age Distribution
1. **Prompt:** "How are customer ages distributed"
2. **Upload:** `example_data/ages_distribution.csv`
3. **Expected:** Histogram

#### Example 4: Correlation Analysis
1. **Prompt:** "What's the relationship between ad spend and sales"
2. **Upload:** `example_data/ads_sales.csv`
3. **Expected:** Scatter plot

#### Example 5: Geographic Data
1. **Prompt:** "Show GDP by country on a map"
2. **Upload:** `example_data/countries_gdp.csv`
3. **Expected:** Choropleth recommendation

## 🧪 Run Tests
```powershell
pytest tests/test_vibe_engine.py -v
```

## 📊 Supported Chart Types
- **line** - Trends over time
- **grouped_bar** - Category comparisons
- **histogram** - Distributions
- **scatter** - Correlations
- **stacked_bar** - Composition
- **horizontal_bar** - Rankings
- **choropleth** - Geographic

## 💡 Tips
- Be specific in your prompts (use keywords like "trend", "compare", "distribution")
- Upload CSV with clear column names
- Use the Insight Type dropdown if auto-detection fails
- Download Vega-Lite JSON for further customization

## 🐛 Troubleshooting
- **Chart not rendering?** Check that your CSV has appropriate column types
- **Wrong chart type?** Try adding more specific keywords to your prompt
- **Tests failing?** Make sure all dependencies are installed
- **Large dataset error?** The app now automatically samples datasets with >5,000 rows for visualization (full data still analyzed)

## 📚 Next Steps
- Explore `mapping_table.csv` to see all keyword mappings
- Check `prompts.csv` for 100+ example prompts
- Read `README.md` for complete documentation
