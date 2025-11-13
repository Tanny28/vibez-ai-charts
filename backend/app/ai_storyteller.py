import os
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

class AIStoryteller:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_story(self, insights: List[Dict[str, Any]], chart_config: Dict[str, Any], context: Optional[str] = None) -> str:
        try:
            prompt = self._create_story_prompt(insights, chart_config, context)
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating story: {e}")
            return "Unable to generate story."
    
    def enhance_insight(self, insight: Dict[str, Any]) -> str:
        try:
            prompt = f"Explain in 1-2 sentences: {insight.get('category')}: {insight.get('summary')}"
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error enhancing insight: {e}")
            return insight.get('summary', '')
    
    def suggest_next_analysis(self, insights: List[Dict[str, Any]], chart_type: str) -> List[str]:
        try:
            summary = "\n".join([f"{i.get('category')}: {i.get('summary')}" for i in insights[:3]])
            prompt = f"Based on:\n{summary}\n\nSuggest 3 questions as JSON array: [\"Q1?\", \"Q2?\", \"Q3?\"]"
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            if '```' in text:
                text = text.split('```')[1].replace('json', '').strip()
            return json.loads(text)[:3]
        except Exception as e:
            print(f"Error generating suggestions: {e}")
            return ["What drives these trends?", "How do patterns compare?", "What actions optimize metrics?"]
    
    def answer_question(self, question: str, data_context: str, insights: List[Dict[str, Any]]) -> str:
        try:
            summary = "\n".join([f"{i.get('category')}: {i.get('summary')}" for i in insights[:3]])
            prompt = f"Question: {question}\n\nData: {data_context}\n\nInsights:\n{summary}\n\nAnswer:"
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error answering question: {e}")
            return "Error analyzing data."
    
    def _create_story_prompt(self, insights: List[Dict[str, Any]], chart_config: Dict[str, Any], context: Optional[str]) -> str:
        summary = "\n".join([f"{i.get('category')}: {i.get('summary')}" for i in insights[:3]])
        return f"Chart: {chart_config.get('type')}\n\nInsights:\n{summary}\n\nWrite 2-3 sentences highlighting key findings."

_storyteller = None

def get_storyteller():
    global _storyteller
    if _storyteller is None:
        _storyteller = AIStoryteller()
    return _storyteller
