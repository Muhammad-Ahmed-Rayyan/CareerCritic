import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import CareerCriticState

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.4,
    api_key=os.environ.get("GROQ_API_KEY"),
)

SYSTEM_PROMPT = """You are a career report writer. Given a candidate's \
parsed resume and a fit analysis against a job description, write a \
clear, well-structured Markdown report for the candidate.

Structure:
## Overall Fit Score
## Matched Skills
## Skill Gaps
## Detailed Feedback
## Suggested Next Steps (3-5 concrete, actionable bullet points)

Keep it encouraging but honest. No preamble before the report, output \
Markdown only."""


def writer_node(state: CareerCriticState) -> dict:
    """LangGraph node: produces the final_report markdown."""
    parsed_resume = state["parsed_resume"]
    fit_analysis = state["fit_analysis"]

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=(
                f"Candidate summary: {parsed_resume.get('summary', '')}\n\n"
                f"Fit score: {fit_analysis['fit_score']}\n"
                f"Matched skills: {', '.join(fit_analysis['matched_skills'])}\n"
                f"Missing skills: {', '.join(fit_analysis['missing_skills'])}\n\n"
                f"Feedback draft: {fit_analysis['feedback_draft']}"
            )
        ),
    ]

    response = llm.invoke(messages)
    final_report = response.content.strip()

    return {"final_report": final_report}