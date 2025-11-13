import pandas as pd
from typing import Dict, Any, List
from app.ai_storyteller import get_storyteller

class DataQA:
    def __init__(self, df: pd.DataFrame, file_id: str):
        self.df = df
        self.file_id = file_id
        self.storyteller = get_storyteller()
    
    def ask(self, question: str, insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            data_context = self._get_df_info()
            answer = self.storyteller.answer_question(question, data_context, insights)
            
            return {
                'answer': answer,
                'success': True,
                'context': {
                    'file_id': self.file_id,
                    'rows': len(self.df),
                    'columns': list(self.df.columns)
                }
            }
        except Exception as e:
            return {
                'answer': f"Error: {str(e)}",
                'success': False
            }
    
    def _get_df_info(self) -> str:
        return f"Dataset with {len(self.df)} rows and {len(self.df.columns)} columns. Columns: {', '.join(self.df.columns)}"

def create_qa_engine(df: pd.DataFrame, file_id: str) -> DataQA:
    return DataQA(df, file_id)
