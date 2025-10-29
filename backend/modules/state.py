# modules/state.py
from typing import List, Dict, Optional
from typing_extensions import TypedDict, Annotated
import operator

class Clause(TypedDict):
    id: int
    text: str
    risk: Optional[str]
    suggestion: Optional[str]
    legal_reference: Optional[Dict]

class AnalysisState(TypedDict):
    job_id: str
    file_path: str
    file_name: str
    raw_text: str
    clauses: Annotated[List[Clause], operator.add]
    status: str  # "uploaded", "parsing", "analyzing", "completed", "failed"
    error: Optional[str]