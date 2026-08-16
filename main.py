import uuid

from dotenv import load_dotenv

from src.cli import run_graph
from src.config import CV_PATH
from src.graph import build_graph
from src.services import fetch_job
from src.services.parse_cv import parse_cv
from src.services.parse_offer import parse_offer
from src import State

load_dotenv()


def main():
    graph = build_graph()
    structured_cv = parse_cv(CV_PATH)
    structured_offer = parse_offer(
        fetch_job("https://nofluffjobs.com/job/senior-java-cloud-developer-azure-dahliamatic-warszawa-1")
    )

    initial_state: State = {
        "offer": structured_offer,
        "cv": structured_cv,
        "fit_score": None,
        "fit_gaps": [],
        "fit_rationale": None,
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

    run_graph(graph=graph, initial_state=initial_state, config=config)


if __name__ == "__main__":
    main()
