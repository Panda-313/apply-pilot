from typing import cast

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from src.config import COMPANY_RESEARCH_PROMPT, BASE_NODE_MODEL
from src.graph.nodes.company_research import CompanyResearchResult
from src.graph.nodes.company_research.agents import company_researcher_agent
from src.state_updates import CompanyResearchUpdate
from src import State

def company_research_node(state: State) -> CompanyResearchUpdate:
    company_name = state["offer"].company_name
    offer_description = state["offer"].description

    research_query = COMPANY_RESEARCH_PROMPT.format(
        company_name=company_name,
        offer_description=offer_description
    )

    agent_result = company_researcher_agent.invoke({
        "messages": [HumanMessage(content=research_query)]
    })

    final_message = agent_result["messages"][-1].content
    structured_llm = ChatOpenAI(model=BASE_NODE_MODEL, temperature=0).with_structured_output(CompanyResearchResult)
    structured_result = cast(CompanyResearchResult, structured_llm.invoke(
        f"Extract the company research result from this text:\n\n{final_message}"
    ))

    return {
        "company_name": structured_result.company_name,
        "company_type": structured_result.company_type,
        "company_summary": structured_result.company_summary,
        "status": "company_researched",
    }