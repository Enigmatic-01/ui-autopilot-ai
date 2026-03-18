from ..prompts.planning_prompts import OVERVIEW_PROMPT,ARCHITECT_PROMPT
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_core.output_parsers import StrOutputParser
from ..pydantic_models.planning_schemas import ProjectOverviewSchema,DummyPages,PageArchitect
from llms import llm





def overview_agent_node(state: dict) -> dict:
    goal = state["goal"]

    init_msgs = [
        SystemMessage(content=OVERVIEW_PROMPT),
        HumanMessage(content=f"Project Goal:\n{goal}")
    ]

    res = llm.with_structured_output(ProjectOverviewSchema).invoke(init_msgs)

    return {"project_overview": res}


def architect_agent_node(payload: dict) -> dict:
    page = payload["page"]

    messages = [
        SystemMessage(content=ARCHITECT_PROMPT),
        HumanMessage(content=f"Planning Input:\n{page} ")
    ]

    result = llm.with_structured_output(PageArchitect).invoke(messages)

    return {"steps": [result]}

