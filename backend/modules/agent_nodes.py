# modules/agent_nodes.py
from modules.state import AnalysisState
from modules.ingestion import DocumentExtractor
from modules.retriever import LegalRetriever
from modules.analyzer import ClauseAnalyzer
from modules.advisor import LegalAdvisor
import os

extractor = DocumentExtractor()
retriever = LegalRetriever()
analyzer = ClauseAnalyzer()
advisor = LegalAdvisor()

def parse_clauses_node(state: AnalysisState) -> dict:
    try:
        text = extractor.extract_text(state["file_path"])
        raw_clauses = extractor.parse_clauses(text)
        clauses = [
            {"id": c["id"], "text": c["text"], "risk": None, "suggestion": None, "legal_reference": None}
            for c in raw_clauses
        ]
        return {
            "raw_text": text,
            "clauses": clauses,
            "status": "parsed"
        }
    except Exception as e:
        return {"status": "failed", "error": f"Parse failed: {str(e)}"}

def analyze_each_clause_node(state: AnalysisState) -> dict:
    updated_clauses = []
    for clause in state["clauses"]:
        try:
            # Retrieve legal context
            refs = retriever.search_legal_references(clause["text"])
            legal_ref = refs[0] if refs else {"act": "N/A", "section": "N/A", "url": ""}

            # Analyze risk
            risk_result = analyzer.analyze_risk(clause["text"], refs)
            risk_level = risk_result.get("risk_level", "medium")

            # Generate advice
            suggestion = advisor.generate_suggestion(clause["text"], risk_result)

            updated_clauses.append({
                "id": clause["id"],
                "text": clause["text"],
                "risk": risk_level,
                "suggestion": suggestion,
                "legal_reference": legal_ref
            })
        except Exception as e:
            updated_clauses.append({
                **clause,
                "risk": "unknown",
                "suggestion": f"Analysis error: {str(e)}",
                "legal_reference": {"act": "Error", "section": "—", "url": ""}
            })
    
    # Cleanup temp file
    if os.path.exists(state["file_path"]):
        os.remove(state["file_path"])

    return {
        "clauses": updated_clauses,
        "status": "completed"
    }