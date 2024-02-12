import dotenv

dotenv.load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from langchain.memory import ChatMessageHistory

chat = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.1)

prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
       "You are a helpful assistant. Answer all questions to the best of your ability.",
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "(input)")
  ]
)

from langchain_core.runnables.history import RunnableWithMessageHistory

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

chain = prompt | chat

chain_with_message_history = RunnableWithMessageHistory(
  chain,
  lambda session_id: demo_ephemeral_chat_history_for_chain,
  input_messages_key="input",
  history_messages_key="chat_history"
)


