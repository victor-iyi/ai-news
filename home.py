import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Load from .env or streamlit secrets.
if (NEWS_API_KEY := os.getenv('NEWS_API_KEY')) is None:
    try:
        # TODO: Add secrets on deploy.
        NEWS_API_KEY = st.secrets.get('NEWS_API_KEY')
    except FileNotFoundError as e:
        st.error(f'Could not load NEWS_API_KEY. {e}')
        st.stop()

st.title('AI News')
st.caption('''\
Get your latest AI news from multiple sources and interract to get more insight you care about.
''')
