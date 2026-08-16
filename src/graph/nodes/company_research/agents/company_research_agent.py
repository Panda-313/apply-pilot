from langchain.agents import create_agent
from langchain.tools import tool

from src.config import BASE_NODE_MODEL


@tool
def web_search(query: str) -> str:
    """Search the web for information about a company."""
    return f"Search results for: {query}"


tools = [web_search]

system_prompt = (
    "You are a company research specialist. "
    "Your job is to research the given company and determine whether it is "
    "a product company, an outsourcing/software house, or unknown. "
    "Use tools when needed. Be factual and concise."
)

company_researcher_agent = create_agent(
    model=BASE_NODE_MODEL,
    tools=tools,
    system_prompt=system_prompt,
)