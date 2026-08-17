from typing import Literal

StateStatus = Literal[
        "initialized",
        "fit_analyzed",
        "awaiting_fit_approval",
        "company_researched",
        "cv_tailored",
        "cv_tailored_approved",
        "mail_written",
        "awaiting_outreach_approval",
        "outreach_rejected",
        "ready_for_export",
        "rejected"
    ]