
from typing import TypedDict, Literal

def getSupervisorRouter(options: list[str]):
    class SupervisorRouter(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""
        next: Literal[*options] #type: ignore
    return SupervisorRouter
