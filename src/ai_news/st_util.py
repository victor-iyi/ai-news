import streamlit as st


def add_to_message_history(role: str, content: str) -> None:
    """Adds a message to the message history.

    Args:
        role (str): The role of the message sender.
        content (str): The content of the message.

    """
    st.session_state.messages.append({'role': role, 'content': content})
