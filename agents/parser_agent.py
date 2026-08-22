from langchain_core.messages import HumanMessage
from agents.base_agent import BaseAgent


class ParserAgent(BaseAgent):
    """Extracts structured resume data (skills, experience, education, projects)."""

    @property
    def system_prompt(self) -> str:
        return """You are a resume parsing assistant. Extract structured \
information from the resume text provided. Respond ONLY with valid JSON, \
no preamble, no markdown fences, no explanation.

Return JSON in exactly this shape:
{
  "skills": ["skill1", "skill2", ...],
  "experience": ["short bullet summary of role/project 1", ...],
  "education": ["degree, institution, year", ...],
  "projects": ["short bullet summary of project 1", ...],
  "summary": "1-2 sentence overview of the candidate's profile"
}"""

    @property
    def output_key(self) -> str:
        return "parsed_resume"

    @property
    def fallback_output(self) -> dict:
        return {
            "skills": [],
            "experience": [],
            "education": [],
            "projects": [],
            "summary": "Could not parse resume automatically.",
        }

    def build_messages(self, state: dict) -> list:
        return [HumanMessage(content=f"Resume text:\n\n{state['resume_text']}")]