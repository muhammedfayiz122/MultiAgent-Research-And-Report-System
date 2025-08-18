from multiAgent_research_and_report_system.src.supervisor_util import make_supervisor_node
from multiAgent_research_and_report_system.utils.model_loader import model_loader
from multiAgent_research_and_report_system.graph.research_team.research_team import getResearchTeamGraph
from multiAgent_research_and_report_system.graph.report_team.report_team import getReportTeamGraph
from langgraph.graph import StateGraph, START, END
from multiAgent_research_and_report_system.src.agent_state import State
from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from multiAgent_research_and_report_system.utils.model_loader import model_loader
from multiAgent_research_and_report_system.src.agent_state import State
from typing import Literal, Callable
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.types import Command
from typing_extensions import TypedDict
from multiAgent_research_and_report_system.src.agent_state import State
from multiAgent_research_and_report_system.prompts.prompt import PROMPT_REGISTRY

llm = model_loader()

def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> Callable:
    options = ["FINISH"] + members
    system_prompt = PROMPT_REGISTRY["main_supervisor"].format(members=", ".join(members))
    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""
        next: Literal[*options] #type: ignore

    def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]: #type: ignore
        """An LLM-based router."""
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"] #type: ignore
        if goto == "FINISH":
            goto = END
        return Command(goto=goto, update={"next": goto})
    
    return supervisor_node

def getSupervisorNode():
    # llm = model_loader()
    supervisor_node = make_supervisor_node(llm, ["research_team", "report_team"])
    return supervisor_node

def callResearchTeam(state: State) -> Command[Literal["supervisor"]]:
    """Call the research team and return results to supervisor."""
    research_graph = getResearchTeamGraph(llm)
    response = research_graph.invoke({"messages": state["messages"]}) #type: ignore
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
    report_graph = getReportTeamGraph(llm)
    response = report_graph.invoke({"messages": state["messages"]}) #type: ignore
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
    # llm = model_loader()
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
    result = supervisor_graph.invoke({"messages": ["What is the current state of the Indian economy?"]}) #type: ignore
    print(result)