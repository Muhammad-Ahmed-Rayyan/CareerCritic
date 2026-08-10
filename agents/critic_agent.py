import json
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import CareerCriticState

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.environ.get("GROQ_API_KEY"),
)

SYSTEM_PROMPT = """You are a strict quality reviewer for career feedback. \
Judge whether the feedback_draft below is specific, actionable, and backed \
by concrete skills/evidence — not generic advice.

Respond ONLY with valid JSON, no preamble, no markdown fences:
{
  "verdict": "pass" or "revise",
  "reasoning": "one sentence explaining your verdict"
}

Mark "revise" if the feedback is vague, generic, or doesn't reference \
specific skills or gaps. Mark "pass" only if it clearly names concrete \
skills, tools, or experience."""


def critic_node(state: CareerCriticState) -> dict:
    """LangGraph node: critiques fit_analysis['feedback_draft']."""
    fit_analysis = state["fit_analysis"]
    retry_count = state.get("retry_count", 0)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"Feedback draft to review:\n\n{fit_analysis['feedback_draft']}"
        ),
    ]

    response = llm.invoke(messages)
    raw_content = response.content.strip()

    if raw_content.startswith("```"):
        raw_content = raw_content.strip("`")
        if raw_content.startswith("json"):
            raw_content = raw_content[4:]
        raw_content = raw_content.strip()

    try:
        critique = json.loads(raw_content)
    except json.JSONDecodeError:
        critique = {"verdict": "pass", "reasoning": "Could not parse critique; defaulting to pass."}

    return {
        "critique": critique,
        "retry_count": retry_count + 1,
    }