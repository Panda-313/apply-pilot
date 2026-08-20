from typing import Literal

StateStatus = Literal[
        "initialized",
        "fit_analyzed",
        "awaiting_fit_approval",
        "company_researched",
        "cv_tailored",
        "cv_tailored_approved",
        "rejected"
    ]