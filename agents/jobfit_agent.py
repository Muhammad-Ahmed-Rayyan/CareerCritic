import json
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import CareerCriticState

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=os.environ.get("GROQ_API_KEY"),
)

SYSTEM_PROMPT = """You are a career advisor comparing a candidate's resume \
against a job description. Respond ONLY with valid JSON, no preamble, no \
markdown fences.

Return JSON in exactly this shape:
{
  "fit_score": <integer 0-100>,
  "matched_skills": ["skill present in both resume and job", ...],
  "missing_skills": ["skill required by job but absent from resume", ...],
  "feedback_draft": "A specific, actionable paragraph of feedback on how \
well this candidate fits the role, and what to improve."
}

Be specific. Avoid generic statements like "improve your skills" — name \
exact skills, tools, or experience gaps."""


def jobfit_node(state: CareerCriticState) -> dict:
    """LangGraph node: produces fit_analysis from parsed_resume + job_description."""
    parsed_resume = state["parsed_resume"]
    job_description = state["job_description"]

    # If the critic sent us back for a retry, include that feedback as context
    critique = state.get("critique")
    revision_note = ""
    if critique and critique.get("verdict") == "revise":
        revision_note = (
            f"\n\nNote: a previous draft of this feedback was rejected as "
            f"too generic. Reason: {critique['reasoning']}. "
            f"Make this version more specific and evidence-based."
        )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=(
                f"Parsed resume:\n{json.dumps(parsed_resume, indent=2)}\n\n"
                f"Job description:\n{job_description}"
                f"{revision_note}"
            )
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
        fit_analysis = json.loads(raw_content)
    except json.JSONDecodeError:
        fit_analysis = {
            "fit_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "feedback_draft": "Could not generate fit analysis automatically.",
        }

    return {"fit_analysis": fit_analysis}