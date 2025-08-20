from marrs.graph.supervisor import SupervisorGraph
from marrs.utils.model_loader import model_loader

def main():
    llm = model_loader()
    supervisor_graph = SupervisorGraph(llm)
    
    