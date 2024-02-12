import os
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.prompt import SQL_PROMPTS
from langchain.chains import create_sql_query_chain


os.environ["OPENAI_API_KEY"] = "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"

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

db = SQLDatabase.from_uri('sqlite:///./db/Chinook.db')

chain = create_sql_query_chain(llm, db)
chain.get_prompts()[0].pretty_print()

context = db.get_context()

prompt_with_context = chain.get_promts()[0].partial(table_info = context["table_info"])

examples = [
    {"input": "List all artists.", "query": "SELECT * FROM Artist;"},
    {
        "input": "Find all albums for the artist 'AC/DC'.",
        "query": "SELECT * FROM Album WHERE ArtistId = (SELECT ArtistId FROM Artist WHERE Name = 'AC/DC');",
    },
    {
        "input": "List all tracks in the 'Rock' genre.",
        "query": "SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');",
    },
    {
        "input": "Find the total duration of all tracks.",
        "query": "SELECT SUM(Milliseconds) FROM Track;",
    },
    {
        "input": "List all customers from Canada.",
        "query": "SELECT * FROM Customer WHERE Country = 'Canada';",
    },
    {
        "input": "How many tracks are there in the album with ID 5?",
        "query": "SELECT COUNT(*) FROM Track WHERE AlbumId = 5;",
    },
    {
        "input": "Find the total number of invoices.",
        "query": "SELECT COUNT(*) FROM Invoice;",
    },
    {
        "input": "List all tracks that are longer than 5 minutes.",
        "query": "SELECT * FROM Track WHERE Milliseconds > 300000;",
    },
    {
        "input": "Who are the top 5 customers by total purchase?",
        "query": "SELECT CustomerId, SUM(Total) AS TotalPurchase FROM Invoice GROUP BY CustomerId ORDER BY TotalPurchase DESC LIMIT 5;",
    },
    {
        "input": "Which albums are from the year 2000?",
        "query": "SELECT * FROM Album WHERE strftime('%Y', ReleaseDate) = '2000';",
    },
    {
        "input": "How many employees are there",
        "query": 'SELECT COUNT(*) FROM "Employee"',
    },
]

from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")

prompt = FewShotPromptTemplate(
  examples=examples[:5],
  example_prompt=example_prompt,
  prefix="You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries.",
  suffix="User input: {input}\nSQL query: ",
  input_variables=["input", "top_k", "table_info"]
)

print(prompt.format(input="How many artists are there?", top_k=3, table_info="foo"))

from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

example_selectors = SemanticSimilarityExampleSelector.from_examples(
  examples,
  OpenAIEmbeddings(),
  FAISS,
  k=5,
  input_keys=["input"]
)