from typing import List, Optional,Literal
from pydantic import BaseModel, Field

# ------------------- Planning Components -------------------

class Selector(BaseModel):
    name: str = Field(..., description="CSS selector name")
    type: Optional[str] = Field(
        None,
        description="Selector type: container, button, input, list, card, modal, alert"
    )
    description: str = Field(..., description="Purpose of this selector in the UI")
    used_in_functions: List[str] = Field(
        default_factory=list,
        description="Functions that interact with this selector"
    )

class Function(BaseModel):
    name: str = Field(..., description="Function name")
    description: str = Field(..., description="What the function does")
    selectors_used: List[str] = Field(
        default_factory=list,
        description="Selectors accessed by this function"
    )

class Identifiers(BaseModel):
    used_function: List[Function]
    used_selector: List[Selector]
    mapping: str = Field(..., description="Complete mapping of functions to their selectors")

class DummyPages(BaseModel):
    code: str = Field(description="Complete dummy code of HTML, CSS, JS")
    identifiers: Identifiers = Field(description="Identifiers extracted from the dummy code")

# ------------------- Project Pages -------------------
class FilePlan(BaseModel):
    path: str
    type: Literal["html","css","js","data","asset"]
    description: str


class ComponentMount(BaseModel):
    component: str
    selector: str

class TestScenario(BaseModel):
    name: str
    steps: List[str]
    expected_result: str

class UIElement(BaseModel):
    tag: str
    id: Optional[str]
    class_name: Optional[str]
    children: Optional[List["UIElement"]]
    description: str
    required: bool = True
    related_features: Optional[List[str]]

class Feature(BaseModel):
    name: str
    description: str
    required_ui: List[str]
    required_logic: List[str]
    validation: List[str]

class BehaviorRule(BaseModel):
    rule: str
    example: Optional[str]

class JSFunction(BaseModel):
    name: str
    selector: str
    event: str
    updates: List[str]
    related_features: List[str]
    description: str
    behavior_rules: List[BehaviorRule]


class Component(BaseModel):
    name: str
    html_path: str
    css_path: Optional[str]
    js_path: Optional[str]
    selectors: List[str]
    description: str


class Page(BaseModel):
    name: str
    path: str

    description: str

    layout: List[UIElement]

    components: List[ComponentMount]

    selectors: List[str]

    js_functions: List[JSFunction]

    dependencies: List[str]

    data_sources: Optional[List[str]]

    features: List[Feature]

    test_scenarios: List[TestScenario]

    behavior_rules: List[BehaviorRule]

class AssetPlan(BaseModel):
    images: List[str]
    icons: List[str]
    fonts: List[str]
    videos: List[str]


class ProjectOverviewSchema(BaseModel):

    tech: str

    description: str

    files: List[FilePlan]

    pages: List[Page]

    components: List[Component]

    assets: AssetPlan

    global_selectors: List[str]

    data_files: Optional[List[str]]

    final_result: str

# -------------------Architect---------------------------------------


class PageArchitect(BaseModel):
    steps: List[List[str]] = Field(
        description="Complete steps for writing the code. Each inner list represents steps for one file (HTML, CSS, JS)."
    )
    path:List[str] = Field(description="complete path of files")
    extension:List[str] =  Field(description="extension of files")






