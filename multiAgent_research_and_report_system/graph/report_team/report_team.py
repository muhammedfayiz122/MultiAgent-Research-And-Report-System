from multiAgent_research_and_report_system.src.supervisor_util import make_supervisor_node
from multiAgent_research_and_report_system.utils.model_loader import model_loader
from multiAgent_research_and_report_system.graph.report_team.inner_nodes.document_summarizer_node import summary_node
from multiAgent_research_and_report_system.graph.report_team.inner_nodes.document_generator_node import doc_generator_node
from langgraph.graph import StateGraph, START
from multiAgent_research_and_report_system.src.agent_state import State

def getReportTeamNode():
    """
    Get the report team node, which includes the document generator and summarizer nodes.
    """
    llm = model_loader()
    generator_supervisor_node = make_supervisor_node(llm, ["summarizer", "doc_generator"])
    return generator_supervisor_node

def getReportTeamGraph():
    """
    Get the report team graph, which includes the document generator and summarizer nodes.
    """
    report_team_node = getReportTeamNode()
    
    # Graph
    generator_builder = StateGraph(State)
    generator_builder.add_node("generator_supervisor", report_team_node)
    generator_builder.add_node("summarizer", summary_node)
    generator_builder.add_node("doc_generator", doc_generator_node)
    generator_builder.add_edge(START, "generator_supervisor")
    report_team_graph = generator_builder.compile()
    return report_team_graph