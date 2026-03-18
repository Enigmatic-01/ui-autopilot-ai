from states import *
from llms import llm,rewrite_agent_executor
from ..pydantic_models.debug_planning_schemas import *
from ..prompts.debug_planning_prompts import *
from langchain_core.messages import HumanMessage,SystemMessage

def deb_palnning_agent(state:dict)->dict:
    tests = state["testing_result"]

    all_files = [f for schema in state["files"] for f in schema.files]

    matched_files = [
        f for f in all_files
        if any(t.file in f.path or t.file == f.filename for t in tests.results)
    ]
    init_msgs = [
        SystemMessage(content=DEBUG_PROMPT),
        HumanMessage(content=f"test results are : {tests} and files : {matched_files} ")
    ]

    res = llm.with_structured_output(DebugPlanSchema).invoke(init_msgs)
    print(res)
    return {"debug_plans":res}



def code_agent_node(state:dict):

    debug_plan = state["debug_plans"]

    if not debug_plan.planning:
        return {"rewrite_status": "no files to rewrite"}

    input_data = {
        "planning": [
            {
                "path": d.path.lstrip("/"),
                "code": d.code,
                "plan": d.plan
            }
            for d in debug_plan.planning
        ]
    }
    init_msgs = [
        SystemMessage(content=REWRITE_PROMPT),
        HumanMessage(content=f"input: {input_data}")
    ]

    res = llm.with_structured_output(WriteFileSchema).invoke(init_msgs)

    return {"updated_files": res}

def rewrite_agent_node(state: dict):
    files = state["updated_files"]
    
    input_data = [
        {
            "path": f.path,
            "content": f.content
        }
        for f in files.updated_files
    ]

    response = rewrite_agent_executor.invoke({
        "input": input_data
        
    })

    return {}