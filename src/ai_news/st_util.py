import streamlit as st
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.prompts import ChatMessage, MessageRole

from ai_news.rag.index import create_index


def add_to_message_history(role: MessageRole, content: str) -> None:
    """Adds a message to the message history.

    Args:
        role (str): The role of the message sender.
        content (str): The content of the message.

    """
    st.session_state.messages.append(ChatMessage(role=role, content=content))


@st.cache_resource(show_spinner='Creating chat engine from index...')
def create_chat_engine() -> BaseChatEngine:
    """Create chat engine from index."""
    index = create_index(
        topic='artificial intelligence',
        collection_name='artificial_intelligence',
        use_semantic_splitter=True,
    )
    chat_engine: BaseChatEngine = index.as_chat_engine()
    return chat_engine
