from src import State


def run_graph(graph, initial_state: State, config: dict):
    result = graph.invoke(initial_state, config=config)

    print(result)


