from pydantic import BaseModel, Field

from src.models import StateStatus
from src.models.structured_cv import TailoredCV
from src.state_updates import CVTailorUpdate


class CVTailoredResult(BaseModel):
    cv_edits: str = Field(
        description=(
            "Clear, human-readable summary of all changes made to the CV. "
            "Describe what was modified in the summary, skills, and experience bullets."
        )
    )
    tailored_cv: TailoredCV = Field(
        description=(
            "The full updated CV after tailoring. "
            "Keep company names, job titles, and dates unchanged. "
            "Rewrite summary, reorder skills, and REWRITE ALL experience bullets based on the rewrite style. "
            "For strong_rewrite: completely rewrite every bullet to be more impactful and professional."
        )
    )