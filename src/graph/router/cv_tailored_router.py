from langgraph.constants import END

from src import State


def cv_tailored_router(state: State):
    status = state["status"]

    if status == "cv_tailored_approved":
        return END

    if status == "rejected":
        return END

    if status == "cv_tailored":
        return "cv_tailor_node"

    return END