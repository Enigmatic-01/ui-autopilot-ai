
from typing import Any

from typing_extensions import Annotated,TypedDict,List
from operator import add
from graphs.pydantic_models.planning_schemas import *
from graphs.pydantic_models.debug_planning_schemas import *
from pydantic_models import *

class AgentState(TypedDict, total=False):
    goal: str
    project_overview: ProjectOverviewSchema
    steps: Annotated[List[PageArchitect], add]
    files: Annotated[List[OutputFileSchema], add]
    testing_result:TestingResults
    memory:str
    debug_plans:DebugPlanSchema
    rewrite_status:str
    retry:int = 0
    updated_files:WriteFileSchema