from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun

from src.config import BASE_NODE_MODEL

ddg_tool = DuckDuckGoSearchRun()

system_prompt = (
    "You are a company research specialist. "
    "Your job is to research the given company and determine whether it is "
    "a product company, an outsourcing/software house, or unknown. "
    "Use tools when needed. Be factual and concise."
)

company_researcher_agent = create_agent(
    model=BASE_NODE_MODEL,
    tools=[ddg_tool],
    system_prompt=system_prompt,
)
