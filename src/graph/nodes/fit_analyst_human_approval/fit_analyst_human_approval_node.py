from langchain_core.messages import HumanMessage
from langgraph.types import interrupt

from src.graph.nodes.fit_analyst_human_approval import FitAnalystHumanApprovalResult
from src import State


def fit_analyst_human_approval_node(state: State) -> FitAnalystHumanApprovalResult:
    human_decision = interrupt({
        "type": "fit_analyst_approval",
        "fit_score": state["fit_score"],
        "fit_gaps": state["fit_gaps"],
        "fit_rationale": state["fit_rationale"],
        "fit_recommendation": state["fit_recommendation"],
    })

    action = human_decision.get("action", "resume")
    feedback = human_decision.get("feedback", "")

    if action == "resume":
        return {
            "status": "fit_analyzed",
            "messages": [
                HumanMessage(content=f"Accepted fit analysis")
            ],
        }

    if action == "exit":
        return {
            "status": "rejected",
            "messages": [
                HumanMessage(content=f"Rejected fit analysis, quiting")
            ],
        }

    return {
        "status": "initialized",
        "analysis_feedback": feedback,
        "messages": [
            HumanMessage(content=f"Added feedback to fit analysis, redoing")
        ]
    }
