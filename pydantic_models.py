from typing import List, Optional
from pydantic import BaseModel, Field
from graphs.pydantic_models.planning_schemas import *


class CodingInput(BaseModel):
    filename: str
    path: str
    ext: str

    required_for: str

    functions_implemented: List[str]
    selectors_used: List[str]

    dependencies: List[str]

    overview_functions: List[Function]
    overview_selectors: List[Selector]

    steps: List[str]


class FileOutput(BaseModel):
    filename: str
    path: str
    ext: str
    code: str


class OutputFileSchema(BaseModel):
    files: List[FileOutput]

class TestIssue(BaseModel):
    type: Literal["error", "warning"]
    message: str
    file: str
    line: Optional[int] = None
    selector: Optional[str] = None
    suggestion: Optional[str] = None


class FileTestResult(BaseModel):
    file: str
    passed: bool
    issues: List[TestIssue]


class TestingResults(BaseModel):
    results: List[FileTestResult]
    passed: bool
    summary: str


class DevPromptEnhancerNode:
    def __init__(self):
        self.system_instruction = """
You are a senior software engineer.

Your job is to rewrite user prompts into highly effective development prompts.
Ensure:
- Clear task definition
- Tech stack (if missing, infer or suggest)
- Input/output expectations
- Edge cases or constraints
- Clean formatting
"""

    def run(self, prompt: str) -> str:
        return f"""
{self.system_instruction}

Rewrite the following development request into a detailed and structured prompt.

Original Request:
{prompt}

Enhanced Development Prompt:
- Objective:
- Requirements:
- Tech Stack:
- Input:
- Output:
- Constraints:
- Edge Cases:
- Example (if applicable):
""".strip()


