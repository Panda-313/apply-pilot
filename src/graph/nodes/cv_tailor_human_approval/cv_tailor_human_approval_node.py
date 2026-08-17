from langchain_core.messages import HumanMessage
from langgraph.types import interrupt

from .schema import CVTailorHumanApprovalResult
from src import State


def cv_tailor_human_approval_node(state: State) -> CVTailorHumanApprovalResult:
    human_decision = interrupt({
        "type": "cv_tailor_approval",
        "cv_edits": state["cv_edits"],
        "tailored_cv": state["tailored_cv"],
    })
    action = human_decision.get("action", "resume")
    feedback = human_decision.get("feedback", "")

    if action == "resume":
        return {
            "status": "cv_tailored_approved",
            "messages": [
                HumanMessage(content="Accepted tailored CV")
            ],
        }

    if action == "exit":
        return {
            "status": "rejected",
            "messages": [
                HumanMessage(content="Rejected tailored CV, quitting")
            ],
        }

    return {
        "status": "cv_tailored",
        "tailored_cv_feedback": feedback,
        "messages": [
            HumanMessage(content="Added feedback to tailored CV, redoing")
        ]
    }
