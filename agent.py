from nodes import *
from edges import *
from agent_graph import agent_graph

agent = agent_graph.compile()

res = agent.invoke({"goal": """ 
Create a blogging website
"""})

