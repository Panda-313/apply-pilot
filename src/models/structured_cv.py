from pydantic import BaseModel, Field


class ExperienceItem(BaseModel):
    company: str = Field(description="Company name exactly as written")
    title: str = Field(description="Job title exactly as written")
    start_date: str | None = Field(description="Start date exactly as written (or null if missing)")
    end_date: str | None = Field(description="End date exactly as written (or null if missing / Present)")
    bullets: list[str] = Field(description="List of bullet points - REWRITE to be more impactful, professional, with action verbs and quantifiable achievements. Fix grammar and improve clarity.")


class EducationItem(BaseModel):
    institution: str = Field(description="School / University name exactly as written")
    degree: str | None = Field(description="Degree or field of study exactly as written")
    start_date: str | None = Field(description="Start date exactly as written")
    end_date: str | None = Field(description="End date exactly as written")

class LanguageItem(BaseModel):
    language: str = Field(description="Language name (e.g., Polish, English)")
    level: str = Field(description="Proficiency level (e.g., native, fluent, B2, C1)")


class TailoredCV(BaseModel):
    full_name: str | None = Field(description="Full name of the candidate exactly as written")
    email: str | None = Field(description="Email address exactly as written")
    phone: str | None = Field(description="Phone number exactly as written")

    summary: str = Field(description="Professional summary - REWRITE to be compelling and targeted to the job offer")
    skills: list[str] = Field(description="List of skills - reorder to put most relevant first, add confirmed skills")
    experience: list[ExperienceItem] = Field(description="Work experience - REWRITE ALL bullets to be professional, impactful, with better grammar and relevant keywords")
    education: list[EducationItem] = Field(description="Education entries")
    languages: list[LanguageItem] = Field(default_factory=list, description="Language proficiencies")

class StructuredCV(TailoredCV):
    raw_text: str = Field(description="Full original text extracted from the CV. Do not modify.")