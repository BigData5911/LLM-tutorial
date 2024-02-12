import os
from langchain_openai.chat_models  import ChatOpenAI


from  langchain_core.tools import tool

os.environ["OPEN_API_PATH"] = "sk-PYydU3RrEmqPLinR3VegT3BlbkFJ3Eyhtjtr"
model = ChatOpenAI(model="gpt-3.5-turbo=1106")

@tool
def multiply(first_int: int, second_int: int) -> int:
  """Multiply two integers together"""
  return first_int * second_int

print(multiply.name)
print(multiply.description)
print(multiply.args)

print(multiply.invoke({"first_int": 4, "second_int": 5}))

model_with_tools = model.bind_tools([multiply], tool_choice="multiply")

print(model_with_tools.kwargs["tools"])

from langchain.output_parsers import JsonOutputKeyToolsParser

chain = model_with_tools | JsonOutputKeyToolsParser(key_name="multiply", return_single = True )
chain.invoke("What's four times 23")

from operator import itemgetter

# Note: the `.map()` at the end of `multiply` allows us to pass in a list of `multiply` arguments instead of a single one.
chain = (
    model_with_tools
    | JsonOutputKeyToolsParser(key_name="multiply", return_single=True)
    | multiply
)
chain.invoke("What's four times 23")


from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent

prompt = hub.pull("hwchase17/openai-tools-agent")
print(prompt.messages)

@tool
def add(first_int: int, second_int: int) -> int:
  "Add two integers."
  return first_int + second_int

@tool
def exponentiate(base: int, exponent: int) -> int:
  "Exponentiate the base to the exponent power."
  return base**exponent

tools = [multiply, add, exponentiate]

model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

# Construct the OpenAI Tools agent
agent = create_openai_tools_agent(model, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke(
  {
    "input" :  "Take 3 to the fifth power and multiply that by the sum of twelve and three, then square the whole result"
  }
)

