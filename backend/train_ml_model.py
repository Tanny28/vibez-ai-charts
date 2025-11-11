# backend/train_ml_model.py
"""
Script to train the ML-based chart recommendation model.
Run this to create an initial model or retrain with new data.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.ml_vibe_engine import MLVibeEngine

# Expanded training dataset with 300+ examples for better accuracy
TRAINING_DATA = [
    # ============================================================
    # TREND / TIME SERIES - LINE CHARTS (50 examples)
    # ============================================================
    ("show sales trends over time", "line"),
    ("monthly revenue growth", "line"),
    ("yearly increase in customers", "line"),
    ("track performance over quarters", "line"),
    ("visualize stock prices over time", "line"),
    ("show temperature changes by month", "line"),
    ("display website traffic trends", "line"),
    ("revenue trend analysis", "line"),
    ("sales over the past year", "line"),
    ("show growth rate monthly", "line"),
    ("how has revenue changed over time", "line"),
    ("plot sales trend for last 2 years", "line"),
    ("show the growth for first 2 years", "line"),
    ("track monthly active users", "line"),
    ("visualize quarterly earnings", "line"),
    ("show profit trends", "line"),
    ("display conversion rate over time", "line"),
    ("track customer acquisition over months", "line"),
    ("show revenue evolution", "line"),
    ("plot weekly sales data", "line"),
    ("visualize daily transactions", "line"),
    ("show engagement trends", "line"),
    ("track product views over time", "line"),
    ("display retention rate trends", "line"),
    ("show churn rate changes", "line"),
    ("visualize subscriber growth", "line"),
    ("plot revenue progression", "line"),
    ("show market value trends", "line"),
    ("track inventory levels over time", "line"),
    ("display price changes monthly", "line"),
    ("show bounce rate trends", "line"),
    ("visualize sales velocity", "line"),
    ("track downloads over weeks", "line"),
    ("show usage patterns over time", "line"),
    ("display cost trends", "line"),
    ("plot margin trends", "line"),
    ("show performance over quarters", "line"),
    ("visualize revenue run rate", "line"),
    ("track customer lifetime value trends", "line"),
    ("show average order value trends", "line"),
    ("display traffic growth", "line"),
    ("plot revenue per user over time", "line"),
    ("show session duration trends", "line"),
    ("visualize leads generated monthly", "line"),
    ("track inventory turnover", "line"),
    ("show operational efficiency trends", "line"),
    ("display customer satisfaction over time", "line"),
    ("plot net promoter score trends", "line"),
    ("show email open rates over time", "line"),
    ("visualize app installs weekly", "line"),
    
    # ============================================================
    # COMPARISON - GROUPED BAR CHARTS (50 examples)
    # ============================================================
    ("compare sales across regions", "grouped_bar"),
    ("revenue by product category", "grouped_bar"),
    ("compare performance between teams", "grouped_bar"),
    ("sales comparison by region", "grouped_bar"),
    ("compare Q1 vs Q2 sales", "grouped_bar"),
    ("revenue per department", "grouped_bar"),
    ("compare profit margins", "grouped_bar"),
    ("sales by store location", "grouped_bar"),
    ("revenue broken down by category", "grouped_bar"),
    ("compare customer satisfaction scores", "grouped_bar"),
    ("show sales by product line", "grouped_bar"),
    ("compare revenue across channels", "grouped_bar"),
    ("sales performance by salesperson", "grouped_bar"),
    ("compare conversion rates by source", "grouped_bar"),
    ("revenue by country", "grouped_bar"),
    ("compare costs across departments", "grouped_bar"),
    ("show profits by division", "grouped_bar"),
    ("compare orders by category", "grouped_bar"),
    ("revenue by customer segment", "grouped_bar"),
    ("compare traffic by platform", "grouped_bar"),
    ("show sales by brand", "grouped_bar"),
    ("compare engagement by channel", "grouped_bar"),
    ("revenue by subscription tier", "grouped_bar"),
    ("compare returns by product", "grouped_bar"),
    ("show downloads by app version", "grouped_bar"),
    ("compare margins by product", "grouped_bar"),
    ("revenue by market segment", "grouped_bar"),
    ("compare signups by source", "grouped_bar"),
    ("show revenue by sales team", "grouped_bar"),
    ("compare costs by supplier", "grouped_bar"),
    ("revenue by payment method", "grouped_bar"),
    ("compare performance by region", "grouped_bar"),
    ("show orders by device type", "grouped_bar"),
    ("compare revenue across quarters", "grouped_bar"),
    ("sales by customer type", "grouped_bar"),
    ("compare views by content type", "grouped_bar"),
    ("revenue by acquisition channel", "grouped_bar"),
    ("compare spending by category", "grouped_bar"),
    ("show revenue by product family", "grouped_bar"),
    ("compare sales by time period", "grouped_bar"),
    ("revenue by business unit", "grouped_bar"),
    ("compare transactions by method", "grouped_bar"),
    ("show costs by expense type", "grouped_bar"),
    ("compare revenue by sales channel", "grouped_bar"),
    ("sales by geographic area", "grouped_bar"),
    ("compare revenue products by region", "grouped_bar"),
    ("show for 2 years only", "grouped_bar"),
    ("compare monthly performance", "grouped_bar"),
    ("revenue comparison across stores", "grouped_bar"),
    ("compare customer groups", "grouped_bar"),
    
    # ============================================================
    # DISTRIBUTION - HISTOGRAMS (50 examples)
    # ============================================================
    ("distribution of customer ages", "histogram"),
    ("age distribution histogram", "histogram"),
    ("show frequency of purchase amounts", "histogram"),
    ("distribution of salaries", "histogram"),
    ("spread of test scores", "histogram"),
    ("show distribution of response times", "histogram"),
    ("frequency of order values", "histogram"),
    ("distribution of employee tenure", "histogram"),
    ("show distribution of ratings", "histogram"),
    ("histogram of transaction amounts", "histogram"),
    ("show age range of customers", "histogram"),
    ("distribution of income levels", "histogram"),
    ("frequency distribution of prices", "histogram"),
    ("show distribution of session lengths", "histogram"),
    ("histogram of purchase frequencies", "histogram"),
    ("distribution of product weights", "histogram"),
    ("show frequency of complaints", "histogram"),
    ("distribution of delivery times", "histogram"),
    ("histogram of customer spending", "histogram"),
    ("show distribution of order sizes", "histogram"),
    ("frequency of page views", "histogram"),
    ("distribution of survey responses", "histogram"),
    ("histogram of contract values", "histogram"),
    ("show distribution of discounts", "histogram"),
    ("frequency of product returns", "histogram"),
    ("distribution of loan amounts", "histogram"),
    ("histogram of customer visits", "histogram"),
    ("show distribution of wait times", "histogram"),
    ("frequency of error occurrences", "histogram"),
    ("distribution of grades", "histogram"),
    ("histogram of service requests", "histogram"),
    ("show distribution of ticket prices", "histogram"),
    ("frequency of call durations", "histogram"),
    ("distribution of inventory items", "histogram"),
    ("histogram of revenue per transaction", "histogram"),
    ("show distribution of customer lifetime", "histogram"),
    ("frequency of product usage", "histogram"),
    ("distribution of employee ages", "histogram"),
    ("histogram of conversion times", "histogram"),
    ("show distribution of credit scores", "histogram"),
    ("frequency of order cancellations", "histogram"),
    ("distribution of project timelines", "histogram"),
    ("histogram of customer segments", "histogram"),
    ("show distribution of subscription lengths", "histogram"),
    ("frequency of support tickets", "histogram"),
    ("distribution of shipping costs", "histogram"),
    ("histogram of profit margins", "histogram"),
    ("show distribution of quantities", "histogram"),
    ("frequency of website visits", "histogram"),
    ("distribution of product ratings", "histogram"),
    
    # ============================================================
    # CORRELATION / RELATIONSHIP - SCATTER PLOTS (50 examples)
    # ============================================================
    ("relationship between price and demand", "scatter"),
    ("correlation of advertising and sales", "scatter"),
    ("show how temperature affects sales", "scatter"),
    ("impact of experience on salary", "scatter"),
    ("relationship between age and income", "scatter"),
    ("correlation analysis of variables", "scatter"),
    ("show connection between study time and grades", "scatter"),
    ("relationship between investment and returns", "scatter"),
    ("how does price affect conversion", "scatter"),
    ("correlation between traffic and revenue", "scatter"),
    ("scatter plot of price vs sales", "scatter"),
    ("show relationship between spend and ROI", "scatter"),
    ("correlation of clicks and conversions", "scatter"),
    ("how does quality affect price", "scatter"),
    ("relationship between size and value", "scatter"),
    ("scatter plot of age vs spending", "scatter"),
    ("correlation between features and satisfaction", "scatter"),
    ("show how ratings affect sales", "scatter"),
    ("relationship between time and performance", "scatter"),
    ("scatter plot of cost vs benefit", "scatter"),
    ("correlation of engagement and retention", "scatter"),
    ("how does location affect revenue", "scatter"),
    ("relationship between visits and purchases", "scatter"),
    ("scatter plot of experience vs productivity", "scatter"),
    ("correlation between marketing and growth", "scatter"),
    ("show how delivery time affects ratings", "scatter"),
    ("relationship between employees and output", "scatter"),
    ("scatter plot of temperature vs energy", "scatter"),
    ("correlation of education and earnings", "scatter"),
    ("how does season affect demand", "scatter"),
    ("relationship between discounts and volume", "scatter"),
    ("scatter plot of speed vs accuracy", "scatter"),
    ("correlation between reviews and sales", "scatter"),
    ("show how inventory affects stockouts", "scatter"),
    ("relationship between leads and conversions", "scatter"),
    ("scatter plot of budget vs results", "scatter"),
    ("correlation of support quality and retention", "scatter"),
    ("how does frequency affect loyalty", "scatter"),
    ("relationship between reach and engagement", "scatter"),
    ("scatter plot of risk vs return", "scatter"),
    ("correlation between features and adoption", "scatter"),
    ("show how complexity affects completion", "scatter"),
    ("relationship between price and quality perception", "scatter"),
    ("scatter plot of investment vs growth", "scatter"),
    ("correlation of satisfaction and referrals", "scatter"),
    ("how does availability affect sales", "scatter"),
    ("relationship between training and performance", "scatter"),
    ("scatter plot of usage vs satisfaction", "scatter"),
    ("correlation between response time and ratings", "scatter"),
    ("show how personalization affects conversion", "scatter"),
    
    # ============================================================
    # COMPOSITION - STACKED BAR (50 examples)
    # ============================================================
    ("market share breakdown", "stacked_bar"),
    ("percentage composition of revenue", "stacked_bar"),
    ("proportion of sales by product line", "stacked_bar"),
    ("show composition of expenses", "stacked_bar"),
    ("breakdown of traffic sources", "stacked_bar"),
    ("show parts that make up the whole", "stacked_bar"),
    ("composition of customer segments", "stacked_bar"),
    ("percentage breakdown by category", "stacked_bar"),
    ("show share of each component", "stacked_bar"),
    ("revenue composition over time", "stacked_bar"),
    ("show revenue mix by product", "stacked_bar"),
    ("composition of total sales", "stacked_bar"),
    ("breakdown of cost structure", "stacked_bar"),
    ("show portfolio composition", "stacked_bar"),
    ("percentage of revenue by source", "stacked_bar"),
    ("composition of user base", "stacked_bar"),
    ("breakdown of market segments", "stacked_bar"),
    ("show composition of assets", "stacked_bar"),
    ("percentage of orders by type", "stacked_bar"),
    ("composition of product mix", "stacked_bar"),
    ("breakdown of revenue streams", "stacked_bar"),
    ("show share of wallet", "stacked_bar"),
    ("composition of expenses by category", "stacked_bar"),
    ("percentage of traffic by channel", "stacked_bar"),
    ("composition of inventory", "stacked_bar"),
    ("breakdown of customer types", "stacked_bar"),
    ("show composition of workforce", "stacked_bar"),
    ("percentage of sales by region", "stacked_bar"),
    ("composition of budget allocation", "stacked_bar"),
    ("breakdown of revenue by quarter", "stacked_bar"),
    ("show composition of deliverables", "stacked_bar"),
    ("percentage of costs by department", "stacked_bar"),
    ("composition of subscription tiers", "stacked_bar"),
    ("breakdown of engagement metrics", "stacked_bar"),
    ("show composition of leads", "stacked_bar"),
    ("percentage of revenue by vertical", "stacked_bar"),
    ("composition of support tickets", "stacked_bar"),
    ("breakdown of conversion funnel", "stacked_bar"),
    ("show composition of features used", "stacked_bar"),
    ("percentage of sales by product family", "stacked_bar"),
    ("composition of customer journey", "stacked_bar"),
    ("breakdown of marketing spend", "stacked_bar"),
    ("show composition of technology stack", "stacked_bar"),
    ("percentage of users by plan", "stacked_bar"),
    ("composition of revenue by contract type", "stacked_bar"),
    ("breakdown of operational costs", "stacked_bar"),
    ("show composition of content types", "stacked_bar"),
    ("percentage of orders by fulfillment method", "stacked_bar"),
    ("composition of sales pipeline", "stacked_bar"),
    ("breakdown of resource allocation", "stacked_bar"),
    
    # ============================================================
    # RANKING - HORIZONTAL BAR (50 examples)
    # ============================================================
    ("top 10 selling products", "horizontal_bar"),
    ("ranking of sales teams", "horizontal_bar"),
    ("best performing regions", "horizontal_bar"),
    ("rank customers by spending", "horizontal_bar"),
    ("top performers this month", "horizontal_bar"),
    ("highest revenue products", "horizontal_bar"),
    ("rank stores by sales", "horizontal_bar"),
    ("top 5 most expensive items", "horizontal_bar"),
    ("leaders in market share", "horizontal_bar"),
    ("rank employees by performance", "horizontal_bar"),
    ("top revenue generators", "horizontal_bar"),
    ("best selling categories", "horizontal_bar"),
    ("rank cities by population", "horizontal_bar"),
    ("top rated products", "horizontal_bar"),
    ("highest profit products", "horizontal_bar"),
    ("rank departments by revenue", "horizontal_bar"),
    ("top traffic sources", "horizontal_bar"),
    ("best converting campaigns", "horizontal_bar"),
    ("rank suppliers by volume", "horizontal_bar"),
    ("top customer segments", "horizontal_bar"),
    ("highest engagement posts", "horizontal_bar"),
    ("rank brands by sales", "horizontal_bar"),
    ("top performing stocks", "horizontal_bar"),
    ("best retention cohorts", "horizontal_bar"),
    ("rank products by margin", "horizontal_bar"),
    ("top revenue accounts", "horizontal_bar"),
    ("highest satisfaction scores", "horizontal_bar"),
    ("rank channels by conversions", "horizontal_bar"),
    ("top downloaded apps", "horizontal_bar"),
    ("best performing ads", "horizontal_bar"),
    ("rank keywords by traffic", "horizontal_bar"),
    ("top selling authors", "horizontal_bar"),
    ("highest value customers", "horizontal_bar"),
    ("rank features by usage", "horizontal_bar"),
    ("top referral sources", "horizontal_bar"),
    ("best performing regions by growth", "horizontal_bar"),
    ("rank products by reviews", "horizontal_bar"),
    ("top revenue generating services", "horizontal_bar"),
    ("highest volume SKUs", "horizontal_bar"),
    ("rank salespeople by quota", "horizontal_bar"),
    ("top searched terms", "horizontal_bar"),
    ("best performing time slots", "horizontal_bar"),
    ("rank countries by GDP", "horizontal_bar"),
    ("top customer pain points", "horizontal_bar"),
    ("highest churn segments", "horizontal_bar"),
    ("rank content by engagement", "horizontal_bar"),
    ("top revenue streams", "horizontal_bar"),
    ("best performing product lines", "horizontal_bar"),
    ("rank markets by potential", "horizontal_bar"),
    ("top expense categories", "horizontal_bar"),
    
    # ============================================================
    # GEOGRAPHIC / MAP - CHOROPLETH (50 examples)
    # ============================================================
    ("sales by country map", "choropleth"),
    ("geographic distribution of revenue", "choropleth"),
    ("revenue across states", "choropleth"),
    ("show sales on a map", "choropleth"),
    ("regional performance map", "choropleth"),
    ("visualize data by location", "choropleth"),
    ("map of customer distribution", "choropleth"),
    ("geographic heat map", "choropleth"),
    ("show revenue by region on map", "choropleth"),
    ("country-wise sales visualization", "choropleth"),
    ("map sales across continents", "choropleth"),
    ("geographic revenue breakdown", "choropleth"),
    ("show customer density by state", "choropleth"),
    ("visualize expansion by country", "choropleth"),
    ("map of market penetration", "choropleth"),
    ("geographic performance visualization", "choropleth"),
    ("show orders by country", "choropleth"),
    ("map of user activity", "choropleth"),
    ("geographic sales distribution", "choropleth"),
    ("visualize growth by region", "choropleth"),
    ("map revenue by territory", "choropleth"),
    ("show traffic sources by country", "choropleth"),
    ("geographic analysis of customers", "choropleth"),
    ("map conversion rates by state", "choropleth"),
    ("show shipping destinations", "choropleth"),
    ("geographic market share", "choropleth"),
    ("map of store locations performance", "choropleth"),
    ("visualize regional trends", "choropleth"),
    ("show demographics by geography", "choropleth"),
    ("map of sales territories", "choropleth"),
    ("geographic distribution of users", "choropleth"),
    ("show market coverage by region", "choropleth"),
    ("map revenue density", "choropleth"),
    ("visualize regional demand", "choropleth"),
    ("geographic customer segments", "choropleth"),
    ("show adoption rates by country", "choropleth"),
    ("map of fulfillment centers utilization", "choropleth"),
    ("geographic pricing variations", "choropleth"),
    ("show competition by region", "choropleth"),
    ("map of seasonal trends by location", "choropleth"),
    ("visualize global presence", "choropleth"),
    ("geographic ROI analysis", "choropleth"),
    ("show market size by country", "choropleth"),
    ("map customer acquisition costs", "choropleth"),
    ("geographic product preferences", "choropleth"),
    ("visualize regional partnerships", "choropleth"),
    ("show supply chain by location", "choropleth"),
    ("map of service coverage", "choropleth"),
    ("geographic brand awareness", "choropleth"),
    ("visualize expansion opportunities", "choropleth"),
]

def main():
    """Train the ML model with sample data."""
    print("=" * 60)
    print("Training ML-Based Chart Recommendation Model")
    print("=" * 60)
    print()
    
    # Create engine
    engine = MLVibeEngine(model_path="backend/models/vibe_classifier.pkl")
    
    print(f"Training with {len(TRAINING_DATA)} examples...")
    print()
    
    # Train
    results = engine.train(TRAINING_DATA)
    
    print()
    print("=" * 60)
    print("Training Results:")
    print(f"  Training Accuracy: {results['train_accuracy']:.2%}")
    print(f"  Validation Accuracy: {results['validation_accuracy']:.2%}")
    print(f"  Total Examples: {results['num_examples']}")
    print("=" * 60)
    print()
    
    # Test a few predictions
    test_prompts = [
        "show me sales trends",
        "compare revenue across products",
        "distribution of ages",
        "relationship between price and sales",
        "top 10 customers",
    ]
    
    print("Testing predictions:")
    print("-" * 60)
    for prompt in test_prompts:
        prediction = engine.predict(prompt, get_probabilities=True)
        print(f"Prompt: '{prompt}'")
        print(f"  → Predicted: {prediction['chart_type']} "
              f"(confidence: {prediction['confidence']:.1%})")
        print()
    
    print("=" * 60)
    print("✅ Model training complete!")
    print(f"Model saved to: backend/models/vibe_classifier.pkl")
    print()
    print("To use this model in your API, update main.py to use ml_vibe_engine")
    print("=" * 60)

if __name__ == "__main__":
    main()
