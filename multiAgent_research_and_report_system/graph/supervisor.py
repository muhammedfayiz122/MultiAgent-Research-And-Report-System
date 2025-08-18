from multiAgent_research_and_report_system.src.supervisor_util import make_supervisor_node
from multiAgent_research_and_report_system.utils.model_loader import model_loader
from multiAgent_research_and_report_system.graph.research_team.research_team import getResearchTeamGraph
from multiAgent_research_and_report_system.graph.report_team.report_team import getReportTeamGraph
from langgraph.graph import StateGraph, START
from multiAgent_research_and_report_system.src.agent_state import State
from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from multiAgent_research_and_report_system.prompts import prompt
from multiAgent_research_and_report_system.tools.search_tool import enhanced_search
from multiAgent_research_and_report_system.utils.model_loader import model_loader
from multiAgent_research_and_report_system.src.agent_state import State

def getSupervisorNode():
    llm = model_loader()
    supervisor_node = make_supervisor_node(llm, ["research_team", "report_team"])
    return supervisor_node

def callResearchTeam(state: State) -> Command[Literal["supervisor"]]:
    """Call the research team and return results to supervisor."""
    research_graph = getResearchTeamGraph()
    response = research_graph.invoke({"messages": state["messages"]})
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response["messages"][-1].content, 
                    name="research_team"
                )
            ]
        },
        goto="supervisor",
    )
    
def callReportTeam(state: State) -> Command[Literal["supervisor"]]:
    """Call the report team and return results to main supervisor."""
    report_graph = getReportTeamGraph()
    response = report_graph.invoke({"messages": state["messages"]})
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response["messages"][-1].content, 
                    name="report_team"
                )
            ]
        },
        goto="supervisor",
    )

def getSupervisorGraph():
    llm = model_loader()
    supervisor_node = getSupervisorNode()

    # Combine the graphs
    supervisor_graph_builder = StateGraph(State)
    supervisor_graph_builder.add_node("supervisor", supervisor_node)
    supervisor_graph_builder.add_node("research_team", callResearchTeam)
    supervisor_graph_builder.add_node("report_team", callReportTeam)
    supervisor_graph_builder.add_edge(START, "supervisor")
    supervisor_graph = supervisor_graph_builder.compile()
    return supervisor_graph

if __name__ == "__main__":
    supervisor_graph = getSupervisorGraph()
    result = supervisor_graph.invoke({"messages": ["What is the current state of the Indian economy?"]})
    print(result)