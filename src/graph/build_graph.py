from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph

from src import State


def build_graph(checkpointer=None):
    if checkpointer is None:
        checkpointer = InMemorySaver()

    builder = StateGraph(State)

    return builder.compile(checkpointer)