import json
import os
from abc import ABC, abstractmethod
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


class BaseAgent(ABC):
    """
    Abstract base class for all CareerCritic agents.

    Subclasses must implement:
        - system_prompt (property): the agent's instructions to the LLM
        - build_messages(state): constructs the HumanMessage content from state
        - output_key (property): the state key this agent's result is stored under
        - fallback_output (property): a safe default if JSON parsing fails
    """

    def __init__(self, model: str = "openai/gpt-oss-120b", temperature: float = 0):
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=os.environ.get("GROQ_API_KEY"),
        )

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Each agent defines its own instructions to the LLM."""
        raise NotImplementedError

    @property
    @abstractmethod
    def output_key(self) -> str:
        """The state dict key this agent writes its result to."""
        raise NotImplementedError

    @property
    @abstractmethod
    def fallback_output(self) -> dict:
        """Safe default returned if the LLM output can't be parsed as JSON."""
        raise NotImplementedError

    @abstractmethod
    def build_messages(self, state: dict) -> list:
        """Builds the list of LangChain messages sent to the LLM for this agent."""
        raise NotImplementedError

    def _clean_json_fences(self, raw_content: str) -> str:
        """Strips markdown code fences the LLM sometimes wraps JSON in."""
        content = raw_content.strip()
        if content.startswith("```"):
            content = content.strip("`")
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        return content

    def _call_llm(self, messages: list) -> dict:
        """Calls the LLM and parses its response as JSON, with a safe fallback."""
        response = self.llm.invoke(messages)
        cleaned = self._clean_json_fences(response.content)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return self.fallback_output

    def run(self, state: dict) -> dict:
        """
        Executes this agent as a LangGraph node.
        Returns a partial state update: {output_key: parsed_result}.
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            *self.build_messages(state),
        ]
        result = self._call_llm(messages)
        return {self.output_key: result}