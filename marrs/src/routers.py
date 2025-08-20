
from typing import TypedDict, Literal, Annotated, Optional
from pydantic import BaseModel

def getSupervisorRouter(options: list[str]):
    class SupervisorRouter(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""
        next: Literal[*options] #type: ignore
    return SupervisorRouter

def getReportTeamRouter(options: list[str]):
    class ReportTeamRouter(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""
        next: Literal[*options] #type: ignore
        task: Annotated[Optional[str], "Task to be performed by the next worker"]
    return ReportTeamRouter

def getResearchTeamRouter(options: list[str]):
    class ResearchTeamRouter(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""
        next: Literal[*options] #type: ignore
        task: Annotated[Optional[str], "Task to be performed by the next worker"]
    return ResearchTeamRouter
