from states import *
from langgraph.types import Send

def architect_orchestrator_node(state: AgentState):
    return [
        Send(
            "architect_agent_node",
            {
                "page": page.model_dump()
            }
        )
        for page in state["project_overview"].pages
    ]