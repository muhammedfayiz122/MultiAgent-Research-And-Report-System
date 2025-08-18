
from multiAgent_research_and_report_system.prompts.prompt import PROMPT_REGISTRY
from multiAgent_research_and_report_system.tools.file_tool import read_file
from multiAgent_research_and_report_system.tools.summary_tool import create_summary
from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent
from multiAgent_research_and_report_system.utils.model_loader import model_loader
from multiAgent_research_and_report_system.src.agent_state import State



def getDocumentSummarizerAgent():
    summarizer_prompt = PROMPT_REGISTRY["summarizer"]
    llm = model_loader()
    summarizer_agent = create_react_agent(
        llm,
        tools=[create_summary, read_file],
        prompt=summarizer_prompt
    )
    return summarizer_agent

def summary_node(state: State) -> Command[Literal["generator_supervisor"]]:
    summarizer_agent = getDocumentSummarizerAgent()
    result = summarizer_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="summarizer")
            ]
        },
        goto="generator_supervisor",
    )