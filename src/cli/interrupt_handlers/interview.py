import questionary


def handle_interview(interrupt_value: dict) -> str:
    question = interrupt_value.get("question", "")
    
    if question:
        print(f"\n{question}\n")
    
    answer = questionary.text("Your response:").ask()
    
    return answer or ""
