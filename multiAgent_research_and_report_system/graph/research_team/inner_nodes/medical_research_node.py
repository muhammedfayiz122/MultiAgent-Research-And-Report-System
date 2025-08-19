from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from langgraph.prebuilt import create_react_agent
from multiAgent_research_and_report_system.prompts import prompt
from multiAgent_research_and_report_system.tools.file_tool import write_file
from multiAgent_research_and_report_system.tools.search_tool import enhanced_search
from multiAgent_research_and_report_system.utils.model_loader import model_loader
from multiAgent_research_and_report_system.src.agent_state import State
from multiAgent_research_and_report_system.logger.cloud_logger import CustomLogger

llm = model_loader()
log = CustomLogger().get_logger(__name__)

def getMedicalResearchAgent():
    """
    Get a medical research agent.
    """
    # llm = model_loader()
    medical_research_prompt = prompt.PROMPT_REGISTRY["medical_research"]
    medical_research_agent = create_react_agent(
        llm,
        tools=[enhanced_search, write_file],
        prompt=medical_research_prompt,
    )
    return medical_research_agent

def medical_research_node(state: State) -> Command[Literal["research_supervisor"]]:
    medical_research_agent = getMedicalResearchAgent()
    
    result = medical_research_agent.invoke(state)
    
    last_message = result["messages"][-1].content
    print(f"from medical research team result: \n{last_message}")
    log.info(f"from medical research team result: \n{result}")
    return Command(
        update={
            "messages": [
                HumanMessage(content=last_message, name="medical_researcher")
            ]
        },
        goto="research_supervisor",
    )
    

    