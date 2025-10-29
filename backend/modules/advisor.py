# modules/advisor.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
class LegalAdvisor:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_suggestion(self, clause: str, risk_analysis: dict) -> str:
        prompt = f"""
        You are a user-friendly legal advisor. Rewrite or suggest an improvement to this clause 
        to better protect the user's interests. Be concise and practical.

        Original clause: "{clause}"
        Risk level: {risk_analysis.get('risk_level', 'medium')}
        Explanation: {risk_analysis.get('explanation', '')}

        Suggestion (1 sentence max):
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Unable to generate suggestion: {str(e)}"