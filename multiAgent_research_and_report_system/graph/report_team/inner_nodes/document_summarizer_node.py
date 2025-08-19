
from multiAgent_research_and_report_system.prompts.prompt import PROMPT_REGISTRY
from multiAgent_research_and_report_system.tools.file_tool import read_file
from multiAgent_research_and_report_system.tools.file_tool import read_file, write_file
from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent
from multiAgent_research_and_report_system.utils.model_loader import model_loader
from multiAgent_research_and_report_system.utils.agent_state import State
from multiAgent_research_and_report_system.logger.cloud_logger import CustomLogger

log = CustomLogger().get_logger(__name__)

llm = model_loader()

def getDocumentSummarizerAgent():
    summarizer_prompt = PROMPT_REGISTRY["summarizer"]
    # llm = model_loader()
    summarizer_agent = create_react_agent(
        llm,
        tools=[read_file, write_file],
        prompt=summarizer_prompt,
    )
    return summarizer_agent

def summary_node(state: State) -> Command[Literal["report_supervisor"]]:
    print("<------inside summary agent----->")
    summarizer_agent = getDocumentSummarizerAgent()
    result = summarizer_agent.invoke(state)
    print(f"from summary team result: \n{result}")
    log.info(f"from summary team result: \n{result}")
    output = result["messages"][-1].content
    output += "Now, you should immediately call the Doc_Generator."
    return Command(
        update={
            "messages": [
                HumanMessage(content=output, name="summarizer")
            ]
        },
        goto="report_supervisor",
    )