from agent_graph import agent_graph
from graphs.graph_complies import *
from orchestrator import *
from agents_nodes import *
agent_graph.add_node("planning_agent",planning_agent)
agent_graph.add_node("coding_agent",coding_agent)
agent_graph.add_node("file_management_agent",file_management_agent)
agent_graph.add_node("testing_agent",testing_agent)
agent_graph.add_node("debugging_agent",debug_agent)
agent_graph.add_node("enhance_prompt_agent",enhance_prompt)