from multiAgent_research_and_report_system.graph.research_team.inner_nodes.finance_research_node import finance_research_node
from multiAgent_research_and_report_system.graph.research_team.inner_nodes.medical_research_node import medical_research_node 
from langgraph.graph import StateGraph, START, END
from multiAgent_research_and_report_system.utils.agent_state import State
from multiAgent_research_and_report_system.logger.cloud_logger import CustomLogger


from typing import Literal, Callable, Optional, Annotated
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.types import Command
from typing_extensions import TypedDict
from multiAgent_research_and_report_system.prompts.prompt import PROMPT_REGISTRY

log = CustomLogger().get_logger(__name__)

def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> Callable:
    options = ["FINISH"] + members
    system_prompt = PROMPT_REGISTRY["research_supervisor"].format(members=", ".join(members))
    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""
        next: Literal[*options] #type: ignore
        task: Annotated[Optional[str], "Task to be performed by the next worker"]

    def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]: #type: ignore
        """An LLM-based router."""
        message_count = len(state["messages"])
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        log.info(f"Research supervisor response: {response}")
        print(f"from research team: \n{response}")
        goto = response["next"] #type: ignore
        if goto == "FINISH":
            goto = END
        elif message_count > 1:
            log.warning(f"Forced termination to stop looping")
            print("Forced termination to stop looping")
            goto = END
        command = Command(goto=goto, update={"next": goto})
        print(f"Command to go to: {command}")
        return command
    
    return supervisor_node

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