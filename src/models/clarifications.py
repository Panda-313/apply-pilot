from typing import Literal

from pydantic import BaseModel, Field


class SkillYears(BaseModel):
    skill: str = Field(description="Technology or skill name")
    years: float = Field(description="Confirmed years of experience")

class ConfirmedAddition(BaseModel):
    gap: str = Field(description="The missing skill or experience from fit_gaps")
    where: str = Field(description="Where in the existing experience this should be added")
    how_to_phrase: str = Field(description="How the candidate wants this described in the CV")

class LanguageSkill(BaseModel):
    language: str = Field(description="Language name (e.g., Polish, English)")
    level: str = Field(description="Proficiency level (e.g., native, fluent, B2, C1)")


class Clarifications(BaseModel):
    style: Literal["conservative", "polished", "strong_rewrite"] = Field(
        description="How aggressive the CV rewrite should be"
    )
    skill_years: list[SkillYears] = Field(
        default_factory=list,
        description="Confirmed years of experience per skill"
    )
    confirmed_additions: list[ConfirmedAddition] = Field(
        default_factory=list,
        description="Gaps the candidate confirmed as real experience to add"
    )
    rejected_gaps: list[str] = Field(
        default_factory=list,
        description="Gaps the candidate said they do not have"
    )
    rewrite_permission: bool = Field(
        description="Whether existing bullets/summary may be rewritten"
    )
    languages: list[LanguageSkill] = Field(
        default_factory=list,
        description="Confirmed language proficiencies"
    )