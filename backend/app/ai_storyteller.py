# backend/app/ai_storyteller.py# backend/app/ai_storyteller.py

""""""

AI-powered data storytelling using Google Gemini.AI-powered data storytelling using OpenAI GPT-4.

Generates natural language narratives from data insights.Generates natural language narratives from data insights.

""""""

import osimport os

from typing import Dict, List, Any, Optionalfrom typing import Dict, List, Any, Optional

import google.generativeai as genaifrom openai import OpenAI

from dotenv import load_dotenvfrom dotenv import load_dotenv

import jsonimport json



# Load environment variables# Load environment variables

load_dotenv()load_dotenv()



class AIStoryteller:class AIStoryteller:

    """Generate compelling narratives from data using Google Gemini."""    """Generate compelling narratives from data using OpenAI."""

        

    def __init__(self):    def __init__(self):

        """Initialize Gemini client."""        """Initialize OpenAI client."""

        api_key = os.getenv('GEMINI_API_KEY')        api_key = os.getenv('OPENAI_API_KEY')

        if not api_key:        if not api_key:

            raise ValueError("GEMINI_API_KEY not found in environment variables")            raise ValueError("OPENAI_API_KEY not found in environment variables")

                

        genai.configure(api_key=api_key)        self.client = OpenAI(api_key=api_key)

        self.model = genai.GenerativeModel('gemini-1.5-flash')  # Fast, efficient model        self.model = "gpt-4o-mini"  # Cost-effective, fast model

        

    def generate_story(self, insights: List[Dict[str, Any]], data_summary: Dict[str, Any]) -> str:    def generate_story(self, insights: List[Dict[str, Any]], data_summary: Dict[str, Any]) -> str:

        """        """

        Generate a compelling data story from insights.        Generate a compelling data story from insights.

                

        Args:        Args:

            insights: List of insight dictionaries with category, summary, metrics            insights: List of insight dictionaries with category, summary, metrics

            data_summary: Dataset summary (rows, columns, column names)            data_summary: Dataset summary (rows, columns, column names)

                

        Returns:        Returns:

            Natural language narrative about the data            Natural language narrative about the data

        """        """

        try:        try:

            # Create prompt            # Create prompt

            prompt = self._create_story_prompt(insights, data_summary)            prompt = self._create_story_prompt(insights, data_summary)

                        

            # Call Gemini            # Call OpenAI

            response = self.model.generate_content(prompt)            response = self.client.chat.completions.create(

                            model=self.model,

            story = response.text.strip()                messages=[

            return story                    {

                                    "role": "system",

        except Exception as e:                        "content": "You are a data storytelling expert. Create compelling, concise narratives from business data insights. Use professional language, highlight key trends, and provide actionable recommendations. Keep responses under 200 words."

            print(f"Error generating story: {e}")                    },

            return self._generate_fallback_story(insights)                    {

                            "role": "user",

    def enhance_insight(self, insight: Dict[str, Any]) -> str:                        "content": prompt

        """                    }

        Enhance a single insight with AI-generated explanation.                ],

                        temperature=0.7,

        Args:                max_tokens=300

            insight: Single insight dictionary            )

                    

        Returns:            story = response.choices[0].message.content.strip()

            Enhanced explanation            return story

        """            

        try:        except Exception as e:

            prompt = f"""            print(f"Error generating story: {e}")

Enhance this data insight with a clear, actionable explanation:            return self._generate_fallback_story(insights)

    

Category: {insight.get('category', 'Unknown')}    def enhance_insight(self, insight: Dict[str, Any]) -> str:

Summary: {insight.get('summary', '')}        """

Metrics: {json.dumps(insight.get('metrics', {}), indent=2)}        Enhance a single insight with AI-generated explanation.

        

Provide a 1-2 sentence explanation that a business user can understand and act on.        Args:

"""            insight: Single insight dictionary

                    

            response = self.model.generate_content(prompt)        Returns:

            return response.text.strip()            Enhanced explanation

                    """

        except Exception as e:        try:

            print(f"Error enhancing insight: {e}")            prompt = f"""

            return insight.get('summary', '')Enhance this data insight with a clear, actionable explanation:

    

    def suggest_next_analysis(self, insights: List[Dict[str, Any]]) -> List[str]:Category: {insight.get('category', 'Unknown')}

        """Summary: {insight.get('summary', '')}

        Suggest follow-up analyses based on current insights.Metrics: {json.dumps(insight.get('metrics', {}), indent=2)}

        

        Args:Provide a 1-2 sentence explanation that a business user can understand and act on.

            insights: List of current insights"""

                    

        Returns:            response = self.client.chat.completions.create(

            List of suggested analysis questions                model=self.model,

        """                messages=[

        try:                    {

            insights_summary = "\n".join([                        "role": "system",

                f"- {i.get('category')}: {i.get('summary')}"                         "content": "You are a business analyst. Explain data insights clearly and concisely."

                for i in insights[:5]                    },

            ])                    {

                                    "role": "user",

            prompt = f"""                        "content": prompt

Based on these data insights:                    }

                ],

{insights_summary}                temperature=0.6,

                max_tokens=100

Suggest 3 follow-up questions a user might ask to dive deeper into the data.             )

Format as simple questions, one per line. Do not number them.            

"""            return response.choices[0].message.content.strip()

                        

            response = self.model.generate_content(prompt)        except Exception as e:

            suggestions = response.text.strip().split('\n')            print(f"Error enhancing insight: {e}")

                        return insight.get('summary', '')

            # Clean up suggestions    

            suggestions = [s.strip('- 123.•') for s in suggestions if s.strip()]    def suggest_next_analysis(self, insights: List[Dict[str, Any]]) -> List[str]:

            return suggestions[:3]        """

                    Suggest follow-up analyses based on current insights.

        except Exception as e:        

            print(f"Error generating suggestions: {e}")        Args:

            return [            insights: List of current insights

                "What are the top performing segments?",        

                "How have trends changed over time?",        Returns:

                "Which factors drive the most impact?"            List of suggested analysis questions

            ]        """

            try:

    def answer_question(self, question: str, df_info: Dict[str, Any], sample_data: str) -> str:            insights_summary = "\n".join([

        """                f"- {i.get('category')}: {i.get('summary')}" 

        Answer a data-related question using Gemini.                for i in insights[:5]

                    ])

        Args:            

            question: User's question about the data            prompt = f"""

            df_info: DataFrame information (columns, types, summary stats)Based on these data insights:

            sample_data: Sample rows from the DataFrame

        {insights_summary}

        Returns:

            AI-generated answerSuggest 3 follow-up questions a user might ask to dive deeper into the data. 

        """Format as simple questions, one per line.

        try:"""

            prompt = f"""            

You are a data analyst. Answer this question about the user's data:            response = self.client.chat.completions.create(

                model=self.model,

Question: {question}                messages=[

                    {

Dataset Information:                        "role": "system",

- Columns: {', '.join(df_info.get('columns', []))}                        "content": "You are a data analyst helping users explore their data."

- Total Rows: {df_info.get('total_rows', 'Unknown')}                    },

- Column Types: {json.dumps(df_info.get('dtypes', {}), indent=2)}                    {

                        "role": "user",

Sample Data (first 5 rows):                        "content": prompt

{sample_data}                    }

                ],

Summary Statistics:                temperature=0.7,

{json.dumps(df_info.get('statistics', {}), indent=2)}                max_tokens=150

            )

Provide a clear, concise answer based on the data. If you cannot answer from the available information, say so and suggest what analysis would help.            

Keep your answer under 150 words.            suggestions = response.choices[0].message.content.strip().split('\n')

"""            # Clean up suggestions

                        suggestions = [s.strip('- 123.') for s in suggestions if s.strip()]

            response = self.model.generate_content(prompt)            return suggestions[:3]

            return response.text.strip()            

                    except Exception as e:

        except Exception as e:            print(f"Error generating suggestions: {e}")

            print(f"Error answering question: {e}")            return [

            return "I apologize, but I'm having trouble analyzing your data right now. Please try rephrasing your question or upload your data again."                "What are the top performing segments?",

                    "How have trends changed over time?",

    def _create_story_prompt(self, insights: List[Dict[str, Any]], data_summary: Dict[str, Any]) -> str:                "Which factors drive the most impact?"

        """Create a prompt for story generation."""            ]

        insights_text = "\n".join([    

            f"- {i.get('category', 'Insight')}: {i.get('summary', 'N/A')}"    def _create_story_prompt(self, insights: List[Dict[str, Any]], data_summary: Dict[str, Any]) -> str:

            for i in insights[:5]        """Create a prompt for story generation."""

        ])        insights_text = "\n".join([

                    f"- {i.get('category', 'Insight')}: {i.get('summary', 'N/A')}"

        return f"""            for i in insights[:5]

Create a compelling data story from these insights:        ])

        

Dataset: {data_summary.get('total_rows', 'Unknown')} rows, {data_summary.get('total_columns', 'Unknown')} columns        return f"""

Create a compelling data story from these insights:

Key Insights:

{insights_text}Dataset: {data_summary.get('total_rows', 'Unknown')} rows, {data_summary.get('total_columns', 'Unknown')} columns



Write a professional narrative that:Key Insights:

1. Highlights the most important findings{insights_text}

2. Identifies trends and patterns

3. Provides actionable recommendationsWrite a professional narrative that:

4. Uses business-friendly language1. Highlights the most important findings

2. Identifies trends and patterns

Keep it concise (under 200 words).3. Provides actionable recommendations

"""4. Uses business-friendly language

    

    def _generate_fallback_story(self, insights: List[Dict[str, Any]]) -> str:Keep it concise (under 200 words).

        """Generate a basic story without AI if API fails.""""""

        if not insights:    

            return "Your data has been analyzed. Upload a file to see detailed insights."    def _generate_fallback_story(self, insights: List[Dict[str, Any]]) -> str:

                """Generate a basic story without AI if API fails."""

        parts = []        if not insights:

        parts.append("📊 Data Analysis Summary")            return "Your data has been analyzed. Upload a file to see detailed insights."

        parts.append("")        

                parts = []

        for insight in insights[:3]:        parts.append("📊 Data Analysis Summary")

            category = insight.get('category', 'Insight')        parts.append("")

            summary = insight.get('summary', '')        

            if summary:        for insight in insights[:3]:

                parts.append(f"• {category}: {summary}")            category = insight.get('category', 'Insight')

                    summary = insight.get('summary', '')

        return "\n".join(parts)            if summary:

                parts.append(f"• {category}: {summary}")

        

# Singleton instance        return "\n".join(parts)

_storyteller_instance = None



def get_storyteller() -> AIStoryteller:# Singleton instance

    """Get or create the AI storyteller singleton."""_storyteller_instance = None

    global _storyteller_instance

    if _storyteller_instance is None:def get_storyteller() -> AIStoryteller:

        try:    """Get or create the AI storyteller singleton."""

            _storyteller_instance = AIStoryteller()    global _storyteller_instance

        except Exception as e:    if _storyteller_instance is None:

            print(f"Warning: Could not initialize AI Storyteller: {e}")        try:

            _storyteller_instance = None            _storyteller_instance = AIStoryteller()

    return _storyteller_instance        except Exception as e:

            print(f"Warning: Could not initialize AI Storyteller: {e}")
            _storyteller_instance = None
    return _storyteller_instance
