from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .schema import CVTailoredResult
from src.state_updates import CVTailorUpdate
from src.config import BASE_NODE_MODEL, CV_TAILORED_NODE_SYSTEM_MESSAGE, \
    CV_TAILORED_NODE_HUMAN_MESSAGE
from src import State


def _normalize_style(style: str) -> str:
    style_lower = style.lower().strip().replace(" ", "_").replace("-", "_")
    if "strong" in style_lower or "complete" in style_lower or "full" in style_lower:
        return "strong_rewrite"
    if "conserv" in style_lower or "minimal" in style_lower:
        return "conservative"
    return "polished"


def cv_tailor_node(state: State) -> CVTailorUpdate:
    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)

    llm_structured = llm.with_structured_output(CVTailoredResult)
    tailored_cv_feedback = state.get("tailored_cv_feedback") or "No reviewer feedback provided. Perform the initial tailoring based on the offer."
    company_name = state.get("company_name") or state["offer"].company_name
    company_type = state.get("company_type") or "unknown"
    company_summary = state.get("company_summary") or "No company research summary available."
    
    clarifications = state.get("clarifications")
    raw_style = clarifications.style if clarifications else "polished"
    clarifications_style = _normalize_style(raw_style)
    clarifications_rewrite_permission = clarifications.rewrite_permission if clarifications else True
    clarifications_skill_years = clarifications.skill_years if clarifications else []
    clarifications_confirmed_additions = clarifications.confirmed_additions if clarifications else []
    clarifications_rejected_gaps = clarifications.rejected_gaps if clarifications else []
    clarifications_languages = clarifications.languages if clarifications and hasattr(clarifications, 'languages') else []

    cv_languages = getattr(state["cv"], 'languages', []) if state.get("cv") else []

    system_message = SystemMessage(CV_TAILORED_NODE_SYSTEM_MESSAGE)
    human_message = HumanMessage(
        CV_TAILORED_NODE_HUMAN_MESSAGE.format(
            offer=state["offer"],
            cv=state["cv"],
            tailored_cv_feedback=tailored_cv_feedback,
            company_name=company_name,
            company_type=company_type,
            company_summary=company_summary,
            clarifications_style=clarifications_style,
            clarifications_rewrite_permission=clarifications_rewrite_permission,
            clarifications_skill_years=clarifications_skill_years,
            clarifications_confirmed_additions=clarifications_confirmed_additions,
            clarifications_rejected_gaps=clarifications_rejected_gaps,
            clarifications_languages=clarifications_languages or cv_languages,
        )
    )

    result = llm_structured.invoke([system_message, human_message])

    return {
        "cv_edits": result.cv_edits,
        "tailored_cv": result.tailored_cv,
        "status": "cv_tailored",
    }
