import os
from llama_index.core.prompts import ChatMessage, MessageRole
import streamlit as st
from dotenv import load_dotenv
from ai_news.st_util import (
    add_to_message_history,
    create_chat_engine,
)

load_dotenv()

# Load from .env or streamlit secrets.
if (NEWS_API_KEY := os.getenv('NEWS_API_KEY')) is None:
    try:
        # TODO: Add secrets on deploy.
        NEWS_API_KEY = st.secrets.get('NEWS_API_KEY')
    except FileNotFoundError as e:
        st.error(f'Could not load NEWS_API_KEY. {e}')
        st.stop()

st.title('🤖 AI News 📰')
st.caption("""\
Get your latest AI news from multiple sources and interract to get more insight you care about.
""")

# Create messages state.
if 'messages' not in st.session_state:
    st.session_state.messages = [
        ChatMessage(
            role=MessageRole.ASSISTANT,
            content='What are you intrested in today?',
        )
    ]

# Dump message history.
for msg in st.session_state.messages:
    st.chat_message(msg.role.value).write(msg.content)

# Create chat engine.
chat_engine = create_chat_engine()

if prompt := st.chat_input('What can I help you with?'):
    st.chat_message('user').write(prompt)
    add_to_message_history(MessageRole.USER, prompt)
    with st.chat_message(MessageRole.ASSISTANT.value):
        with st.spinner('Thinking...'):
            response = chat_engine.chat(
                message=prompt,
                chat_history=st.session_state.messages,
            )
            st.write(response.response)
            # st.write(response.sources)
            add_to_message_history(MessageRole.ASSISTANT, response.response)
