from langgraph.graph import StateGraph
from typing import TypedDict

from modules.llm import generate_answer
from hitl.human import human_intervention


class GraphState(TypedDict):
    query: str
    context: str
    answer: str
    escalate: bool


def process_node(state, retriever, llm):
    query = state["query"]

    docs = retriever.invoke(query)

    if not docs:
        return {
            "context": "",
            "answer": "",
            "escalate": True
        }

    context = "\n".join([doc.page_content for doc in docs])

    answer = generate_answer(llm, query, context)

    # Simple confidence logic
    if "I don't know" in answer or len(context) < 20:
        escalate = True
    else:
        escalate = False

    return {
        "context": context,
        "answer": answer,
        "escalate": escalate
    }


def route_node(state):
    if state["escalate"]:
        return "hitl"
    return "output"


def hitl_node(state):
    response = human_intervention(state["query"])
    return {"answer": response}


def output_node(state):
    return state


def build_graph(retriever, llm):
    builder = StateGraph(GraphState)

    builder.add_node("process", lambda state: process_node(state, retriever, llm))
    builder.add_node("hitl", hitl_node)
    builder.add_node("output", output_node)

    builder.set_entry_point("process")

    builder.add_conditional_edges(
        "process",
        route_node,
        {
            "hitl": "hitl",
            "output": "output"
        }
    )

    builder.add_edge("hitl", "output")

    return builder.compile()
