import os
from llama_index.core import Settings
from llama_index.core.prompts import ChatMessage, MessageRole
import streamlit as st
from dotenv import load_dotenv
from ai_news.st_util import (
    add_to_message_history,
    create_chat_engine,
    load_embed_model,
    load_model,
)

load_dotenv()

# Load from streamlit secrets or .env.
NEWS_API_KEY = st.secrets.get('NEWS_API_KEY', os.environ['NEWS_API_KEY'])
OPENAI_API_KEY = st.secrets.get('OPENAI_API_KEY', os.environ['OPENAI_API_KEY'])

if not all((NEWS_API_KEY, OPENAI_API_KEY)):
    st.error('Could not fetch API keys')
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

with st.sidebar:
    model = st.selectbox(
        label='Select which model to use',
        options=['gpt-3.5-turbo', 'gpt-4-turbo', 'gpt-4o'],
    ) or 'gpt-3.5-turbo'

# Dump message history.
for msg in st.session_state.messages:
    st.chat_message(msg.role.value).write(msg.content)

# Load LLM & embedding models.
Settings.llm = load_model(api_key=OPENAI_API_KEY, model=model)
Settings.embed_model = load_embed_model(api_key=OPENAI_API_KEY)

# Create chat engine.
chat_engine = create_chat_engine(news_api_key=NEWS_API_KEY)

if prompt := st.chat_input('What can I help you with?'):
    st.chat_message('user').write(prompt)
    add_to_message_history(MessageRole.USER, prompt)
    with st.chat_message(MessageRole.ASSISTANT.value):
        response_container = st.empty()
        with st.spinner('Thinking...'):
            response_stream = chat_engine.stream_chat(
                message=prompt,
                chat_history=st.session_state.messages,
            )
        response: str = ''
        for token in response_stream.response_gen:
            response += token
            response_container.markdown(response)
        # st.write(response_stream.response)
        # st.write(response.sources)
        add_to_message_history(MessageRole.ASSISTANT, response)
