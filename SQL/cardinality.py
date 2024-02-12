import ast
import re
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI


db = SQLDatabase.from_uri("sqlite:///./db/Chinook.db")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def query_as_list(db, query):
  res = db.run(query)
  res = [el for sub in ast.literal_eval(res) for el in sub]
  res = [re.sub(r"\b\d+\b", "", string) for string in res]
  return res

proper_nouns = query_as_list(db, "select name from artist")
proper_nouns += query_as_list(db, "select title from album")
proper_nouns += query_as_list(db, "select name from genre")

print(proper_nouns[:5])

from langchain_community.vectorstores import faiss
from langchain_openai import OpenAIEmbeddings

vector_db = faiss.from_texts(proper_nouns, OpenAIEmbeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 15})

from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from langchain.chains import create_sql_query_chain

system = """You are a SQLite expert. Given an input question, create a syntactically \
correct SQLite query to run. Unless otherwise specificed, do not return more than \
{top_k} rows.\n\nHere is the relevant table info: {table_info}\n\nHere is a non-exhaustive \
list of possible feature values. If filtering on a feature value make sure to check its spelling \
against this list first:\n\n{proper_nouns}"""

prompt = ChatPromptTemplate.from_messages([("system", system), ("humman", "{input}")])
query_chain = create_sql_query_chain(llm, db, prompt=prompt)

retriever_chain = (
    itemgetter("question")
    | retriever
    | (lambda docs: "\n".join(doc.page_content for doc in docs))
)

chain = RunnablePassthrough.assign(proper_nouns=retriever_chain) | query_chain

query = query_chain.invoke(
    {"question": "What are all the genres of elenis moriset songs", "proper_nouns": ""}
)

print(query)
db.run(query)

# With retrieval
query = chain.invoke({"question": "What are all the genres of elenis moriset songs"})
print(query)
db.run(query)
