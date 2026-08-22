from src import State


def fit_analysis_router(state: State):
    if state.get("fit_analysis_cv_source") == "tailored_cv":
        return "cv_tailor_human_approval_node"

    return "company_research_node"
