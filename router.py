from rag_pipeline import retrieve_context, get_llm

llm = get_llm()


def route_question(question: str, documents_available: bool) -> str:
    """
    Decide whether to answer using:
    - document (RAG)
    - general knowledge (LLM)
    """

    # No documents uploaded
    if not documents_available:
        return "general"

    # Retrieve relevant context
    context = retrieve_context(question)

    # No relevant context found
    if not context.strip():
        return "general"

    prompt = f"""
You are an intelligent routing assistant.

Your ONLY job is to decide whether the retrieved document
contains enough information to answer the user's question.

Question:
{question}

Retrieved Context:
{context}

Rules:

1. Reply DOCUMENT if the retrieved context is enough to answer.

2. Reply GENERAL if the question is unrelated or the context is insufficient.

Return ONLY one word.

DOCUMENT

or

GENERAL
"""

    decision = llm.invoke(prompt).content.strip().upper()

    print("\n" + "=" * 60)
    print("ROUTER")
    print(f"Question : {question}")
    print(f"Decision : {decision}")
    print("=" * 60 + "\n")

    if decision == "DOCUMENT":
        return "document"

    return "general"