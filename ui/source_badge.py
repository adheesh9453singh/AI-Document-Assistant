import streamlit as st


def render_source_badge(source: str):
    """
    Display a badge indicating the response source.
    """

    if not source:
        return

    if source.lower() == "document":
        color = "#10B981"
        icon = "📄"
    else:
        color = "#3B82F6"
        icon = "🧠"

    st.markdown(
        f"""
        <div style="
            display:inline-block;
            background:{color};
            padding:4px 12px;
            border-radius:999px;
            font-size:12px;
            font-weight:600;
            color:white;
            margin-bottom:10px;
        ">
            {icon} {source}
        </div>
        """,
        unsafe_allow_html=True,
    )