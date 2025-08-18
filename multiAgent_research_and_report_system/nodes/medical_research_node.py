from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from langgraph.prebuilt import create_react_agent
from multiAgent_research_and_report_system.tools.search_tool import enhanced_search
from multiAgent_research_and_report_system.utils.model_loader import model_loader



def medical_research_node(state: State) -> Command[Literal["research_supervisor"]]:
    llm = model_loader()
    # Medical/Pharma Research Agent
    medical_research_agent = create_react_agent(
        llm, 
        tools=[enhanced_search],
        prompt="You are a medical and pharmaceutical research specialist. Use the enhanced_search tool to find the most current and real-time information on medical, healthcare, pharmaceutical, and biotech topics. Focus on recent developments, breaking news, clinical studies, regulatory updates, and industry trends. Provide detailed research on health-related queries with emphasis on current data."
    )
    
    result = medical_research_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="medical_researcher")
            ]
        },
        goto="research_supervisor",
    )