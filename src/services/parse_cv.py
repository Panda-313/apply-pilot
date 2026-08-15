from pathlib import Path
from typing import cast

from docx import Document
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config import CV_PATH, BASE_NODE_MODEL, CV_PROMPT
from src.models.structured_cv import StructuredCV
from src.utils import ensure_api_key

load_dotenv()

def parse_cv(cv_path: Path) -> StructuredCV:
    ensure_api_key()

    doc = Document(str(cv_path))
    text = "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
    )


    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)
    structured_llm = llm.with_structured_output(StructuredCV)

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=CV_PROMPT),
        HumanMessage(content=f"Extract the structured information from the following CV text:\n\n{text}")
    ])

    result = cast(StructuredCV, structured_llm.invoke(prompt.format_messages()))

    return result


def main() -> int:
    result = parse_cv(CV_PATH)
    print(result)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
