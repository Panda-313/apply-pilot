from langgraph.types import Command

from src import State
from src.cli.interrupt_handlers import handle_interrupt


def run_graph(graph, initial_state: State, config: dict):
    graph.invoke(initial_state, config=config)

    while True:
        snapshot = graph.get_state(config=config)

        if not snapshot.next:
            break

        if not snapshot.tasks or not snapshot.tasks[0].interrupts:
            graph.invoke(None, config=config)
            continue

        interrupt_value = snapshot.tasks[0].interrupts[0].value
        resume_value = handle_interrupt(interrupt_value)

        graph.invoke(Command(resume=resume_value), config=config)
    return snapshot.values
