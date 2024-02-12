

from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser

repo_path = "E:\Workspace\Python\langchain-master (1)\langchain-master"

loader = GenericLoader.from_filesystem(
  repo_path + "/libs/langchain/langchain",
  glob="**/*",
  suffixes=[".py"],
  exclude=["**/non-utf8-encoding.py"],
  parser=LanguageParser(language=Language.PYTHON, parser_threshold=500)
)

documents = loader.load()

print(len(documents))

from langchain.text_splitter import RecursiveCharacterTextSplitter
pow+ \\\\\\\\\\\=========================================================================================================================================================================================================================================================================================================================================================================================================================gr4lop9yfbvc      mmnnbobmmmmmmmn m,o;.v
python_splitter = RecursiveCharacterTextSplitter.from_language(
  language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
)
texts = python_splitter.split_documents(documents)
len(texts)

from langchain_community.vectorstores import chroma
from langchain_openai import OpenAIEmbeddings

db = chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
retriever = db.as_retriever(
  search_type="mmr",
  search_kwargs={"k": 8},
)


from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model='gpt-3.5-turbo-1106')
memory = ConversationSummaryMemory(
  llm = llm, memory_key="chat_history", return_messages=True
)

qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

question = "How can I initialize a ReAct agent?"
result = qa(question)
result["answer"]

questions = [
    "What is the class hierarchy?",
    "What classes are derived from the Chain class?",
    "What one improvement do you propose in code in relati  on to the class hierarchy for the Chain class?",
]

for question in questions:
  result = qa(question)
  print(f"-> **Question**: {question} \n")
  print(f"**Answer**: {result['answer']} \n")

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.memory import ConversationSummaryMemory
from langchain.prompts import PromptTemplate
from langchain_community.llms import llamacpp