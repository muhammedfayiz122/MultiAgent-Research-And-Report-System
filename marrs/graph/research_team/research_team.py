from typing import Literal, Optional, Annotated

from pydantic import BaseModel
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langchain_core.language_models.chat_models import BaseChatModel

from marrs.src.agent_state import State
from marrs.prompts.prompt import PROMPT_REGISTRY
from marrs.logger.cloud_logger import CustomLogger
from marrs.src.routers import getResearchTeamRouter
from marrs.utils.model_loader import model_loader

from marrs.graph.research_team.inner_nodes.finance_research_node import finance_research_node
from marrs.graph.research_team.inner_nodes.medical_research_node import medical_research_node
 
class ResearchTeam():
    members = ["medical_researcher", "finance_researcher"]
    def __init__(self, llm: BaseChatModel):
        self.log = CustomLogger().get_logger(__name__)
        self.llm = llm
        self.options = self.members + ["FINISH"]
        self.Router = getResearchTeamRouter(self.options)
        self.system_prompt = PROMPT_REGISTRY["research_supervisor"].format(members=", ".join(self.members))

    def research_team_node(self, state: State) -> Command[Literal[*members, "__end__"]]: #type: ignore
        """An LLM-based router."""
        message_count = len(state["messages"])
        messages = [
            {"role": "system", "content": self.system_prompt},
        ] + state["messages"]
        response = self.llm.with_structured_output(self.Router).invoke(messages)
        self.log.info(f"Research supervisor response: {response}")
        print(f"from research team: \n{response}")
        goto = response["next"] #type: ignore
        if goto == "FINISH":
            goto = END
        elif message_count > 1:
            self.log.warning(f"Forced termination to stop looping")
            print("Forced termination to stop looping")
            goto = END
        command = Command(goto=goto, update={"next": goto})
        print(f"Command to go to: {command}")
        return command


    def getResearchTeamGraph(self):
        """
        Get the research team.
        """

        # Build Research Team Graph
        research_builder = StateGraph(State)
        research_builder.add_node("research_supervisor", self.research_team_node)
        research_builder.add_node("medical_researcher", medical_research_node)
        research_builder.add_node("finance_researcher", finance_research_node)
        research_builder.add_edge(START, "research_supervisor")
        research_graph = research_builder.compile()
        return research_graph

if __name__ == "__main__":
    from marrs.utils.model_loader import model_loader
    llm = model_loader()
    research_graph = ResearchTeam(llm).getResearchTeamGraph()
    for message in research_graph.stream(
        {"messages": [("user", "is indian gdp rising")]}, #type: ignore
        {"recursion_limit": 100}
    ):
        print(message)