# backend/app/data_qa.py# backend/app/data_qa.py

""""""

AI-powered Q&A system for data using Google Gemini.AI-powered Q&A system for data analysis.

Answers user questions about their uploaded data.Answers natural language questions about uploaded data using OpenAI GPT-4.

""""""

import pandas as pdimport os

from typing import Dict, Any, Optionalimport pandas as pd

from app.ai_storyteller import get_storytellerimport numpy as np

from typing import Dict, List, Any, Optional

from openai import OpenAI

class DataQA:from dotenv import load_dotenv

    """AI-powered question answering for datasets."""import json

    

    def __init__(self, df: pd.DataFrame):load_dotenv()

        """Initialize with a DataFrame."""

        self.df = dfclass DataQA:

        self.storyteller = get_storyteller()    """Answer questions about data using AI and actual data analysis."""

        

    def ask(self, question: str) -> Dict[str, Any]:    def __init__(self, df: pd.DataFrame):

        """        """Initialize with dataframe to analyze."""

        Answer a question about the data.        self.df = df

                

        Args:        api_key = os.getenv('OPENAI_API_KEY')

            question: User's question        if not api_key:

                    raise ValueError("OPENAI_API_KEY not found in environment")

        Returns:        

            Dictionary with answer and related information        self.client = OpenAI(api_key=api_key)

        """        self.model = "gpt-4o-mini"

        if not self.storyteller:        

            return {        # Analyze data structure once

                'answer': 'AI service is currently unavailable. Please try again later.',        self.data_summary = self._analyze_data_structure()

                'success': False    

            }    def answer_question(self, question: str) -> Dict[str, Any]:

                """

        try:        Answer a natural language question about the data.

            # Prepare data information        

            df_info = self._get_df_info()        Args:

            sample_data = self._get_sample_data()            question: User's question (e.g., "What are the top 5 products by sales?")

                    

            # Get AI answer        Returns:

            answer = self.storyteller.answer_question(            {

                question=question,                'answer': str,  # Natural language answer

                df_info=df_info,                'data': dict,   # Relevant data points

                sample_data=sample_data                'visualization_suggestion': str,  # Suggested chart

            )                'sql_equivalent': str  # What this query would look like in SQL

                        }

            return {        """

                'answer': answer,        try:

                'success': True,            # Step 1: Analyze what data we need

                'data_summary': {            analysis_plan = self._create_analysis_plan(question)

                    'total_rows': len(self.df),            

                    'total_columns': len(self.df.columns),            # Step 2: Execute the analysis on actual data

                    'columns': list(self.df.columns)            analyzed_data = self._execute_analysis(analysis_plan)

                }            

            }            # Step 3: Generate natural language answer with GPT-4

                        answer = self._generate_answer(question, analyzed_data)

        except Exception as e:            

            return {            # Step 4: Suggest visualization

                'answer': f'Error processing your question: {str(e)}',            viz_suggestion = self._suggest_visualization(question, analyzed_data)

                'success': False            

            }            return {

                    'question': question,

    def _get_df_info(self) -> Dict[str, Any]:                'answer': answer,

        """Get DataFrame information for AI context."""                'data': analyzed_data,

        try:                'visualization_suggestion': viz_suggestion,

            # Get column info                'confidence': 'high' if analyzed_data else 'low'

            columns = list(self.df.columns)            }

            dtypes = {col: str(dtype) for col, dtype in self.df.dtypes.items()}            

                    except Exception as e:

            # Get summary statistics for numeric columns            print(f"Error answering question: {e}")

            numeric_cols = self.df.select_dtypes(include=['number']).columns            return {

            statistics = {}                'question': question,

                            'answer': f"I encountered an error analyzing this data: {str(e)}",

            for col in numeric_cols:                'data': {},

                statistics[col] = {                'visualization_suggestion': None,

                    'mean': float(self.df[col].mean()),                'confidence': 'low'

                    'median': float(self.df[col].median()),            }

                    'min': float(self.df[col].min()),    

                    'max': float(self.df[col].max()),    def _analyze_data_structure(self) -> Dict[str, Any]:

                    'std': float(self.df[col].std())        """Analyze the dataframe structure for context."""

                }        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()

                    categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()

            return {        datetime_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()

                'columns': columns,        

                'dtypes': dtypes,        # Get sample statistics

                'total_rows': len(self.df),        stats = {}

                'total_columns': len(self.df.columns),        for col in numeric_cols[:10]:  # Limit to first 10 numeric columns

                'statistics': statistics            stats[col] = {

            }                'min': float(self.df[col].min()),

        except Exception as e:                'max': float(self.df[col].max()),

            print(f"Error getting df info: {e}")                'mean': float(self.df[col].mean()),

            return {                'sum': float(self.df[col].sum())

                'columns': list(self.df.columns),            }

                'total_rows': len(self.df),        

                'total_columns': len(self.df.columns)        return {

            }            'rows': len(self.df),

                'columns': len(self.df.columns),

    def _get_sample_data(self) -> str:            'column_names': list(self.df.columns),

        """Get sample data as string for AI context."""            'numeric_columns': numeric_cols,

        try:            'categorical_columns': categorical_cols,

            # Get first 5 rows            'datetime_columns': datetime_cols,

            sample = self.df.head(5)            'statistics': stats,

            return sample.to_string()            'sample_data': self.df.head(3).to_dict('records')

        except Exception as e:        }

            print(f"Error getting sample data: {e}")    

            return "Sample data unavailable"    def _create_analysis_plan(self, question: str) -> Dict[str, Any]:

        """Use GPT-4 to create an analysis plan."""

        prompt = f"""

def create_qa_engine(df: pd.DataFrame) -> DataQA:Given this data structure:

    """Create a Q&A engine for a DataFrame."""- Rows: {self.data_summary['rows']}

    return DataQA(df)- Columns: {', '.join(self.data_summary['column_names'])}

- Numeric columns: {', '.join(self.data_summary['numeric_columns'])}
- Categorical columns: {', '.join(self.data_summary['categorical_columns'])}

User question: "{question}"

Create a JSON analysis plan with:
1. "operation": One of [top_n, bottom_n, aggregate, filter, trend, correlation, comparison]
2. "column": The primary column to analyze
3. "groupby": Column to group by (if applicable)
4. "limit": Number of results (if applicable)
5. "sort_by": Column to sort by
6. "ascending": true/false

Only respond with valid JSON, no explanation.
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a data analysis expert. Create precise analysis plans in JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        plan_text = response.choices[0].message.content.strip()
        # Extract JSON if wrapped in markdown
        if '```json' in plan_text:
            plan_text = plan_text.split('```json')[1].split('```')[0].strip()
        elif '```' in plan_text:
            plan_text = plan_text.split('```')[1].split('```')[0].strip()
        
        return json.loads(plan_text)
    
    def _execute_analysis(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the analysis plan on the actual dataframe."""
        operation = plan.get('operation', '')
        column = plan.get('column', '')
        groupby = plan.get('groupby', '')
        limit = plan.get('limit', 10)
        sort_by = plan.get('sort_by', column)
        ascending = plan.get('ascending', False)
        
        result = {}
        
        try:
            if operation == 'top_n' and column in self.df.columns:
                # Top N values
                if groupby and groupby in self.df.columns:
                    # Group and aggregate
                    df_grouped = self.df.groupby(groupby)[column].sum().sort_values(ascending=ascending).head(limit)
                    result['values'] = [
                        {'label': str(k), 'value': float(v)} 
                        for k, v in df_grouped.items()
                    ]
                else:
                    # Just sort
                    df_sorted = self.df.nlargest(limit, column) if not ascending else self.df.nsmallest(limit, column)
                    result['values'] = df_sorted[[column]].to_dict('records')
            
            elif operation == 'aggregate' and column in self.df.columns:
                # Aggregate statistics
                if groupby and groupby in self.df.columns:
                    df_grouped = self.df.groupby(groupby)[column].agg(['sum', 'mean', 'count'])
                    result['aggregates'] = df_grouped.to_dict()
                else:
                    result['total'] = float(self.df[column].sum())
                    result['average'] = float(self.df[column].mean())
                    result['count'] = int(self.df[column].count())
            
            elif operation == 'comparison' and groupby and column:
                # Compare groups
                df_grouped = self.df.groupby(groupby)[column].sum().sort_values(ascending=False).head(limit)
                result['comparison'] = [
                    {'category': str(k), 'value': float(v)}
                    for k, v in df_grouped.items()
                ]
            
            elif operation == 'trend' and column in self.df.columns:
                # Time-based trend
                datetime_col = self.data_summary['datetime_columns'][0] if self.data_summary['datetime_columns'] else None
                if datetime_col:
                    df_trend = self.df.sort_values(datetime_col)[[datetime_col, column]].head(100)
                    result['trend'] = df_trend.to_dict('records')
                else:
                    result['trend'] = self.df[column].head(50).tolist()
            
            # Add summary stats
            if column in self.df.columns and column in self.data_summary['numeric_columns']:
                result['stats'] = self.data_summary['statistics'].get(column, {})
        
        except Exception as e:
            print(f"Analysis execution error: {e}")
            result['error'] = str(e)
        
        return result
    
    def _generate_answer(self, question: str, analyzed_data: Dict[str, Any]) -> str:
        """Generate natural language answer using GPT-4."""
        prompt = f"""
User asked: "{question}"

Analysis results:
{json.dumps(analyzed_data, indent=2)}

Data context:
- Dataset has {self.data_summary['rows']} rows
- Available columns: {', '.join(self.data_summary['column_names'])}

Provide a clear, concise answer (2-3 sentences) that:
1. Directly answers the question
2. Includes specific numbers from the analysis
3. Provides actionable insights

Be conversational and helpful.
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful data analyst. Answer questions clearly with specific numbers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
    
    def _suggest_visualization(self, question: str, analyzed_data: Dict[str, Any]) -> Optional[str]:
        """Suggest an appropriate visualization for the answer."""
        question_lower = question.lower()
        
        # Pattern-based suggestions
        if any(word in question_lower for word in ['trend', 'over time', 'timeline', 'change']):
            return "line"
        elif any(word in question_lower for word in ['compare', 'vs', 'versus', 'top', 'bottom']):
            return "bar"
        elif any(word in question_lower for word in ['distribution', 'breakdown', 'percentage', 'share']):
            return "pie"
        elif any(word in question_lower for word in ['relationship', 'correlation', 'scatter']):
            return "scatter"
        else:
            # Default based on data structure
            if 'comparison' in analyzed_data:
                return "bar"
            elif 'trend' in analyzed_data:
                return "line"
            else:
                return "bar"


# Singleton pattern
_qa_instances = {}

def get_data_qa(df: pd.DataFrame, file_id: str) -> DataQA:
    """Get or create DataQA instance for a file."""
    if file_id not in _qa_instances:
        _qa_instances[file_id] = DataQA(df)
    return _qa_instances[file_id]
