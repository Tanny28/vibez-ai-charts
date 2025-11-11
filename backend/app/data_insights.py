# backend/app/data_insights.py
"""
Automatic data analysis and business insights generation.
Inspired by the enhanced Streamlit app's intelligence features.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


class DataInsightsEngine:
    """Generate business insights and recommendations from data automatically."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.insights = []
        self.recommendations = []
        
    def analyze(self) -> Dict[str, Any]:
        """Run complete analysis and return all insights."""
        return {
            'insights': self.generate_insights(),
            'recommendations': self.generate_recommendations(),
            'auto_charts': self.suggest_auto_charts(),
            'statistics': self.calculate_statistics()
        }
    
    def generate_insights(self) -> List[Dict[str, Any]]:
        """Generate 5 key business insights automatically."""
        insights = []
        
        # 1. Revenue Performance
        revenue_insight = self._analyze_revenue()
        if revenue_insight:
            insights.append(revenue_insight)
        
        # 2. Top Performing Categories
        category_insight = self._analyze_categories()
        if category_insight:
            insights.append(category_insight)
        
        # 3. Return/Quality Analysis
        quality_insight = self._analyze_quality()
        if quality_insight:
            insights.append(quality_insight)
        
        # 4. Geographic Performance
        geo_insight = self._analyze_geography()
        if geo_insight:
            insights.append(geo_insight)
        
        # 5. Customer Engagement
        customer_insight = self._analyze_customers()
        if customer_insight:
            insights.append(customer_insight)
        
        return insights
    
    def _detect_column(self, keywords: List[str]) -> Optional[str]:
        """Find column matching any of the keywords (case-insensitive)."""
        columns_lower = {col.lower(): col for col in self.df.columns}
        for keyword in keywords:
            for col_lower, col_original in columns_lower.items():
                if keyword.lower() in col_lower:
                    return col_original
        return None
    
    def _analyze_revenue(self) -> Optional[Dict[str, Any]]:
        """Analyze revenue performance."""
        revenue_col = self._detect_column(['revenue', 'sales', 'amount', 'price', 'total'])
        
        if revenue_col and pd.api.types.is_numeric_dtype(self.df[revenue_col]):
            total_revenue = self.df[revenue_col].sum()
            avg_revenue = self.df[revenue_col].mean()
            
            return {
                'category': 'revenue',
                'icon': '💰',
                'title': 'Revenue Performance',
                'metrics': {
                    'total_revenue': f"${float(total_revenue):,.2f}",
                    'avg_transaction': f"${float(avg_revenue):,.2f}",
                    'num_transactions': int(len(self.df))
                },
                'summary': f"Total revenue: ${float(total_revenue):,.2f} | Avg per transaction: ${float(avg_revenue):,.2f}",
                'recommendation': "Focus on increasing average transaction value through upselling and cross-selling strategies."
            }
        return None
    
    def _analyze_categories(self) -> Optional[Dict[str, Any]]:
        """Analyze top performing categories/products."""
        category_col = self._detect_column(['category', 'product', 'type', 'segment'])
        revenue_col = self._detect_column(['revenue', 'sales', 'amount', 'price'])
        
        if category_col and revenue_col:
            # Group by category and sum revenue
            cat_revenue = self.df.groupby(category_col)[revenue_col].sum().sort_values(ascending=False)
            top_3 = cat_revenue.head(3)
            
            return {
                'category': 'categories',
                'icon': '📊',
                'title': 'Top Performing Categories',
                'metrics': {
                    'top_category': str(top_3.index[0]) if len(top_3) > 0 else 'N/A',
                    'top_revenue': f"${top_3.iloc[0]:,.2f}" if len(top_3) > 0 else '$0',
                    'num_categories': int(cat_revenue.count())
                },
                'summary': f"Best: {top_3.index[0]} (${top_3.iloc[0]:,.2f})" if len(top_3) > 0 else "No data",
                'recommendation': f"Increase inventory and marketing budget for top category: {top_3.index[0]}"
            }
        return None
    
    def _analyze_quality(self) -> Optional[Dict[str, Any]]:
        """Analyze returns or quality issues."""
        status_col = self._detect_column(['status', 'state', 'order_status'])
        
        if status_col:
            status_counts = self.df[status_col].value_counts()
            total = len(self.df)
            
            # Look for return/cancelled indicators
            return_keywords = ['return', 'cancel', 'refund', 'failed']
            returns = 0
            for keyword in return_keywords:
                matching = status_counts[status_counts.index.str.contains(keyword, case=False, na=False)]
                returns += matching.sum()
            
            return_rate = (returns / total * 100) if total > 0 else 0
            
            return {
                'category': 'quality',
                'icon': '🔄',
                'title': 'Order Quality Analysis',
                'metrics': {
                    'return_rate': f"{return_rate:.1f}%",
                    'total_returns': int(returns),
                    'successful_orders': int(total - returns)
                },
                'summary': f"Return rate: {return_rate:.1f}% ({int(returns):,} returns)",
                'recommendation': "Improve product descriptions and quality control to reduce return rate." if return_rate > 10 else "Maintain current quality standards."
            }
        return None
    
    def _analyze_geography(self) -> Optional[Dict[str, Any]]:
        """Analyze geographic performance."""
        geo_col = self._detect_column(['location', 'city', 'region', 'zone', 'state', 'country'])
        revenue_col = self._detect_column(['revenue', 'sales', 'amount', 'price'])
        
        if geo_col and revenue_col:
            geo_revenue = self.df.groupby(geo_col)[revenue_col].sum().sort_values(ascending=False)
            top_region = geo_revenue.head(1)
            
            return {
                'category': 'geography',
                'icon': '🗺',
                'title': 'Geographic Insights',
                'metrics': {
                    'top_market': str(top_region.index[0]),
                    'top_revenue': f"${float(top_region.iloc[0]):,.2f}",
                    'num_regions': int(geo_revenue.count())
                },
                'summary': f"Top market: {top_region.index[0]} (${float(top_region.iloc[0]):,.2f})",
                'recommendation': f"Replicate successful strategies from {top_region.index[0]} to underperforming regions."
            }
        return None
    
    def _analyze_customers(self) -> Optional[Dict[str, Any]]:
        """Analyze customer engagement."""
        customer_col = self._detect_column(['customer', 'customer_id', 'user_id', 'client'])
        
        if customer_col:
            unique_customers = self.df[customer_col].nunique()
            total_orders = len(self.df)
            avg_orders = total_orders / unique_customers if unique_customers > 0 else 0
            
            return {
                'category': 'customers',
                'icon': '👥',
                'title': 'Customer Engagement',
                'metrics': {
                    'unique_customers': f"{int(unique_customers):,}",
                    'avg_orders_per_customer': f"{float(avg_orders):.1f}",
                    'total_orders': f"{int(total_orders):,}"
                },
                'summary': f"{int(unique_customers):,} unique customers | {float(avg_orders):.1f} orders per customer",
                'recommendation': "Implement loyalty programs and email campaigns to increase repeat purchase rate." if avg_orders < 2 else "Strong customer loyalty. Focus on acquisition."
            }
        return None
    
    def generate_recommendations(self) -> List[str]:
        """Generate actionable business recommendations."""
        recs = []
        
        # Extract recommendations from insights
        insights = self.generate_insights()
        for insight in insights:
            if insight.get('recommendation'):
                recs.append(insight['recommendation'])
        
        return recs
    
    def suggest_auto_charts(self) -> List[Dict[str, str]]:
        """Suggest 5 automatic visualizations based on data."""
        suggestions = []
        
        # 1. Revenue by Category
        category_col = self._detect_column(['category', 'product', 'type'])
        revenue_col = self._detect_column(['revenue', 'sales', 'amount'])
        if category_col and revenue_col:
            suggestions.append({
                'title': 'Revenue by Category',
                'type': 'horizontal_bar',
                'prompt': f'top 10 {category_col} by {revenue_col}'
            })
        
        # 2. Revenue Trend Over Time
        date_col = self._detect_column(['date', 'time', 'created', 'order_date'])
        if date_col and revenue_col:
            suggestions.append({
                'title': 'Revenue Trend Over Time',
                'type': 'line',
                'prompt': f'{revenue_col} trends over {date_col}'
            })
        
        # 3. Status Distribution
        status_col = self._detect_column(['status', 'state'])
        if status_col:
            suggestions.append({
                'title': 'Order Status Distribution',
                'type': 'stacked_bar',
                'prompt': f'distribution of {status_col}'
            })
        
        # 4. Geographic Performance
        geo_col = self._detect_column(['location', 'city', 'region'])
        if geo_col and revenue_col:
            suggestions.append({
                'title': 'Geographic Performance',
                'type': 'choropleth',
                'prompt': f'{revenue_col} by {geo_col}'
            })
        
        # 5. Price Analysis
        price_cols = [col for col in self.df.columns if 'price' in col.lower()]
        if len(price_cols) >= 2:
            suggestions.append({
                'title': 'Price Analysis',
                'type': 'scatter',
                'prompt': f'relationship between {price_cols[0]} and {price_cols[1]}'
            })
        
        return suggestions[:5]  # Return max 5
    
    def calculate_statistics(self) -> Dict[str, Any]:
        """Calculate enhanced statistics for the dataset."""
        stats = {
            'shape': {
                'rows': int(len(self.df)),
                'columns': int(len(self.df.columns))
            },
            'columns': {
                'numeric': int(len(self.df.select_dtypes(include=[np.number]).columns)),
                'categorical': int(len(self.df.select_dtypes(include=['object', 'category']).columns)),
                'datetime': int(len(self.df.select_dtypes(include=['datetime']).columns))
            },
            'missing': {
                'total_missing': int(self.df.isnull().sum().sum()),
                'missing_percentage': float(self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns)) * 100)
            }
        }
        
        # Add column-level statistics for numeric columns
        numeric_stats = {}
        for col in self.df.select_dtypes(include=[np.number]).columns:
            numeric_stats[col] = {
                'mean': float(self.df[col].mean()),
                'median': float(self.df[col].median()),
                'std': float(self.df[col].std()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max())
            }
        
        stats['numeric_stats'] = numeric_stats
        
        return stats
