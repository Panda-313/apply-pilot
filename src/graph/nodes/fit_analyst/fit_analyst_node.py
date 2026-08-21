from typing import cast

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config import BASE_NODE_MODEL, FIT_ANALYST_SYSTEM_PROMPT, FIT_ANALYST_HUMAN_MESSAGE
from .schema import FitAnalystResult
from src.state_updates import FitAnalystUpdate
from src import State


def fit_analyst_node(state: State) -> FitAnalystUpdate:
    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)

    structured_llm = llm.with_structured_output(FitAnalystResult)
    analysis_feedback = state.get("analysis_feedback") or "No reviewer feedback provided. Perform the initial evidence-based analysis."
    cv_for_analysis = state.get("tailored_cv") or state["cv"]
    cv_source = "tailored_cv" if state.get("tailored_cv") else "cv"

    system_message = SystemMessage(FIT_ANALYST_SYSTEM_PROMPT)
    human_message = HumanMessage(
        FIT_ANALYST_HUMAN_MESSAGE.format(
            offer=state["offer"],
            cv=cv_for_analysis,
            analysis_feedback=analysis_feedback,
        )
    )

    prompt = ChatPromptTemplate.from_messages([system_message, human_message])
    result = cast(FitAnalystResult, structured_llm.invoke(prompt.format_messages()))
    print(f"Aktualny wynik: {result.fit_score}")
    return {
        "fit_score": result.fit_score,
        "fit_gaps": result.fit_gaps,
        "fit_rationale": result.fit_rationale,
        "fit_recommendation": result.fit_recommendation,
        "fit_analysis_cv_source": cv_source,
        "status": "awaiting_fit_approval",
    }