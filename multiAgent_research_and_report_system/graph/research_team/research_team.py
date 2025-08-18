from multiAgent_research_and_report_system.src.supervisor_util import make_supervisor_node

from multiAgent_research_and_report_system.graph.research_team.inner_nodes.finance_research_node import finance_research_node
from multiAgent_research_and_report_system.graph.research_team.inner_nodes.medical_research_node import medical_research_node 
from langgraph.graph import StateGraph, START
from multiAgent_research_and_report_system.src.agent_state import State

def getResearchTeamNode(llm):
    """
    Get the research team.
    """
    # llm = model_loader()
    research_supervisor_node = make_supervisor_node(llm, ["medical_researcher", "finance_researcher"])
    return research_supervisor_node

def getResearchTeamGraph(llm):
    """
    Get the research team.
    """
    research_supervisor_node = getResearchTeamNode(llm)

    # Build Research Team Graph
    research_builder = StateGraph(State)
    research_builder.add_node("research_supervisor", research_supervisor_node)
    research_builder.add_node("medical_researcher", medical_research_node)
    research_builder.add_node("finance_researcher", finance_research_node)
    research_builder.add_edge(START, "research_supervisor")
    research_graph = research_builder.compile()
    return research_graph

if __name__ == "__main__":
    from multiAgent_research_and_report_system.utils.model_loader import model_loader
    llm = model_loader()
    research_graph = getResearchTeamGraph(llm)
    for message in research_graph.stream(
        {"messages": [("user", "is indian gdp rising")]}, #type: ignore
        {"recursion_limit": 100}
    ):
        print(message)