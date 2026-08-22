"""
JobFit Agent — compares parsed resume against a job description
and produces a fit analysis with a feedback draft.
"""

import json
from langchain_core.messages import HumanMessage
from agents.base_agent import BaseAgent


class JobFitAgent(BaseAgent):
    """Scores resume-to-job fit and drafts feedback, revising on critic rejection."""

    def __init__(self):
        super().__init__(temperature=0.3)

    @property
    def system_prompt(self) -> str:
        return """You are a career advisor comparing a candidate's resume \
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

    @property
    def output_key(self) -> str:
        return "fit_analysis"

    @property
    def fallback_output(self) -> dict:
        return {
            "fit_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "feedback_draft": "Could not generate fit analysis automatically.",
        }

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