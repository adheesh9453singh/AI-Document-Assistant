from langchain.tools import tool
from rag_pipeline import load_rag_chain, load_chatbot


@tool
def rag_tool(question: str) -> str:
    """
    Answer ONLY using the uploaded document(s).

    Use for:
    - summarization
    - extraction
    - document explanation
    - resume questions
    - contract questions
    - research paper questions
    """

    rag_chain = load_rag_chain()

    return rag_chain.invoke(question)


@tool
def chat_tool(question: str) -> str:
    """
    Answer using general LLM knowledge.

    Use for:
    - coding
    - mathematics
    - reasoning
    - world knowledge
    - conversation
    - anything unrelated to uploaded documents.
    """

    chatbot = load_chatbot()

    return chatbot.invoke(question).content