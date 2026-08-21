from typing import TypedDict

from pydantic import BaseModel, Field

from src.models import CompanyType, StateStatus
from src.state_updates import CompanyResearchUpdate


class CompanyResearchResult(BaseModel):
    company_name: str = Field(description="Official or most commonly used company name")
    company_type: CompanyType = Field(
        description="product = builds its own product; outsourcing = software house / body leasing; unknown = cannot determine"
    )
    company_summary: str = Field(
        description="3-6 sentence summary of what the company does, its main business, and relevant context for a job candidate"
    )