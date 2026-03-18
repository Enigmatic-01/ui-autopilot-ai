from ..graph_implements import planning_graph
from langgraph.graph import START, END
from ..orchestrator.planning_orchestrator import *

planning_graph.add_edge(START, "overview_agent_node")


planning_graph.add_conditional_edges("overview_agent_node", architect_orchestrator_node,["architect_agent_node"])

planning_graph.add_edge("architect_agent_node",END)