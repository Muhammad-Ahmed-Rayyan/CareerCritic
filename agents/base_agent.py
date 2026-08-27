import os
from abc import ABC, abstractmethod
from typing import Optional, Type
from pydantic import BaseModel
from langchain_groq import ChatGroq
from config import DEFAULT_MODEL
from utils.logger import get_logger
from langchain_core.messages import SystemMessage, HumanMessage


class BaseAgent(ABC):
    """
    Abstract base class for all CareerCritic agents.

    Subclasses must implement:
        - system_prompt (property): the agent's instructions to the LLM
        - build_messages(state): constructs the HumanMessage content from state
        - output_key (property): the state key this agent's result is stored under
        - output_schema (property): a Pydantic model class for structured output,
          or None if this agent produces raw text (e.g. the Writer agent)
    """

    def __init__(self, model: str = DEFAULT_MODEL, temperature: float = 0):
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        self.logger = get_logger(self.__class__.__name__)

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def output_key(self) -> str:
        raise NotImplementedError

    @property
    def output_schema(self) -> Optional[Type[BaseModel]]:
        """Override with a Pydantic model for structured output. None = raw text output."""
        return None

    @abstractmethod
    def build_messages(self, state: dict) -> list:
        raise NotImplementedError

    def _call_llm(self, messages: list):
        """
        Calls the LLM. If output_schema is set, binds it via
        with_structured_output() using JSON mode and returns a validated
        Pydantic instance. Otherwise returns the raw text response.
        """
        self.logger.info("Calling LLM (structured=%s)", self.output_schema is not None)

        if self.output_schema is not None:
            structured_llm = self.llm.with_structured_output(
                self.output_schema, method="json_mode"
            )
            try:
                result = structured_llm.invoke(messages)
                self.logger.info("LLM call succeeded, output validated against schema")
                return result
            except Exception as e:
                self.logger.error("Structured output validation failed: %s", e)
                raise
        else:
            response = self.llm.invoke(messages)
            self.logger.info("LLM call succeeded (raw text output)")
            return response.content.strip()


    def run(self, state: dict) -> dict:
        """
        Executes this agent as a LangGraph node.
        Returns a partial state update: {output_key: result}.
        """
        self.logger.info("Running agent, writing to state key '%s'", self.output_key)

        messages = [
            SystemMessage(content=self.system_prompt),
            *self.build_messages(state),
        ]
        result = self._call_llm(messages)

        if self.output_schema is not None:
            result = result.model_dump()

        self.logger.info("Agent finished successfully")
        return {self.output_key: result}