import streamlit as st

from ui.source_badge import render_source_badge
from ui.message_actions import render_actions


def render_chat(messages):
    """
    Render the entire conversation.
    """

    if not messages:
        render_welcome()
        return

    for index, message in enumerate(messages):

        render_message(
            role=message.get("role", "assistant"),
            content=message.get("content", ""),
            source=message.get("source"),
            key=index,
        )


def render_message(
    role: str,
    content: str,
    source: str | None = None,
    key: int = 0,
):
    """
    Render a single chat message.
    """

    avatar = "👤" if role == "user" else "🤖"
    title = "You" if role == "user" else "AI Assistant"

    with st.chat_message(role):

        col_avatar, col_message = st.columns(
            [1, 12],
            vertical_alignment="top",
        )

        with col_avatar:

            st.markdown(
                f"""
                <div class="avatar">
                    {avatar}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_message:

            st.markdown(
                f"""
                <div class="message-header">
                    <div class="message-role">
                        {title}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if role == "assistant" and source:
                render_source_badge(source)

            st.markdown(
                f"""
                <div class="message-card {role}-message">
                    {content}
                </div>
                """,
                unsafe_allow_html=True,
            )

            if role == "assistant":
                render_actions(
                    message=content,
                    key=str(key),
                )


def add_user_message(question: str):
    """
    Add user message to session.
    """

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )


def add_assistant_message(
    answer: str,
    source: str | None = None,
):
    """
    Add assistant message to session.
    """

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "source": source,
        }
    )


def clear_chat():
    """
    Clear conversation.
    """

    st.session_state.messages = []


def render_welcome():

    st.markdown(
        """
<div class="welcome">

<h1>🤖 AI Document Assistant</h1>

<p>
Upload PDF documents and ask questions naturally.

The assistant intelligently decides whether to answer
from your uploaded documents or general AI knowledge.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("### 💡 Try asking")

    col1, col2 = st.columns(2)

    with col1:

        st.info("📄 Summarize my uploaded PDF")

        st.info("📚 Explain this document")

    with col2:

        st.info("🧠 What is LangGraph?")

        st.info("💻 Generate Python interview questions")