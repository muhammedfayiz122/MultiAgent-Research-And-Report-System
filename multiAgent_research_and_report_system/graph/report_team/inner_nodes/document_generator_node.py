from multiAgent_research_and_report_system.prompts.prompt import PROMPT_REGISTRY
from multiAgent_research_and_report_system.tools.document_tool import create_document
from multiAgent_research_and_report_system.tools.file_tool import read_file
from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent
from multiAgent_research_and_report_system.utils.model_loader import model_loader
from multiAgent_research_and_report_system.src.agent_state import State

def getDocumentGeneratorAgent():
    llm = model_loader()
    doc_generator_agent = create_react_agent(
        llm,
        tools=[create_document, read_file],
        prompt="You are a document generator. Read summary files using read_file tool, then create comprehensive documents and ALWAYS save them using the create_document tool with an appropriate filename."
    )
    return doc_generator_agent


def doc_generator_node(state: State) -> Command[Literal["generator_supervisor"]]:
    doc_generator_agent = getDocumentGeneratorAgent()
    result = doc_generator_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="doc_generator")
            ]
        },
        goto="generator_supervisor",
    )