from langgraph.graph import StateGraph, END

from graph.state import CareerCriticState
from agents.parser_agent import ParserAgent
from agents.jobfit_agent import JobFitAgent
from agents.critic_agent import CriticAgent
from agents.writer_agent import WriterAgent

from utils.logger import get_logger

logger = get_logger("workflow")

from config import MAX_RETRIES


def route_after_critic(state: CareerCriticState) -> str:
    """Conditional edge: loop back to jobfit or proceed to writer."""
    critique = state["critique"]
    retry_count = state.get("retry_count", 0)

    if critique["verdict"] == "revise" and retry_count < MAX_RETRIES:
        logger.info("Routing decision: jobfit (revise, retry %d/%d)", retry_count, MAX_RETRIES)
        return "jobfit"

    logger.info("Routing decision: writer (verdict=%s, retry %d/%d)", critique["verdict"], retry_count, MAX_RETRIES)
    return "writer"


def build_graph():
    """Constructs and compiles the CareerCritic StateGraph."""
    parser_agent = ParserAgent()
    jobfit_agent = JobFitAgent()
    critic_agent = CriticAgent()
    writer_agent = WriterAgent()

    graph = StateGraph(CareerCriticState)

    graph.add_node("parser", parser_agent.run)
    graph.add_node("jobfit", jobfit_agent.run)
    graph.add_node("critic", critic_agent.run)
    graph.add_node("writer", writer_agent.run)

    graph.set_entry_point("parser")
    graph.add_edge("parser", "jobfit")
    graph.add_edge("jobfit", "critic")

    graph.add_conditional_edges(
        "critic",
        route_after_critic,
        {"jobfit": "jobfit", "writer": "writer"},
    )

    graph.add_edge("writer", END)

    return graph.compile()