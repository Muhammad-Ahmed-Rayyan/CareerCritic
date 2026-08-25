from langchain_core.messages import HumanMessage, SystemMessage
from agents.base_agent import BaseAgent
from config import WRITER_TEMPERATURE


class WriterAgent(BaseAgent):
    """Compiles the final Markdown fit report. Output is plain text, not JSON."""

    def __init__(self):
        super().__init__(temperature=WRITER_TEMPERATURE)

    @property
    def system_prompt(self) -> str:
        return """You are a career report writer. Given a candidate's \
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

    @property
    def output_key(self) -> str:
        return "final_report"

    @property
    def fallback_output(self) -> dict:
        return {}  # unused, writer doesn't parse JSON

    def build_messages(self, state: dict) -> list:
        parsed_resume = state["parsed_resume"]
        fit_analysis = state["fit_analysis"]
        content = (
            f"Candidate summary: {parsed_resume.get('summary', '')}\n\n"
            f"Fit score: {fit_analysis['fit_score']}\n"
            f"Matched skills: {', '.join(fit_analysis['matched_skills'])}\n"
            f"Missing skills: {', '.join(fit_analysis['missing_skills'])}\n\n"
            f"Feedback draft: {fit_analysis['feedback_draft']}"
        )
        return [HumanMessage(content=content)]

    def run(self, state: dict) -> dict:
        """Overrides base run() because output is raw Markdown, not JSON —
        another example of polymorphism across the agent hierarchy."""
        messages = [
            SystemMessage(content=self.system_prompt),
            *self.build_messages(state),
        ]
        response = self.llm.invoke(messages)
        return {self.output_key: response.content.strip()}