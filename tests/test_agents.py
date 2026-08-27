import pytest
from agents.parser_agent import ParserAgent
from agents.jobfit_agent import JobFitAgent
from agents.critic_agent import CriticAgent
from agents.writer_agent import WriterAgent
from graph.schemas import ParsedResumeSchema, FitAnalysisSchema, CritiqueSchema


def test_parser_agent_has_correct_output_key():
    agent = ParserAgent()
    assert agent.output_key == "parsed_resume"


def test_parser_agent_uses_correct_schema():
    agent = ParserAgent()
    assert agent.output_schema is ParsedResumeSchema


def test_parser_agent_builds_messages_from_resume_text():
    agent = ParserAgent()
    state = {"resume_text": "Experienced Python developer."}
    messages = agent.build_messages(state)
    assert len(messages) == 1
    assert "Experienced Python developer." in messages[0].content


def test_jobfit_agent_has_correct_output_key():
    agent = JobFitAgent()
    assert agent.output_key == "fit_analysis"


def test_jobfit_agent_uses_correct_schema():
    agent = JobFitAgent()
    assert agent.output_schema is FitAnalysisSchema


def test_jobfit_agent_includes_revision_note_when_critic_says_revise():
    """When the critic previously rejected feedback, JobFitAgent's prompt
    should include that context so the retry is actually informed."""
    agent = JobFitAgent()
    state = {
        "parsed_resume": {"skills": ["Python"]},
        "job_description": "Looking for a Python developer.",
        "critique": {"verdict": "revise", "reasoning": "too generic"},
    }
    messages = agent.build_messages(state)
    assert "rejected" in messages[0].content
    assert "too generic" in messages[0].content


def test_jobfit_agent_omits_revision_note_on_first_pass():
    """On the first attempt (no critique yet), no revision note should appear."""
    agent = JobFitAgent()
    state = {
        "parsed_resume": {"skills": ["Python"]},
        "job_description": "Looking for a Python developer.",
        "critique": None,
    }
    messages = agent.build_messages(state)
    assert "rejected" not in messages[0].content


def test_critic_agent_uses_correct_schema():
    agent = CriticAgent()
    assert agent.output_schema is CritiqueSchema


def test_writer_agent_has_no_structured_schema():
    """Writer produces raw Markdown, not JSON — output_schema should be None."""
    agent = WriterAgent()
    assert agent.output_schema is None


def test_writer_agent_output_key():
    agent = WriterAgent()
    assert agent.output_key == "final_report"