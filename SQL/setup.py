import os
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI  # Updated import

# Set the environment variable for OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = "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"  # Replace with your actual OpenAI API key

# Initialize the SQLDatabase
db = SQLDatabase.from_uri("sqlite:///./db/Chinook.db")
print(db.dialect)
print(db.get_usable_table_names())
db.run("SELECT * FROM Artist LIMIT 10;")

# Initialize the ChatOpenAI class
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many employees are there"})
print(response)

from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
chain = write_query | execute_query
chain.invoke({"question": "How many employees are there"})