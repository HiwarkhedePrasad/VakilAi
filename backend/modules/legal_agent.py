# modules/legal_agent.py
from langgraph.graph import StateGraph, END
from modules.state import AnalysisState
from modules.agent_nodes import parse_clauses_node, analyze_each_clause_node

def should_continue(state: AnalysisState):
    if state["status"] == "failed":
        return END
    return "analyze"

def build_legal_agent():
    workflow = StateGraph(AnalysisState)

    workflow.add_node("parse", parse_clauses_node)
    workflow.add_node("analyze", analyze_each_clause_node)

    workflow.set_entry_point("parse")
    workflow.add_conditional_edges("parse", should_continue)
    workflow.add_edge("analyze", END)

    return workflow.compile()