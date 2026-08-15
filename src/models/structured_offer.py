from pydantic import BaseModel, Field


class StructuredOffer(BaseModel):
    title: str = Field(description="Job title / position name")
    company_name: str = Field(description="Name of the hiring company (or the end client if it's body leasing)")
    description: str = Field(description="Concise summary of the role and project context (2-5 sentences)")
    must_have: list[str] = Field(description="Required skills, technologies and experience. Only explicitly stated requirements.")
    nice_to_have: list[str] = Field(description="Nice-to-have / preferred skills and technologies.")
    tech_stack: list[str] = Field(description="All technologies, tools and frameworks mentioned in the offer")
    raw_text: str = Field(description="Original cleaned text of the offer. Do not modify.")