from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph

from .nodes.company_research import company_research_node
from .nodes.cv_tailor import cv_tailor_node
from .nodes.cv_tailor_human_approval import cv_tailor_human_approval_node
from .nodes.cv_interview import cv_interview_node
from .nodes.fit_analyst import fit_analyst_node
from src import State
from .router import fit_analysis_router, cv_tailored_router, cv_interview_router


def build_graph(checkpointer=None):
    if checkpointer is None:
        checkpointer = InMemorySaver()

    builder = StateGraph(State)
    builder.add_node("fit_analyst_node", fit_analyst_node)
    builder.add_node("company_research_node", company_research_node)
    builder.add_node("cv_interview_node", cv_interview_node)
    builder.add_node("cv_tailor_node", cv_tailor_node)
    builder.add_node("cv_tailor_human_approval_node", cv_tailor_human_approval_node)

    builder.add_edge(START, "fit_analyst_node")
    builder.add_conditional_edges("fit_analyst_node", fit_analysis_router)
    builder.add_edge("company_research_node", "cv_interview_node")
    builder.add_conditional_edges("cv_interview_node", cv_interview_router)
    builder.add_edge("cv_tailor_node", "fit_analyst_node")
    builder.add_conditional_edges("cv_tailor_human_approval_node", cv_tailored_router)

    return builder.compile(checkpointer=checkpointer)