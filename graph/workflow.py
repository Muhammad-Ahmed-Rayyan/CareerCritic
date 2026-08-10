from langgraph.graph import StateGraph, END

from graph.state import CareerCriticState
from agents.parser_agent import parser_node
from agents.jobfit_agent import jobfit_node
from agents.critic_agent import critic_node
from agents.writer_agent import writer_node

MAX_RETRIES = 2


def route_after_critic(state: CareerCriticState) -> str:
    """
    Conditional edge: decide whether to loop back to jobfit_node
    or proceed to writer_node.
    """
    critique = state["critique"]
    retry_count = state.get("retry_count", 0)

    if critique["verdict"] == "revise" and retry_count < MAX_RETRIES:
        return "jobfit"
    return "writer"


def build_graph():
    """Constructs and compiles the CareerCritic StateGraph."""
    graph = StateGraph(CareerCriticState)

    graph.add_node("parser", parser_node)
    graph.add_node("jobfit", jobfit_node)
    graph.add_node("critic", critic_node)
    graph.add_node("writer", writer_node)

    graph.set_entry_point("parser")
    graph.add_edge("parser", "jobfit")
    graph.add_edge("jobfit", "critic")

    graph.add_conditional_edges(
        "critic",
        route_after_critic,
        {
            "jobfit": "jobfit",   # loop back for a revision
            "writer": "writer",  # good enough, proceed
        },
    )

    graph.add_edge("writer", END)

    return graph.compile()