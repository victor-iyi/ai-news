import os
import streamlit as st
from dotenv import load_dotenv
from ai_news.st_util import add_to_message_history
from ai_news.rag.index import create_index

load_dotenv()

# Load from .env or streamlit secrets.
if (NEWS_API_KEY := os.getenv('NEWS_API_KEY')) is None:
    try:
        # TODO: Add secrets on deploy.
        NEWS_API_KEY = st.secrets.get('NEWS_API_KEY')
    except FileNotFoundError as e:
        st.error(f'Could not load NEWS_API_KEY. {e}')
        st.stop()

# Containers.
header = st.container()
# latest_news = st.container()
# chat_section = st.container()

with header:
    st.title('AI News')
    st.caption('''\
    Get your latest AI news from multiple sources and interract to get more insight you care about.
    ''')

st.header('Get the latest news')

# Create messages state.
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            'role': 'assistant',
            'content': 'What are you intrested in today?',
        },
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

# TODO: Wrap this in a progress bar or spinner widget.
if 'chat_engine' not in st.session_state.keys():
    index = create_index(
        topic='artificial intelligence',
        collection_name='artificial_intelligence'
    )
    chat_engine = index.as_chat_engine()
    st.session_state.chat_engine = chat_engine


if prompt := st.chat_input(st.session_state.messages[0]['content']):
    st.chat_message('user').write(prompt)
    add_to_message_history('user', prompt)
    with st.chat_message('assistant'):
        with st.spinner('Thinking...'):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            # st.write(response.sources)
            add_to_message_history('assistant', response.response)
