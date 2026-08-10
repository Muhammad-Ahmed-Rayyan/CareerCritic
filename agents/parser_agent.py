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

SYSTEM_PROMPT = """You are a resume parsing assistant. Extract structured \
information from the resume text provided. Respond ONLY with valid JSON, \
no preamble, no markdown fences, no explanation.

Return JSON in exactly this shape:
{
  "skills": ["skill1", "skill2", ...],
  "experience": ["short bullet summary of role/project 1", ...],
  "education": ["degree, institution, year", ...],
  "projects": ["short bullet summary of project 1", ...],
  "summary": "1-2 sentence overview of the candidate's profile"
}
"""


def parser_node(state: CareerCriticState) -> dict:
    """LangGraph node: parses resume_text into a structured ParsedResume."""
    resume_text = state["resume_text"]

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Resume text:\n\n{resume_text}"),
    ]

    response = llm.invoke(messages)
    raw_content = response.content.strip()

    # Defensive cleanup in case the model wraps output in markdown fences
    if raw_content.startswith("```"):
        raw_content = raw_content.strip("`")
        if raw_content.startswith("json"):
            raw_content = raw_content[4:]
        raw_content = raw_content.strip()

    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError:
        # Fallback: don't crash the graph, surface a minimal structure instead
        parsed = {
            "skills": [],
            "experience": [],
            "education": [],
            "projects": [],
            "summary": "Could not parse resume automatically.",
        }

    return {"parsed_resume": parsed}