from pydantic import BaseModel, Field


class ExperienceItem(BaseModel):
    company: str = Field(description="Company name exactly as written")
    title: str = Field(description="Job title exactly as written")
    start_date: str | None = Field(description="Start date exactly as written (or null if missing)")
    end_date: str | None = Field(description="End date exactly as written (or null if missing / Present)")
    bullets: list[str] = Field(description="List of bullet points copied EXACTLY as they appear. Do not rephrase.")


class EducationItem(BaseModel):
    institution: str = Field(description="School / University name exactly as written")
    degree: str | None = Field(description="Degree or field of study exactly as written")
    start_date: str | None = Field(description="Start date exactly as written")
    end_date: str | None = Field(description="End date exactly as written")

class StructuredCV(BaseModel):
    full_name: str | None = Field(description="Full name of the candidate exactly as written")
    email: str | None = Field(description="Email address exactly as written")
    phone: str | None = Field(description="Phone number exactly as written")

    summary: str = Field(description="Professional summary / profile section. Copy as closely as possible.")
    skills: list[str] = Field(description="List of skills exactly as they appear in the CV")
    experience: list[ExperienceItem] = Field(description="Work experience entries in reverse chronological order")
    education: list[EducationItem] = Field(description="Education entries")

    raw_text: str = Field(description="Full original text extracted from the CV. Do not modify.")