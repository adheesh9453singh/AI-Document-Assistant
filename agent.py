from typing import TypedDict

from langgraph.graph import StateGraph, END

from tools import rag_tool, chat_tool
from router import route_question


class AgentState(TypedDict):
    question: str
    documents_available: bool
    route: str
    answer: str


def router_node(state: AgentState):
    route = route_question(
        state["question"],
        state["documents_available"],
    )

    return {"route": route}


def document_node(state: AgentState):
    answer = rag_tool.invoke(state["question"])

    # Handle AIMessage if returned
    if hasattr(answer, "content"):
        answer = answer.content

    return {"answer": str(answer)}


def general_node(state: AgentState):
    answer = chat_tool.invoke(state["question"])

    # Handle AIMessage if returned
    if hasattr(answer, "content"):
        answer = answer.content

    return {"answer": str(answer)}


# ==========================
# Build Graph
# ==========================

builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("document", document_node)
builder.add_node("general", general_node)

builder.set_entry_point("router")

builder.add_conditional_edges(
    "router",
    lambda state: state["route"],
    {
        "document": "document",
        "general": "general",
    },
)

builder.add_edge("document", END)
builder.add_edge("general", END)

graph = builder.compile()


# ==========================
# Main Agent Function
# ==========================

def ask_agent(question: str, documents_available: bool):

    result = graph.invoke(
        {
            "question": question,
            "documents_available": documents_available,
        }
    )

    return {
        "answer": result.get("answer", ""),
        "source": (
            "Document"
            if result.get("route") == "document"
            else "General AI"
        ),
    }