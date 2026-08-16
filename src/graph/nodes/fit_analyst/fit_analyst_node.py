from typing import cast

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config import BASE_NODE_MODEL, FIT_ANALYST_SYSTEM_PROMPT, FIT_ANALYST_HUMAN_MESSAGE
from .schema import FitAnalystResult
from src import State


def fit_analyst_node(state: State) -> dict:
    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)

    structured_llm = llm.with_structured_output(FitAnalystResult)
    analysis_feedback = state.get("analysis_feedback") or "No reviewer feedback provided. Perform the initial evidence-based analysis."

    system_message = SystemMessage(FIT_ANALYST_SYSTEM_PROMPT)
    human_message = HumanMessage(
        FIT_ANALYST_HUMAN_MESSAGE.format(
            offer=state["offer"],
            cv=state["cv"],
            analysis_feedback=analysis_feedback,
        )
    )

    prompt = ChatPromptTemplate.from_messages([system_message, human_message])
    result = cast(FitAnalystResult, structured_llm.invoke(prompt.format_messages()))

    return {
        "fit_score": result.fit_score,
        "fit_gaps": result.fit_gaps,
        "fit_rationale": result.fit_rationale,
        "fit_recommendation": result.fit_recommendation,
        "status": "awaiting_fit_approval",
    }