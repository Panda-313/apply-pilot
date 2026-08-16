from typing import Literal

StateStatus = Literal[
        "initialized",
        "fit_analyzed",
        "awaiting_fit_approval",
        "fit_rejected",
        "researching_company",
        "company_filtered",
        "company_skipped",
        "cv_tailored",
        "mail_written",
        "awaiting_outreach_approval",
        "outreach_rejected",
        "ready_for_export",
        "rejected"
    ]