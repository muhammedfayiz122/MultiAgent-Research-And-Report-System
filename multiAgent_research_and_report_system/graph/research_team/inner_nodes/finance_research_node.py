from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from langgraph.prebuilt import create_react_agent
from multiAgent_research_and_report_system.prompts import prompt
from multiAgent_research_and_report_system.tools.search_tool import enhanced_search
from multiAgent_research_and_report_system.utils.model_loader import model_loader
from multiAgent_research_and_report_system.src.agent_state import State

def getFinanceResearchAgent():
    """
    Get a finance research agent.
    """
    llm = model_loader()
    finance_research_prompt = prompt.PROMPT_REGISTRY["finance_research"]
    
    finance_research_agent = create_react_agent(
        llm,
        tools=[enhanced_search],
        prompt=finance_research_prompt
    )
    return finance_research_agent

def finance_research_node(state: State) -> Command[Literal["research_supervisor"]]:
    finance_research_agent = getFinanceResearchAgent()
    result = finance_research_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="finance_researcher")
            ]
        },
        goto="research_supervisor",
    )