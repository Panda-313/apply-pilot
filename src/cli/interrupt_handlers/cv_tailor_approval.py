import questionary


def handle_cv_tailor_approval(interrupt_value: dict) -> dict:
    print(
        f"Tailored CV result:\n\n"
        f"CV Edits: {interrupt_value['cv_edits']}\n\n"
        f"Tailored CV:\n{interrupt_value['tailored_cv']}\n"
    )

    human_decision = questionary.select(
        "Do you accept the changes in the CV?",
        choices=[
            questionary.Choice("Accept", value="accept"),
            questionary.Choice("Reject (quit)", value="reject"),
            questionary.Choice("Add feedback and tailor again", value="feedback"),
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
