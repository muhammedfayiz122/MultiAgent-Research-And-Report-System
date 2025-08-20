from marrs.utils.model_loader import model_loader
from marrs.graph.research_team.research_team import getResearchTeamGraph
from marrs.graph.report_team.report_team import getReportTeamGraph
from langgraph.graph import StateGraph, START, END
from marrs.utils.agent_state import State
from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from marrs.utils.model_loader import model_loader
from marrs.utils.agent_state import State
from typing import Literal, Callable
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.types import Command
from typing_extensions import TypedDict
from marrs.utils.agent_state import State
from marrs.prompts.prompt import PROMPT_REGISTRY
from marrs.logger.cloud_logger import CustomLogger

log = CustomLogger().get_logger(__name__)

llm = model_loader()

def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> Callable:
    options = ["FINISH"] + members
    system_prompt = PROMPT_REGISTRY["main_supervisor"].format(members=", ".join(members))
    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""
        next: Literal[*options] #type: ignore

    def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]: #type: ignore
        """An LLM-based router."""
        message_count = len(state["messages"])
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        log.info(f"Supervisor response: {response}")
        print(f"from supervisor: \n{response}")
        goto = response["next"] #type: ignore
        last_message = str(state["messages"][-1].content).lower()
        if goto == "FINISH" or last_message.endswith("finish."):
            goto = END
            log.info(f"Overall state is : {state}")
        elif message_count > 1 and goto == members[0]:
            log.warning(f"Forced handoff to stop looping")
            print("Forced handoff to stop looping")
            goto = members[1]
        return Command(goto=goto, update={"next": goto})
    
    return supervisor_node

def getSupervisorNode():
    """
    Get the supervisor node .
    """
    # llm = model_loader()
    supervisor_node = make_supervisor_node(llm, ["research_supervisor", "report_supervisor"])
    return supervisor_node

def callResearchTeam(state: State) -> Command[Literal["supervisor"]]:
    """
    Call the research team and return results to supervisor.
    """
    research_graph = getResearchTeamGraph(llm)
    response = research_graph.invoke({"messages": state["messages"]}) #type: ignore
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response["messages"][-1].content, 
                    name="research_supervisor"
                )
            ]
        },
        goto="supervisor",
    )
    
def callReportTeam(state: State) -> Command[Literal["supervisor"]]:
    """
    Call the report team and return results to main supervisor.
    """
    report_graph = getReportTeamGraph(llm)

    # Invoke the report team graph
    response = report_graph.invoke(
        {"messages": state["messages"]}, #type: ignore
        {"recursion_limit": 20}
    )

    # Extract the last message
    message = str(response["messages"][-1].content)
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=message, 
                    name="report_supervisor"
                )
            ]
        },
        goto="supervisor",
    )

def getSupervisorGraph():
    """
    Get the supervisor graph which includes the research and report teams.
    """
    # Get the supervisor node.
    supervisor_node = getSupervisorNode()

    # Combine the graphs
    supervisor_graph_builder = StateGraph(State)
    supervisor_graph_builder.add_node("supervisor", supervisor_node)
    supervisor_graph_builder.add_node("research_supervisor", callResearchTeam)
    supervisor_graph_builder.add_node("report_supervisor", callReportTeam)
    supervisor_graph_builder.add_edge(START, "supervisor")
    supervisor_graph = supervisor_graph_builder.compile()
    return supervisor_graph

if __name__ == "__main__":
    supervisor_graph = getSupervisorGraph()
    result = supervisor_graph.invoke({"messages": ["What is the current state of the Indian economy?"]}) #type: ignore
    print(result)