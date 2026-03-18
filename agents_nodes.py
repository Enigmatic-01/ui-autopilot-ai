#Implemts Nodes

from mimetypes import init

from langchain_core.messages import HumanMessage,SystemMessage
import prompt_toolkit
from states import *
from llms import *
from tools import *
from prompts import *
import os
from pathlib import Path

BASE_DIR = Path("./workspace").resolve()
BASE_DIR.mkdir(exist_ok=True)



def coding_agent(state: dict) -> dict:
    

    step = state["step"]
    

    init_msgs = [
        SystemMessage(content=CODING_PROMPT),
        HumanMessage(
            content=f"""
File Paths:
{step.path}

Extensions:
{step.extension}

Implementation Steps:
{step.steps}
"""
        )
    ]

    res = llm.with_structured_output(OutputFileSchema).invoke(init_msgs)

    return {"files": [res]}






def relative_path(from_file: Path, to_file: Path) -> str:
    """Compute relative path from from_file (HTML) to to_file (CSS/JS)."""
    return os.path.relpath(to_file.resolve(), start=from_file.parent.resolve())




def file_management_agent(state: dict):
    results = []

    all_files = state.get("all_files") or []
    if not all_files and "file" in state:
        all_files = [state["file"]]

    if not all_files:
        return {"file_status": "no files to process"}

    for file in all_files:
        try:
            # --- Safe path resolution ---
            clean_path = file.path.lstrip("/")
            path = (BASE_DIR / clean_path).resolve()

            if not str(path).startswith(str(BASE_DIR)):
                raise ValueError(f"Invalid path outside workspace: {path}")

            code = file.code
            ext = file.ext.lower().lstrip(".")

            # --- Fix HTML imports ---
            if ext == "html":
                css_files = [f for f in all_files if f.ext.lower().endswith("css")]
                js_files = [f for f in all_files if f.ext.lower().endswith("js")]

                for css in css_files:
                    css_path = (BASE_DIR / css.path.lstrip("/")).resolve()
                    rel = os.path.relpath(css_path, start=path.parent)

                    filename = Path(css.path).name
                    code = code.replace(f'href="{filename}"', f'href="{rel}"')

                for js in js_files:
                    js_path = (BASE_DIR / js.path.lstrip("/")).resolve()
                    rel = os.path.relpath(js_path, start=path.parent)

                    filename = Path(js.path).name
                    code = code.replace(f'src="{filename}"', f'src="{rel}"')

            # --- Ensure directory exists ---
            path.parent.mkdir(parents=True, exist_ok=True)

            # --- Write file ---
            path.write_text(code, encoding="utf-8")

            results.append({
                "path": clean_path,
                "status": "written"
            })

        except Exception as e:
            results.append({
                "path": getattr(file, "path", "unknown"),
                "status": "failed",
                "error": str(e)
            })

    return {}

def testing_agent(state: AgentState):

    files = state.get("files", [])
    if not files:
        return {
            "testing_result": TestingResults(
                results=[],
                passed=True,
                summary="No files to test."
            ),
            "memory": "",
            "retry": state.get("retry", 0)
        }

    virtual_files = {}

    for schema in files:
        for f in schema.files:
            virtual_path = f.path.lstrip("/")

            virtual_files[virtual_path] = {
                "filename": f.filename,
                "path": virtual_path,
                "ext": f.ext.lstrip("."),
                "code": f.code
            
            }

    files_repr = list(virtual_files.values())
    file_index = list(virtual_files.keys())

    agent_input = {
        "files": files_repr,
        "file_index": file_index,


    }

    res = testing_agent_executor.invoke({
        "input": agent_input,
        "goal": state["goal"]
    })

    structured: TestingResults = structured_llm.invoke(res["output"])

    passed = all(r.passed for r in structured.results)
    retry = state.get("retry", 0) + 1

    return {
        "testing_result": TestingResults(
            results=structured.results,
            passed=passed,
            summary=structured.summary
        ),
        "memory": "Testing completed using file-based ground truth.",
        "retry": retry
    }

def enhance_prompt(state: dict) -> dict:
    prompt = state["goal"]
    
    node = DevPromptEnhancerNode()
    enhanced_prompt = node.run(prompt)
    
    return {
        "goal": enhanced_prompt
    }