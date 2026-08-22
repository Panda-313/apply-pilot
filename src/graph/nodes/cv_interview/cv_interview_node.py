from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.types import interrupt

from src import State
from src.config import BASE_NODE_MODEL, CV_INTERVIEW_NODE_PROMPT, CV_INTERVIEW_CONTEXT
from src.state_updates import CVInterviewUpdate
from .schema import InterviewTurn

def _quit(result: InterviewTurn) -> bool:
    text = (result.assistant_message or "").lower()
    return any(word in text for word in ["stop applying", "do not apply", "rejected", "won't apply"])


def cv_interview_node(state: State) -> CVInterviewUpdate:
    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)
    structured_llm = llm.with_structured_output(InterviewTurn)

    messages = list(state.get("interview_messages") or [])
    context = CV_INTERVIEW_CONTEXT.format(
        offer=state.get("offer"),
        cv=state.get("cv"),
        fit_score=state.get("fit_score"),
        fit_gaps=state.get("fit_gaps"),
        fit_rationale=state.get("fit_rationale"),
        company_name=state.get("company_name"),
        company_type=state.get("company_type"),
        company_summary=state.get("company_summary"),
    )

    if not messages:
        result = structured_llm.invoke([
            SystemMessage(content=CV_INTERVIEW_NODE_PROMPT),
            HumanMessage(content=context + "\nStart the interview with the fit summary and ask if they want to proceed."),
        ])
        return {
            "interview_messages": [AIMessage(content=result.assistant_message)],
            "status": "awaiting_interview",
        }

    last_ai = messages[-1].content if messages else ""
    user_text = interrupt({
        "type": "interview",
        "status": "awaiting_interview",
        "question": last_ai,
    })

    result = structured_llm.invoke([
        SystemMessage(content=CV_INTERVIEW_NODE_PROMPT),
        HumanMessage(content=context),
        *messages,
        HumanMessage(content=str(user_text)),
    ])

    new_messages = [
        HumanMessage(content=str(user_text)),
        AIMessage(content=result.assistant_message),
    ]

    if result.is_complete and result.clarifications is not None:
        return {
            "interview_messages": new_messages,
            "clarifications": result.clarifications,
            "status": "interview_complete",
        }

    if _quit(result):
        return {
            "interview_messages": new_messages,
            "status": "rejected",
        }

    return {
        "interview_messages": new_messages,
        "status": "awaiting_interview",
    }