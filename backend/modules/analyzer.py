# modules/analyzer.py
import os
import google.generativeai as genai
from typing import Dict
from dotenv import load_dotenv
load_dotenv()
class ClauseAnalyzer:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_risk(self, clause: str, legal_refs: list) -> Dict[str, str]:
        legal_context = "\n".join([
            f"{ref.get('act', '')} Section {ref.get('section', '')}: {ref.get('text', '')}"
            for ref in legal_refs[:2]
        ]) or "No specific legal reference found."

        prompt = f"""
        Analyze this contract clause for risk to the user:
        CLAUSE: "{clause}"

        Relevant legal context:
        {legal_context}

        Respond in JSON format only:
        {{
            "risk_level": "low|medium|high",
            "explanation": "1-2 sentence reason"
        }}
        """

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            import json
            return json.loads(response.text)
        except Exception as e:
            return {
                "risk_level": "medium",
                "explanation": f"Analysis failed: {str(e)}"
            }