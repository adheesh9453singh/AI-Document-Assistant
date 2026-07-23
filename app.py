import streamlit as st
from rag_pipeline import load_rag_chain, load_chatbot
from ingest import process_documents


# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

    st.title("🤖 AI Document Assistant")

    st.markdown("---")

    st.subheader("📂 Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose PDF file(s)",
        type=["pdf"],
        accept_multiple_files=True
    )

    process_button = st.button(
        "🚀 Process Documents",
        use_container_width=True
    )

    # ============================================
# PROCESS DOCUMENTS BUTTON
# ============================================



if process_button:

    if uploaded_files:

        with st.spinner("📄 Processing documents... Please wait"):

            success = process_documents(uploaded_files)

            if success:
                st.session_state.documents_processed = True
                st.success("✅ Documents processed successfully!")

            else:
                st.error("❌ Failed to process documents.")

    else:
        st.error("⚠️ Please upload at least one PDF.")

# ============================================
# STATUS
# ============================================

st.markdown("---")

st.subheader("📊 Status")

if st.session_state.documents_processed:
    st.success("✅ Documents Ready")
else:
    st.warning("⚠️ No Documents Processed")

# ============================================
# MAIN PAGE
# ============================================

st.title("🤖 AI Assistant")

st.caption(
    "Chat with AI or upload PDF documents for document-based answers using RAG.")


st.markdown("---")

# ============================================
# CHAT HISTORY
# ============================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================
# USER INPUT
# ============================================

question = st.chat_input(
    "Ask me anything... or upload PDF documents for document-based answers."

)



if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    try:

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                if st.session_state.documents_processed:

                    rag_chain = load_rag_chain()
                    answer = rag_chain.invoke(question)

                else:

                    chatbot = load_chatbot()
                    answer = chatbot.invoke(question).content

            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:

        st.error(f"❌ Error: {e}")