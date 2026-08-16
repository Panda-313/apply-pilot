import questionary
from langgraph.types import Command

from src import State


def run_graph(graph, initial_state: State, config: dict):
    result = graph.invoke(initial_state, config=config)

    while True:
        snapshot = graph.get_state(config=config)

        if not snapshot.tasks or not snapshot.tasks[0].interrupts:
            break

        interrupt_value = snapshot.tasks[0].interrupts[0].value

        print(f"Outcome of analysis of your CV being matched with offer: \n\n "
              f"Fit score: {interrupt_value["fit_score"]} \n\n"
              f"Fit gaps: {interrupt_value['fit_gaps']} \n\n"
              f"Fit rationale: {interrupt_value['fit_rationale']} \n\n"
              f"Fit recommendation: {interrupt_value['fit_recommendation']}\n\n"
        )

        human_decision = questionary.select(
            "Czy zgadzasz sie z podanym wynikiem?",
            choices=[
                questionary.Choice("Accept", value="accept"),
                questionary.Choice("Reject (quit)", value="reject"),
                questionary.Choice("Add feedback and score again", value="feedback"),
            ],
        ).ask()

        if human_decision == "accept":
            resume_value = {
                "action": "resume",
            }
        elif human_decision == "reject":
            resume_value = {
                "action": "exit",
            }
        else:
            resume_value = {
                "action": "feedback",
                "feedback": input("\n Give feedback: \n")
            }

        result = graph.invoke(Command(resume=resume_value), config=config)



