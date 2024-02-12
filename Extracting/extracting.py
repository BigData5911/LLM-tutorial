from langchain.chains import create_extraction_chain
from langchain_openai import ChatOpenAI

schema = {
  "properties": {
    "name": {"type": "string"},
    "height": {"type": "integer"},
    "hair_color": {"type": "string"},
  },
  "required": ["name", "height"],
}

inp = inp = """Alex is 5 feet tall. Claudia is 1 feet taller Alex and jumps higher than him. Claudia is a brunette and Alex is blonde."""

llm = ChatOpenAI(
  model="gpt-3.5-turbo",
  temperature=0
)

chain = create_extraction_chain(schema, llm)

chain.run(inp)

schema = {
  "properties": {
    "name": {"type": "string"},
    "height": {"type": "integer"},
    "hair_color": {"type": "string"},
  },
  "required": ["name", "height"],
}

chain = create_extraction_chain(schema, llm)

inp = """Alex is 5 feet tall. Claudia is 1 feet taller Alex and jumps higher than him. Claudia is a brunette and Alex is blonde.
Alex's dog Frosty is a labrador and likes to play hide and seek."""


chain.run(inp)