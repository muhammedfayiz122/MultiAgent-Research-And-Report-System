
from typing import Literal, Callable
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END
from langgraph.types import Command
from typing_extensions import TypedDict
from multiAgent_research_and_report_system.src.agent_state import State


def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> Callable:
    options = ["FINISH"] + members
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        f" following workers: {members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When finished,"
        " respond with FINISH."
    )
    
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