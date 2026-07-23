import streamlit as st

from agent import ask_agent
from ingest import process_documents

from ui.theme import load_theme
from ui.chat import render_chat

# ============================================
# LOAD THEME
# ============================================

load_theme()

# ============================================
# SESSION STATE
# ============================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:


    st.markdown("---")

    st.subheader("📂 Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose PDF file(s)",
        type=["pdf"],
        accept_multiple_files=True,
    )

    process_button = st.button(
        "🚀 Process Documents",
        use_container_width=True,
    )

    st.markdown("---")

    st.subheader("📊 Status")

    if st.session_state.documents_processed:
        st.success("✅ Documents Ready")
    else:
        st.warning("⚠️ No Documents Processed")

# ============================================
# PROCESS DOCUMENTS
# ============================================

if process_button:

    if uploaded_files:

        with st.spinner("📄 Processing documents..."):

            success = process_documents(uploaded_files)

            if success:
                st.session_state.documents_processed = True
                st.success("✅ Documents processed successfully!")
            else:
                st.error("❌ Failed to process documents.")

    else:
        st.error("⚠️ Please upload at least one PDF.")

# ============================================
# MAIN PAGE
# ============================================



# ============================================
# DISPLAY CHAT HISTORY
# ============================================

render_chat(st.session_state.messages)

# ============================================
# CHAT INPUT
# ============================================

question = st.chat_input("💬 Ask anything...")

if question:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Refresh UI immediately
    st.rerun()

# ============================================
# GENERATE RESPONSE
# ============================================

if (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
):

    question = st.session_state.messages[-1]["content"]

    try:

        with st.spinner("🤖 Thinking..."):

            result = ask_agent(
                question,
                st.session_state.documents_processed,
            )

            st.write("RESULT:", result)
            st.write("TYPE:", type(result))
 



        answer = result["answer"]
        source = result["source"]

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "source": source,
            }
        )

        st.rerun()

    except Exception as e:

        st.error(f"❌ {e}")