import os
import uuid

import streamlit as st
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


# ============================================================
# 1. Configuration
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="Conversational AI",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# 2. Application Header
# ============================================================

st.title("🤖 Conversational AI")
st.caption("A simple conversational AI built with LangChain and GPT-4o-mini")


# ============================================================
# 3. Session State
# ============================================================

if "store" not in st.session_state:
    st.session_state.store = {}

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


# ============================================================
# 4. Conversation History
# ============================================================

def get_session_history(session_id):
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = InMemoryChatMessageHistory()

    return st.session_state.store[session_id]


# ============================================================
# 5. Prompt
# ============================================================

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a helpful teacher.

Explain concepts for beginners.
Use simple examples when helpful.
Keep explanations clear and concise."""
    ),
    MessagesPlaceholder("history"),
    (
        "human",
        "{question}"
    )
])


# ============================================================
# 6. LLM
# ============================================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)


# ============================================================
# 7. LangChain
# ============================================================

chain = prompt | llm | StrOutputParser()

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)


# ============================================================
# 8. Sidebar
# ============================================================

with st.sidebar:

    st.header("💬 Chat")

    st.write(
        "Ask questions and have a conversation with the AI. "
        "The application remembers previous messages in the current chat."
    )

    st.divider()

    st.subheader("Technology")

    st.write("**Framework:** LangChain")
    st.write("**Model:** GPT-4o-mini")
    st.write("**Memory:** Chat message history")
    st.write("**Response:** Streaming")

    st.divider()

    if st.button("🆕 New Chat", use_container_width=True):

        st.session_state.session_id = str(uuid.uuid4())

        st.rerun()


# ============================================================
# 9. Display Conversation History
# ============================================================

history = get_session_history(st.session_state.session_id)

for message in history.messages:

    if message.type == "human":

        with st.chat_message("user"):
            st.markdown(message.content)

    elif message.type == "ai":

        with st.chat_message("assistant"):
            st.markdown(message.content)


# ============================================================
# 10. Chat Input
# ============================================================

question = st.chat_input("Ask me anything...")


# ============================================================
# 11. Process User Question
# ============================================================

if question:

    # Display user's message
    with st.chat_message("user"):
        st.markdown(question)

    # Generate assistant response
    with st.chat_message("assistant"):

        response_placeholder = st.empty()
        response = ""

        for chunk in chain_with_history.stream(
            {"question": question},
            config={
                "configurable": {
                    "session_id": st.session_state.session_id
                }
            }
        ):

            response += chunk
            response_placeholder.markdown(response)
