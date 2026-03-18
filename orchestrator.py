from multiprocessing import dummy
from turtle import st

from states import *

from langgraph.types import Send


def code_orchestrater_agent(state: AgentState):
    return [
        Send(
            "coding_agent",
            { 
                "step": step
            }
        )
        for step in state["steps"]
    ]
def file_orchestrater_agent(state: AgentState):
    all_files = [f for schema in state["files"] for f in schema.files]

    tasks = []
    for file in all_files:
        tasks.append(
            Send(
                "file_management_agent",
                {
                    "file": file,
                    "all_files": all_files  # pass all files so HTML can fix imports
                }
            )
        )
    return tasks

def debug_orchestrater_agent(state:AgentState):
    if state["testing_result"].passed or state["retry"]>6:
        return "END"
    return "debug"
