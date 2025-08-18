from multiAgent_research_and_report_system.src.supervisor_util import make_supervisor_node
from multiAgent_research_and_report_system.utils.model_loader import model_loader
from multiAgent_research_and_report_system.graph.research_team.research_team import getResearchTeamGraph
from multiAgent_research_and_report_system.graph.report_team.report_team import getReportTeamGraph
from langgraph.graph import StateGraph, START
from multiAgent_research_and_report_system.src.agent_state import State

def getSupervisorNode():
    llm = model_loader()
    supervisor_node = make_supervisor_node(llm, ["research_team", "generator_team"])
    return supervisor_node

def getSupervisorGraph():
    llm = model_loader()
    supervisor_node = getSupervisorNode()
    research_graph = getResearchTeamGraph()
    report_graph = getReportTeamGraph()

    # Combine the graphs
    supervisor_graph = StateGraph(State)
    supervisor_graph.add_node("supervisor", supervisor_node)
    supervisor_graph.add_node("research_team", research_graph)
    supervisor_graph.add_node("report_team", report_graph)
    supervisor_graph.add_edge(START, "supervisor")
    supervisor_graph.compile()
    return supervisor_graph