from agent_graph import agent_graph
from langgraph.graph import START,END
from nodes import *
from orchestrator import * 

agent_graph.add_edge(START,"planning_agent")


agent_graph.add_conditional_edges("planning_agent",
            code_orchestrater_agent,
            ["coding_agent"])



agent_graph.add_conditional_edges(
    "coding_agent",
    file_orchestrater_agent,
    ["file_management_agent"]
)

agent_graph.add_edge("file_management_agent","testing_agent")
agent_graph.add_conditional_edges("testing_agent",
                                  debug_orchestrater_agent,
                                  {"debug":"debugging_agent",
                                   "END":END
                                   })
agent_graph.add_edge("debugging_agent","testing_agent")
