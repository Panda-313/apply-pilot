from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from config import BASE_NODE_MODEL
from models import FetchJobSuccess
from models.structured_offer import StructuredOffer
from services import fetch_job
from utils import ensure_api_key

load_dotenv()

def parse_offer(offer: FetchJobSuccess):
    ensure_api_key()

    llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0)
    structured_llm = llm.with_structured_output(StructuredOffer)

    
    structured_offer = structured_llm.invoke(offer)

if __name__ == "__main__":
    exit(parse_offer(fetch_job('https://nofluffjobs.com/job/senior-java-cloud-developer-azure-dahliamatic-warszawa-1')))
