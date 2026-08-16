from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from .nodes.fit_analyst import fit_analyst_node
from src import State
from .nodes.fit_analyst_human_approval import fit_analyst_human_approval_node
from .router import fit_analyst_router


def build_graph(checkpointer=None):
    if checkpointer is None:
        checkpointer = InMemorySaver()

    builder = StateGraph(State)
    builder.add_node("fit_analyst_node", fit_analyst_node)
    builder.add_node("analyst_human_approval_node", fit_analyst_human_approval_node)


    builder.add_edge(START, "fit_analyst_node")
    builder.add_edge( "fit_analyst_node", "analyst_human_approval_node")
    builder.add_conditional_edges( "analyst_human_approval_node", fit_analyst_router)

    return builder.compile(checkpointer=checkpointer)