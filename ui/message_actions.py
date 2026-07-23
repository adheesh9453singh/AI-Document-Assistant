import streamlit as st


def render_actions(message: str, key: str):
    """
    Render action buttons below assistant messages.
    """

    col1, col2, col3 = st.columns([1, 1, 10])

    with col1:
        st.button(
            "👍",
            key=f"up_{key}",
            help="Helpful",
        )

    with col2:
        st.button(
            "👎",
            key=f"down_{key}",
            help="Not Helpful",
        )

    with col3:
        st.caption("Copy the response manually for now.")