from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .schema import CVTailoredResult
from src.config import BASE_NODE_MODEL, CV_TAILORED_NODE_SYSTEM_MESSAGE, \
    CV_TAILORED_NODE_HUMAN_MESSAGE
from src import State


def cv_tailor_node(state: State) -> dict:
    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)

    llm_structured = llm.with_structured_output(CVTailoredResult)
    tailored_cv_feedback = state.get("tailored_cv_feedback") or "No reviewer feedback provided. Perform the initial tailoring based on the offer."

    system_message = SystemMessage(CV_TAILORED_NODE_SYSTEM_MESSAGE)
    human_message = HumanMessage(
        CV_TAILORED_NODE_HUMAN_MESSAGE.format(
            offer=state["offer"],
            cv=state["cv"],
            tailored_cv_feedback=tailored_cv_feedback,
        )
    )

    result = llm_structured.invoke([system_message, human_message])


    return {
        "cv_edits": result.cv_edits,
        "tailored_cv": result.tailored_cv,
        "status": "cv_tailored",
    }
