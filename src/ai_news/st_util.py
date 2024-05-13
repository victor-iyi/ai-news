import streamlit as st
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.prompts import ChatMessage, MessageRole
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

from ai_news.rag.index import create_index


def add_to_message_history(role: MessageRole, content: str) -> None:
    """Adds a message to the message history.

    Args:
        role (str): The role of the message sender.
        content (str): The content of the message.

    """
    st.session_state.messages.append(ChatMessage(role=role, content=content))


@st.cache_resource(
    show_spinner='Creating chat engine from index. This will take a few moment..',
)
def create_chat_engine(news_api_key: str) -> BaseChatEngine:
    """Create chat engine from index."""
    index = create_index(
        topic='artificial intelligence',
        collection_name='artificial_intelligence',
        use_semantic_splitter=True,
        news_api_key=news_api_key,
    )
    chat_engine: BaseChatEngine = index.as_chat_engine()
    return chat_engine


@st.cache_data
def load_embed_model(api_key: str) -> OpenAIEmbedding:
    """Load OpenAI embedding model."""
    return OpenAIEmbedding(
        api_key=api_key,
    )


@st.cache_data
def load_model(api_key: str) -> OpenAI:
    """Load OpenAI model."""
    return OpenAI(
        api_key=api_key,
    )
