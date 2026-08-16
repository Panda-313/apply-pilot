from langgraph.constants import END

from src import State


def fit_analyst_router(state: State):
    status = state["status"]

    if status == "fit_analyzed":
        return END

    if status == "rejected":
        return END

    if status == "initialized":
        return "fit_analyst_node"