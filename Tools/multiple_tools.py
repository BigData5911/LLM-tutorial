import os
from langchain_core.tools import tool

os.environ["OPEN_API_KEY"] = "sk-PYydU3RrEmqPLinR3VegT3BlbkFJ3Eyhtjtr"

@tool
def multiply(first_int: int, second_int:int) -> int:
  """Multiply two integeres together."""
  return first_int * second_int

@tool
def add(first_int: int, second_int: int) -> int:
  "Add two integers."
  return first_int + second_int

@tool
def exponentiate(base: int, exponent: int) -> int:
  "Exponentiate the base to the exponent power."
  return base**exponent

tools = [multiply, add, exponentiate]

from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI

prompt = hub.pull("hwchase17/openai-tools-agent")
prompt.pretty_print()

# Choose the LLM that will drive the agent
# Only certain models support this
model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

# Construct the OpenAI Tools agent
agent = create_openai_tools_agent(model, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

from operator import itemgetter
from typing import Union

from langchain.output_parsers import JsonOutputToolsParser
from langchain_core.runnables import (
  Runnable,
  RunnableLambda,
  RunnableMap,
  RunnablePassthrough
)
from langchain_openai import ChatOpenAI

model = ChatOpenAI(mode="gpt-3.5-turbo")
tools = [multiply, exponentiate, add]
model_with_tools = model.bind_tools(tools)
tool_map = {tool.name: tool for tool in tools}

def call_tool(toll_invocation: dict) -> Union[str, Runnable]:
  """Function for dynamically constructing the end of the chain based on the model-selected tool."""
  tool = tool_map[toll_invocation["type"]]
  return RunnablePassthrough.assign(output=itemgetter("args") | tool)

call_tool_list = RunnableLambda(call_tool).map()
chain = model_with_tools | JsonOutputToolsParser() | call_tool_list

 