from langgraph.constants import END

from src import State


def cv_interview_router(state: State):
    status = state["status"]

    if status == "interview_complete":
        return 'cv_tailor_node'

    if status == "rejected":
        return END

    return 'cv_interview_node'