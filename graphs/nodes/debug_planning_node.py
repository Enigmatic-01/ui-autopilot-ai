from ..graph_implements import debug_graph
from ..node_implements.debug_planning_node_implements import *
debug_graph.add_node("debug_palnning_agent_node", deb_palnning_agent)
debug_graph.add_node("debug_rewrite_agent_node", rewrite_agent_node)
debug_graph.add_node("debug_code_agent_node", code_agent_node)