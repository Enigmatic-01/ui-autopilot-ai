from re import L
from typing import List, Optional
from langchain_community.cache import Base
from pydantic import BaseModel, Field


class RewritingSteps(BaseModel):
    filename:str
    title:str
    steps:List[str]

class Debug(BaseModel):
    plan:List[RewritingSteps]
    code:str
    path:str

class DebugPlanSchema(BaseModel):
    planning:List[Debug]


class WriteFile(BaseModel):
    path: str
    content: str

class WriteFileSchema(BaseModel):
    updated_files:List[WriteFile]