from ..graph_implements import debug_graph
from langgraph.graph import START, END
from ..orchestrator.planning_orchestrator import *

debug_graph.add_edge(START,"debug_palnning_agent_node")
debug_graph.add_edge("debug_palnning_agent_node","debug_code_agent_node")
debug_graph.add_edge("debug_code_agent_node","debug_rewrite_agent_node")
debug_graph.add_edge("debug_rewrite_agent_node",END)