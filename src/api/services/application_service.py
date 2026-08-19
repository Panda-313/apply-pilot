import uuid

from src import State
from src.graph import build_graph


class ApplicationService:
    def __init__(self, checkpointer):
        self.checkpointer = checkpointer
        self.graph = None

    def _ensure_graph(self) -> None:
        if self.graph is None:
            self.graph = build_graph(self.checkpointer)


    def create_application(self, structured_cv, structured_offer):
        self._ensure_graph()

        initial_state: State = {
            "offer": structured_offer,
            "cv": structured_cv,
            "fit_score": None,
            "fit_gaps": [],
            "fit_analysis_cv_source": None,
            "fit_rationale": None,
            "analysis_feedback": None,
            "tailored_cv_feedback": None,
            "fit_recommendation": None,
            "company_name": None,
            "company_type": None,
            "company_summary": None,
            "cv_edits": None,
            "tailored_cv": None,
            "mail_draft": None,
            "status": "initialized",
            "human_feedback": None,
            "messages": [],
        }

        config = {
            "configurable": {
                "thread_id": uuid.uuid4().hex[:8]
            }
        }

        result = self.graph.invoke(initial_state, config)

        return result, config["configurable"]["thread_id"]




