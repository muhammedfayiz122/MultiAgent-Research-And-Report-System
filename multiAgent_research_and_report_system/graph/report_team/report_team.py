from multiAgent_research_and_report_system.src.supervisor_util import make_supervisor_node

from multiAgent_research_and_report_system.graph.report_team.inner_nodes.document_summarizer_node import summary_node
from multiAgent_research_and_report_system.graph.report_team.inner_nodes.document_generator_node import doc_generator_node
from langgraph.graph import StateGraph, START, END
from multiAgent_research_and_report_system.utils.agent_state import State
from typing import Literal, Callable
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.types import Command
from typing_extensions import TypedDict
from multiAgent_research_and_report_system.utils.agent_state import State
from multiAgent_research_and_report_system.prompts.prompt import PROMPT_REGISTRY
from typing import Annotated, Optional
from multiAgent_research_and_report_system.logger.cloud_logger import CustomLogger

log = CustomLogger().get_logger(__name__)

def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> Callable:
    options = ["FINISH"] + members
    system_prompt = PROMPT_REGISTRY["report_supervisor"].format(members=", ".join(members))
    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""
        next: Literal[*options] #type: ignore
        task: Annotated[Optional[str], "Task to be performed by the next worker"]

    def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]: #type: ignore
        """An LLM-based router."""
        print("<------inside Report team----->")
        last_message = str(state["messages"][-1].content).lower()
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"] #type: ignore
        
        print(f"from report team: \n{response}")
        log.info(f"from report team: \n{response}")
        
        if goto == "FINISH" or last_message.endswith("finish."):
            goto = END
            return Command(goto=goto, update={
                "next": goto,
                "current": "Research_supervisor"
            })
        elif last_message.endswith("doc_generator."):
            goto = "doc_generator"
            
        if hasattr(response, "task"):
            # print(f"Task for next worker: {response['task']}")
            return Command(goto=goto, update={
                "next": goto,
                "task": response.get("task", None) # type: ignore
            })
        return Command(goto=goto, update={
            "next": goto
        })

    return supervisor_node

def getReportTeamNode(llm):
    """
    Get the report team node, which includes the document generator and summarizer nodes.
    """
    # llm = model_loader()
    generator_supervisor_node = make_supervisor_node(llm, ["summarizer", "doc_generator"])
    return generator_supervisor_node

def getReportTeamGraph(llm):
    """
    Get the report team graph, which includes the document generator and summarizer nodes.
    """
    report_team_node = getReportTeamNode(llm)
    
    # Graph
    generator_builder = StateGraph(State)
    generator_builder.add_node("report_supervisor", report_team_node)
    generator_builder.add_node("summarizer", summary_node)
    generator_builder.add_node("doc_generator", doc_generator_node)
    generator_builder.add_edge(START, "report_supervisor")
    report_team_graph = generator_builder.compile()
    return report_team_graph

if __name__ == "__main__":
    from multiAgent_research_and_report_system.utils.model_loader import model_loader
    llm = model_loader()
    report_graph = getReportTeamGraph(llm)
    query = """
    ["HumanMessage(content=\"### Market Snapshot:\\n- **GDP Growth Rate**: India's GDP growth rate for the fiscal year 2025 is reported at 6.5%, driven by strong private consumption and investments. (Source: Deloitte)\\n- **Sector Contribution**: The services sector dominates the economy, contributing 54.7%, followed by industry at 27.6% and agriculture at 17.7%. (Source: Wikipedia)\\n- **Recent Quarter Growth**: The Indian GDP expanded by 5.4% in the September quarter of 2024, down from 6.7% in the previous quarter. (Source: Trading Economics)\\n\\n### Key Financial Events:\\n- **GDP Growth Projection**: The Reserve Bank of India (RBI) projects a growth rate of 6.5% for FY26, indicating continued economic expansion. (Source: IBEF)\\n- **Inflation Rate**: The average consumer price inflation rate is 4.2%, reflecting controlled price levels. (Source: IMF)\\n\\n### Data & Sources (with timestamps):\\n1. **Deloitte**: India's GDP growth for FY25 is 6.5%, supported by domestic demand and easing inflation. (Recent)\\n2. **World Bank Data**: Confirms India's GDP growth rate of 6.5%. (Recent)\\n3. **Trading Economics**: Reports a 5.4% GDP growth in Q3 2024. (Recent)\\n4. **IMF DataMapper**: Provides detailed metrics including real GDP growth and per capita growth. (Recent)\\n5. **Wikipedia**: Sector-wise contribution to GDP. (Recent)\\n6. **IBEF**: Projects 6.5% growth for FY26. (Recent)\\n7. **World Bank**: GDP and per capita growth figures. (Recent)\\n8. **IMF**: Real GDP growth and inflation rates. (Recent)\\n\\n### Investment/Business Implications:\\n- **Positive Outlook**: The consistent GDP growth rate and controlled inflation suggest a stable economic environment, making India an attractive destination for investments.\\n- **Sector Opportunities**: The dominance of the services sector, coupled with contributions from industry and agriculture, presents diverse investment opportunities across sectors.\\n- **Consumer Demand**: Strong private consumption and investments indicate resilient domestic demand, favorable for businesses and investors.\\n\\nOverall, the Indian economy is showing signs of steady growth, supported by strong domestic demand and a stable inflation environment, making it an attractive market for investors and businesses.\", additional_kwargs={}, response_metadata={}, name='research_team', id='ac3e2805-99bb-41af-9c17-cd2a5b01e7c4')"]
    """
    for message in report_graph.stream({"messages": [("user", query)]}, {"recursion_limit": 20}): #type: ignore
        print(message)
        
    # python -m multiAgent_research_and_report_system.graph.report_team.report_team