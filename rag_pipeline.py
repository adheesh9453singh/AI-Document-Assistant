from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from config import (
    CHROMA_DB_DIR,
    EMBEDDING_MODEL,
    GROQ_API_KEY,
    MODEL_NAME,
)


# --------------------------
# Format Retrieved Documents
# --------------------------

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# --------------------------
# LLM
# --------------------------

def get_llm():

    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=MODEL_NAME,
        temperature=0,
    )


# --------------------------
# General Chatbot
# --------------------------

def load_chatbot():

    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=MODEL_NAME,
        temperature=0.3,
    )


# --------------------------
# Embeddings
# --------------------------

def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )


# --------------------------
# Vector Store
# --------------------------

def get_vector_store():

    return Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=get_embeddings(),
    )


# --------------------------
# Retriever
# --------------------------

def get_retriever():

    return get_vector_store().as_retriever(
        search_kwargs={"k": 4}
    )


# --------------------------
# Retrieve Documents
# --------------------------

def retrieve_documents(question: str):

    retriever = get_retriever()

    return retriever.invoke(question)


# --------------------------
# Retrieve Context
# --------------------------
# --------------------------
# Retrieve Context
# --------------------------

def retrieve_context(question: str) -> str:
    """
    Retrieve relevant document chunks and return them
    as a single string.
    """

    docs = retrieve_documents(question)

    if not docs:
        return ""

    return format_docs(docs)


# --------------------------
# Prompt
# --------------------------

def get_prompt():

    return ChatPromptTemplate.from_template(
        """
You are a helpful AI assistant.

Answer the user's question ONLY using the provided context.

If the answer cannot be found in the context, reply exactly:

"I don't know based on the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""
    )


# --------------------------
# RAG Chain
# --------------------------

def load_rag_chain():

    print("Loading retriever...")
    retriever = get_retriever()

    print("Loading prompt...")
    prompt = get_prompt()

    print("Loading LLM...")
    llm = get_llm()

    print("Building RAG chain...")

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    print("✅ RAG chain ready!")

    return rag_chain