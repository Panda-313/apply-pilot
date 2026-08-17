import questionary


def handle_fit_analyst_approval(interrupt_value: dict) -> dict:
    print(
        f"Outcome of analysis of your CV being matched with offer:\n\n"
        f"Fit score: {interrupt_value['fit_score']}\n\n"
        f"Fit gaps: {interrupt_value['fit_gaps']}\n\n"
        f"Fit rationale: {interrupt_value['fit_rationale']}\n\n"
        f"Fit recommendation: {interrupt_value['fit_recommendation']}\n"
    )

    human_decision = questionary.select(
        "Do you agree with given score?",
        choices=[
            questionary.Choice("Accept", value="accept"),
            questionary.Choice("Reject (quit)", value="reject"),
            questionary.Choice("Add feedback and score again", value="feedback"),
        ],
    ).ask()

    if human_decision == "accept":
        return {"action": "resume"}
    elif human_decision == "reject":
        return {"action": "exit"}
    else:
        return {
            "action": "feedback",
            "feedback": input("\nGive feedback:\n"),
        }
