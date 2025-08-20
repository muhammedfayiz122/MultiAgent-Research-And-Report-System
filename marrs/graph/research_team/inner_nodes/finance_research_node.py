from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from langgraph.prebuilt import create_react_agent
from marrs.prompts import prompt
from marrs.tools.file_tool import write_file
from marrs.tools.search_tool import enhanced_search
from marrs.utils.model_loader import model_loader
from marrs.utils.agent_state import State
from marrs.logger.cloud_logger import CustomLogger

llm = model_loader()
log = CustomLogger().get_logger(__name__)

def getFinanceResearchAgent():
    """
    Get a finance research agent.
    """
    # llm = model_loader()
    finance_research_prompt = prompt.PROMPT_REGISTRY["finance_research"]
    
    finance_research_agent = create_react_agent(
        llm,
        tools=[enhanced_search, write_file],
        prompt=finance_research_prompt
    )
    return finance_research_agent

def finance_research_node(state: State) -> Command[Literal["research_supervisor"]]:
    finance_research_agent = getFinanceResearchAgent()
    result = finance_research_agent.invoke(state)
    last_message = result["messages"][-1].content
    print(f"from finance research team result: \n{last_message}")
    log.info(f"from finance research team result: \n{result}")
    return Command(
        update={
            "messages": [
                HumanMessage(content=last_message, name="finance_researcher")
            ]
        },
        goto="research_supervisor",
    )