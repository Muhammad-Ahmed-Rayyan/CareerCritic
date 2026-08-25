import json
from langchain_core.messages import HumanMessage
from agents.base_agent import BaseAgent
from graph.schemas import FitAnalysisSchema


class JobFitAgent(BaseAgent):
    """Scores resume-to-job fit and drafts feedback, revising on critic rejection."""

    def __init__(self):
        super().__init__(temperature=0.3)

    @property
    def system_prompt(self) -> str:
        return """You are a career advisor comparing a candidate's resume \
against a job description. Respond in JSON format matching exactly this schema:

{
  "fit_score": <integer 0-100>,
  "matched_skills": ["skill present in both resume and job", ...],
  "missing_skills": ["skill required by job but absent from resume", ...],
  "feedback_draft": "A single paragraph of specific, actionable feedback \
on how well this candidate fits the role, and what to improve."
}

IMPORTANT: use exactly these four field names. Do not add extra fields \
like "strengths", "gaps", or "recommendations". feedback_draft must be a \
single string paragraph, not a list.

Be specific in feedback_draft. Avoid generic statements like "improve your \
skills" — name exact skills, tools, or experience gaps."""

    @property
    def output_key(self) -> str:
        return "fit_analysis"

    @property
    def output_schema(self):
        return FitAnalysisSchema

    def build_messages(self, state: dict) -> list:
        critique = state.get("critique")
        revision_note = ""
        if critique and critique.get("verdict") == "revise":
            revision_note = (
                f"\n\nNote: a previous draft of this feedback was rejected as "
                f"too generic. Reason: {critique['reasoning']}. "
                f"Make this version more specific and evidence-based."
            )

        content = (
            f"Parsed resume:\n{json.dumps(state['parsed_resume'], indent=2)}\n\n"
            f"Job description:\n{state['job_description']}"
            f"{revision_note}"
        )
        return [HumanMessage(content=content)]