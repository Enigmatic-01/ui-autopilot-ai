#LLMS
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from prompts import *
from tools import *
from pydantic_models import *
from graphs.prompts.debug_planning_prompts import *

load_dotenv()

llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", TESTING_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

testing_tool_agent = create_tool_calling_agent(
    llm,
    test_tools,
    prompt
)

testing_agent_executor = AgentExecutor(
    agent=testing_tool_agent,
    tools=test_tools,
    verbose=True,
    max_iterations=10,
    handle_parsing_errors=True
)
structured_llm = llm.with_structured_output(TestingResults)


rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", REWRITE_FILE_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)



rewrite_agent = create_tool_calling_agent(
    llm,
    rewrite_tools,
    rewrite_prompt
)

rewrite_agent_executor = AgentExecutor(
    agent=rewrite_agent,
    tools=rewrite_tools,
    verbose=True,
    max_iterations=10,
    handle_parsing_errors=True
)