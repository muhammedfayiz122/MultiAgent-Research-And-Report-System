from typing import Literal, Callable

from pydantic import BaseModel

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langchain_core.messages import HumanMessage

from marrs.utils.model_loader import model_loader
from marrs.src.agent_state import State
from marrs.prompts.prompt import PROMPT_REGISTRY
from marrs.logger.cloud_logger import CustomLogger
from marrs.graph.research_team.research_team import getResearchTeamGraph
from marrs.graph.report_team.report_team import getReportTeamGraph
from marrs.src.routers import getSupervisorRouter

class Router(BaseModel):
    next: Literal[*(["FINISH"] + self.members)]  # type: ignore

class SupervisorGraph:
    def __init__(self):
        self.log = CustomLogger().get_logger(__name__)
        self.llm = model_loader()
        self.members = ["research_supervisor", "report_supervisor"]
        self.options = self.members + ["FINISH"]
        self.system_prompt = PROMPT_REGISTRY["main_supervisor"].format(
            members=", ".join(self.members)
        )
        self.router = getSupervisorRouter(self.options)

    def supervisor_node(self, state: State) -> Command[Literal[*members, "__end__"]]: #type: ignore
        """
        Supervisor node for the state graph.
        
        This node:
        - Receives messages from the user.
        - Routes the messages to the appropriate team (research or report).
        - Returns the response from the team back to the user.

        args:
            state (State): The current state of the conversation.

        returns:
            Command[Literal[*members, "__end__"]]: The command to execute next.
        """
        # Prepare messages for the LLM
        messages = [
            {"role": "system", "content": self.system_prompt},
        ] + state["messages"]

        # Invoke the LLM
        response = self.llm.with_structured_output(Router).invoke(messages)
        self.log.info(f"Supervisor response: {response}")
        print(f"from supervisor: \n{response}")

        # Determine the next node to go to
        goto = response["next"] #type: ignore

        # Determine the last message and state message count
        last_message = str(state["messages"][-1].content).lower()
        state_message_count = len(state["messages"])

        # Determine if we need to finish or handoff
        if goto == "FINISH" or last_message.endswith("finish."):
            goto = END
            self.log.info(f"Overall state is : {state}")
        elif state_message_count > 1 and goto == self.members[0]:
            self.log.warning(f"Forced handoff to stop looping")
            print("Forced handoff to stop looping")
            goto = self.members[1]
            
        return Command(goto=goto, update={"next": goto})


    def callResearchTeam(self, state: State) -> Command[Literal["supervisor"]]:
        """
        Call the research team and return results to supervisor.

        Args:
            state (State): The current state of the conversation.
            
        Returns:
            Command[Literal["supervisor"]]: The command to go back to the supervisor.
        """
        research_graph = getResearchTeamGraph(self.llm)
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
        
    def callReportTeam(self, state: State) -> Command[Literal["supervisor"]]:
        """
        Call the report team and return results to main supervisor.
        
        Args:
            state (State): The current state of the conversation.

        Returns:
            Command[Literal["supervisor"]]: The command to go back to the supervisor.
        """
        report_graph = getReportTeamGraph(self.llm)

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

    def getSupervisorGraph(self):
        """
        Get the supervisor graph which includes the research and report teams.
        """
        # Combine the graphs
        graph_builder = StateGraph(State)
        graph_builder.add_node("supervisor", self.supervisor_node)
        graph_builder.add_node("research_supervisor", self.callResearchTeam)
        graph_builder.add_node("report_supervisor", self.callReportTeam)
        graph_builder.add_edge(START, "supervisor")
        supervisor_graph = graph_builder.compile()
        return supervisor_graph

if __name__ == "__main__":
    supervisor_graph = SupervisorGraph().getSupervisorGraph()
    result = supervisor_graph.invoke({"messages": ["What is the current state of the Indian economy?"]}) #type: ignore
    print(result)