from langchain_core.messages import HumanMessage
from agents.base_agent import BaseAgent


class CriticAgent(BaseAgent):
    """Judges whether feedback is specific/actionable; drives the revision loop."""

    @property
    def system_prompt(self) -> str:
        return """You are a strict quality reviewer for career feedback. \
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

    @property
    def output_key(self) -> str:
        return "critique"

    @property
    def fallback_output(self) -> dict:
        return {"verdict": "pass", "reasoning": "Could not parse critique; defaulting to pass."}

    def build_messages(self, state: dict) -> list:
        feedback = state["fit_analysis"]["feedback_draft"]
        return [HumanMessage(content=f"Feedback draft to review:\n\n{feedback}")]

    def run(self, state: dict) -> dict:
        """Overrides base run() to also increment retry_count — an example
        of polymorphism, since this agent's node behavior differs slightly
        from the shared default."""
        base_result = super().run(state)
        base_result["retry_count"] = state.get("retry_count", 0) + 1
        return base_result