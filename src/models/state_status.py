from typing import Literal

StateStatus = Literal[
        "initialized",
        "awaiting_interview",
        "interview_complete",
        "fit_analyzed",
        "awaiting_fit_approval",
        "company_researched",
        "cv_tailored",
        "cv_tailored_approved",
        "rejected"
    ]
