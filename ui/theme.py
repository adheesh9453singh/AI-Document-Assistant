import streamlit as st
from pathlib import Path


def load_theme():
    """
    Configure the Streamlit page and load custom CSS.
    """

    st.set_page_config(
        page_title="AI Document Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    css_file = Path(__file__).parent / "styles.css"

    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )