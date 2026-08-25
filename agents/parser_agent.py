from langchain_core.messages import HumanMessage
from agents.base_agent import BaseAgent
from graph.schemas import ParsedResumeSchema


class ParserAgent(BaseAgent):
    """Extracts structured resume data (skills, experience, education, projects)."""

    @property
    def system_prompt(self) -> str:
        return """You are a resume parsing assistant. Extract structured \
information from the resume text provided. Respond in JSON format matching \
exactly this schema:

{
  "skills": ["skill1", "skill2", ...],
  "experience": ["one flat string per role, e.g. 'AI/ML Intern at X, did Y and Z'", ...],
  "education": ["one flat string per entry, e.g. 'BS AI, SZABIST, 2023-Present'", ...],
  "projects": ["one flat string per project, e.g. 'ProjectName: what it does and how'", ...],
  "summary": "1-2 sentence overview of the candidate's profile"
}

IMPORTANT: every item in skills, experience, education, and projects must \
be a single flat string, NOT a nested object. Do not include contact info, \
achievements, or activities — only the five fields above."""

    @property
    def output_key(self) -> str:
        return "parsed_resume"

    @property
    def output_schema(self):
        return ParsedResumeSchema

    def build_messages(self, state: dict) -> list:
        return [HumanMessage(content=f"Resume text:\n\n{state['resume_text']}")]