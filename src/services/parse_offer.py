from typing import cast

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config import BASE_NODE_MODEL, PARSE_OFFER_PROMPT
from src.models import FetchJobSuccess
from src.models.structured_offer import StructuredOffer
from src.services import fetch_job
from src.utils import ensure_api_key

load_dotenv()

def parse_offer(offer: FetchJobSuccess) -> StructuredOffer:
    ensure_api_key()

    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)
    structured_llm = llm.with_structured_output(StructuredOffer)

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=PARSE_OFFER_PROMPT),
        HumanMessage(content=f"Offer title: {offer['title']} \n\nExtract the structured information from the following job offer text: {offer['cleaned_text']}")
    ])

    structured_offer = cast(StructuredOffer,structured_llm.invoke(prompt.format_messages()))

    return structured_offer

def main() -> int:
    parse_offer(fetch_job('https://nofluffjobs.com/job/senior-java-cloud-developer-azure-dahliamatic-warszawa-1'))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
