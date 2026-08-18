import uuid

from dotenv import load_dotenv
load_dotenv()

from src.cli import run_graph
from src.config import CV_PATH, DEFAULT_JOB_OFFER_URL
from src.graph import build_graph
from src.services import fetch_job, apply_cv_edits
from src.services.parse_cv import parse_cv
from src.services.parse_offer import parse_offer
from src import State


def main():
    graph = build_graph()
    structured_cv = parse_cv(CV_PATH)
    structured_offer = parse_offer(
        fetch_job(DEFAULT_JOB_OFFER_URL)
    )

    initial_state: State = {
        "offer": structured_offer,
        "cv": structured_cv,
        "fit_score": None,
        "fit_gaps": [],
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

    final_state = run_graph(graph=graph, initial_state=initial_state, config=config)

    tailored_cv = final_state.get("tailored_cv")
    if tailored_cv is None:
        raise ValueError("Graph finished without tailored CV. Cannot apply CV edits.")

    output_path = CV_PATH.with_name(f"{CV_PATH.stem}_tailored{CV_PATH.suffix}")
    saved_path = apply_cv_edits(
        original_docx_path=CV_PATH,
        tailored_cv=tailored_cv,
        output_path=output_path,
    )
    print(f"Tailored CV saved to: {saved_path}")


if __name__ == "__main__":
    main()
