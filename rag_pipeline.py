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


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def load_rag_chain():

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings,
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=MODEL_NAME,
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful AI assistant.

Answer the question only using the provided context.

If the answer is not present in the context, say:
"I don't know based on the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
def load_chatbot():

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=MODEL_NAME,
        temperature=0.3,
    )

    return llm