import dotenv

dotenv.load_dotenv()

from langchain_openai import ChatOpenAI

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

from langchain_core.messages import HumanMessage, AIMessage

chat.invoke(
  [
    HumanMessage(
      content="Translate this sentence from English to French: I love programming."
    )
  ]
)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_examples(
  [
    (
      "system",
       "You are a helpful assistant. Answer all questions to the best of your ability.",
    ),
    MessagesPlaceholder(variable_name="messages")
  ]
)

chain = prompt | chat

chain.invoke(
    {
        "messages": [
            HumanMessage(
                content="Translate this sentence from English to French: I love programming."
            ),
            AIMessage(content="J'adore la programmation."),
            HumanMessage(content="What did you just say?"),
        ],
    }
)

from langchain.memory import ChatMessageHistory

demo_ephemeral_chat_history = ChatMessageHistory()

demo_ephemeral_chat_history.add_user_message("hi")

chain.invode(
  {
    "messages": demo_ephemeral_chat_history.messages
  }
)

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
data = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

vectorescores = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings)

retriever = vectorescores.as_retriever(k=4)

docs = retriever.invoke("how can langsmith help with testing?")

from langchain.chains.combine_documents import create_stuff_documents_chain

chat = ChatOpenAI(model="gpt-3.5-turbo-1106")

question_answering_prompt = ChatPromptTemplate.from_messages(
      [
        (
            "system",
            "Answer the user's questions based on the below context:\n\n{context}",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

document_chain = create_stuff_documents_chain(
  chat, question_answering_prompt
)

from langchain.memory import ChatMessageHistory

demo_ephemeral_chat_history = ChatMessageHistory()

demo_ephemeral_chat_history.add_user_message("how can langsmith help with testing?")

document_chain.invoke(
  {
    "messages": demo_ephemeral_chat_history.messages,
    "context": docs,
  }
)

#-----------------------------Creating a retrieval chain

from typing import Dict

from langchain_core.runnables import RunnablePassthrough

def parse_retriever_input(params: Dict):
    return params["messages"][-1].content

retrieval_chain = RunnablePassthrough.assign(
    context=parse_retriever_input | retriever,
).assign(
    answer=document_chain,
)

response = retrieval_chain.invoke(
    {
        "messages": demo_ephemeral_chat_history.messages,
    }
)

response