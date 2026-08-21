from pydantic import BaseModel, Field

from src.models import StateStatus
from src.models.structured_cv import TailoredCV
from src.state_updates import CVTailorUpdate


class CVTailoredResult(BaseModel):
    cv_edits: str = Field(
        description=(
            "Clear, human-readable summary of all changes made to the CV. "
            "Describe what was modified in the summary, skills, and experience bullets. "
            "Do not invent any new jobs, companies, dates or skills."
        )
    )
    tailored_cv: TailoredCV = Field(
        description=(
            "The full updated CV after tailoring. "
            "Keep all company names, job titles, dates and original experience entries exactly as they were. "
            "You may only improve the professional summary, re-order/add relevant skills that already exist, "
            "and rephrase existing bullets to better match the job offer. "
            "Never add fabricated experience. "
        )
    )