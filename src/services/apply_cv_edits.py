from __future__ import annotations

from pathlib import Path

from docx import Document
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from src.config import (
    APPLY_CV_EDITS_HUMAN_TEMPLATE,
    APPLY_CV_EDITS_SYSTEM_PROMPT,
    BASE_NODE_MODEL,
)
from src.models import TailoredCV
from src.utils import apply_paragraph_changes, extract_paragraphs, format_paragraphs_for_prompt


class ParagraphChange(BaseModel):
    index: int = Field(description="0-based index of the paragraph to change")
    new_text: str = Field(description="Exact new text that should replace the paragraph content")

class ParagraphChanges(BaseModel):
    changes: list[ParagraphChange] = Field(
        description="List of paragraphs that need to be updated. Only include paragraphs that actually require changes."
    )


def apply_cv_edits(
    original_docx_path: str | Path,
    tailored_cv: TailoredCV,
    output_path: str | Path,
) -> Path:
    original_docx_path = Path(original_docx_path)
    output_path = Path(output_path)

    if not original_docx_path.exists():
        raise FileNotFoundError(f"Original CV not found: {original_docx_path}")

    doc = Document(str(original_docx_path))
    paragraphs = extract_paragraphs(doc)

    paragraphs_text = format_paragraphs_for_prompt(paragraphs)

    experience_text = ""
    for exp in tailored_cv.experience:
        experience_text += f"\nCompany: {exp.company} | Title: {exp.title}\n"
        for b in exp.bullets:
            experience_text += f"- {b}\n"

    human_message = APPLY_CV_EDITS_HUMAN_TEMPLATE.format(
        paragraphs_text=paragraphs_text,
        summary=tailored_cv.summary,
        skills=", ".join(tailored_cv.skills),
        experience=experience_text.strip(),
    )

    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)
    structured_llm = llm.with_structured_output(ParagraphChanges)

    result = structured_llm.invoke([
        {"role": "system", "content": APPLY_CV_EDITS_SYSTEM_PROMPT},
        {"role": "user", "content": human_message},
    ])

    apply_paragraph_changes(doc, result.changes)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


if __name__ == "__main__":
    print("LLM-assisted apply_cv_edits service ready.")
    print("Usage: apply_cv_edits(original_path, tailored_cv, output_path)")