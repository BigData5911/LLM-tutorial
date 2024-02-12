import os
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain

os.environ["OPEN_API_KEY"] = "sk-PYydU3RrEmqPLinR3VegT3BlbkFJ3Eyhtjtr"

db = SQLDatabase.from_uri('sqlite:///./db/Chinook.db')

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

chain = create_sql_query_chain(llm, db)

from langchain.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

system = """Double check the user's {dialect} query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

Output the final SQL query only."""

prompt = ChatPromptTemplate.from_messages(
  [("system", system), ("human", "{query}")],
).partial(dialect=db.dialect)

validation_chain = prompt | llm | StrOutputParser()

full_chain = {"query": chain} | validation_chain

query = full_chain.invoke(
  {
     "question": "What's the average Invoice from an American customer whose Fax is missing since 2003 but before 2010"
  }
)
