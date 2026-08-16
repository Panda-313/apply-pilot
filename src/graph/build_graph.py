from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from .nodes.fit_analyst import fit_analyst_node
from src import State


def build_graph(checkpointer=None):
    if checkpointer is None:
        checkpointer = InMemorySaver()

    builder = StateGraph(State)
    builder.add_node("fit_analyst_node", fit_analyst_node)


    builder.add_edge(START, "fit_analyst_node")
    builder.add_edge( "fit_analyst_node", END)

    return builder.compile(checkpointer=checkpointer)