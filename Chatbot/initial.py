import dotenv

dotenv.load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory

chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)

prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You are a helpful assistant. Answer all questions to the best of your ability."
    ),
    MessagesPlaceholder(variable_name="message")
  ]
)

chat = prompt | chat

print(chat.invoke(
  {
    "messages": [
      HumanMessage(
              content="Translate this sentence from English to French: I love programming."
      ),
      AIMessage(content="J'adore la programmation."),
      HumanMessage(content="What did you just say?"),
    ]
  }
))

demo_ephemeral_chat_history = ChatMessageHistory()

demo_ephemeral_chat_history.add_user_message("hi")

demo_ephemeral_chat_history.add_ai_message("whats up?")

print(demo_ephemeral_chat_history.messages)

demo_ephemeral_chat_history.add_user_message(
    "Translate this sentence from English to French: I love programming."
)


response = chat.invoke({"messages": demo_ephemeral_chat_history.messages})

demo_ephemeral_chat_history.add_ai_message(response)

demo_ephemeral_chat_history.add_user_message("What did you just say?")

chat.invoke({"messages": demo_ephemeral_chat_history.messages})

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader('https://docs.smith.langchain.com/overview')
data = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

all_splits = text_splitter.split_documents(data)

from langchain_community.vectorstores import Chorma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chorma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever(k=4)


docs = retriever.invoke("how can langsmith help with testing?")