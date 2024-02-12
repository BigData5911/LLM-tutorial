import os
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field

os.environ["OPEN_API_PATH"] = "sk-PYydU3RrEmqPLinR3VegT3BlbkFJ3Eyhtjtr"
db = SQLDatabase.from_uri('sqlite:///./db/Chinook.db')
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

class Table(BaseModel):
  """Table in SQL database."""
  name: str = Field(description="Name of table in SQL database.")

table_names = "\n".join(db.get_usable_table_names())
system = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables are:
{table_names}
Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

table_chain = create_extraction_chain_pydantic(Table, llm, system_message=system)
table_chain.invoke({"input": "What are all the genres of Alanis Morisette songs"})

system = f"""Return the names of the SQL tables that are relevant to the user question. \
The tables are:

Music
Business"""
category_chain = create_extraction_chain_pydantic(Table, llm, system_message=system)
category_chain.invoke({"input": "What are all the genres of Alanis Morisette songs"})

from typing import List

def get_tables(categories: List[Table]) -> List[str]:
  """Get table names from Table pydantic models."""
  tables = []
  for category in categories:
    if category.name == "Music":
      tables.extend([
          "Album",
          "Artist",
          "Genre",
          "MediaType",
          "Playlist",
          "PlaylistTrack",
          "Track",
      ])
    elif category.name == "Business":
      tables.extend([
        "Customer", "Employee", "Invoice", "InvoiceLine"
      ])
  return tables

table_chain = category_chain | get_tables
table_chain.invoke({"input": "What are all the genres of Alanis Morisette songs"})

from operator import itemgetter

from langchain.chains import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough

query_chain = create_sql_query_chain(llm, db)
# Convert "question" key to the "input" key expected by current table_chain.
table_chain = {"input": itemgetter("question")} | table_chain
# Set table_names_to_use using table_chain.
full_chain = RunnablePassthrough.assign(table_names_to_use=table_chain) | query_chain

query = full_chain.invoke(
  {
    "question": "What are all the genres of Alanis Morisette songs"
  }
)

print(query)

query = full_chain.invoke(
  {
    "question": "What is the set of all unique gengres of Alanis Morisette songs"
  }
)

print(query)



