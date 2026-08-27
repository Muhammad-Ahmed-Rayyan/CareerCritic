from graph.workflow import route_after_critic
from config import MAX_RETRIES


def test_routes_to_jobfit_when_revise_and_under_retry_limit():
    """Critic says revise, retries below cap -> should loop back to jobfit."""
    state = {
        "critique": {"verdict": "revise", "reasoning": "too vague"},
        "retry_count": 1,
    }
    assert route_after_critic(state) == "jobfit"


def test_routes_to_writer_when_pass():
    """Critic says pass -> should proceed to writer regardless of retry count."""
    state = {
        "critique": {"verdict": "pass", "reasoning": "specific enough"},
        "retry_count": 0,
    }
    assert route_after_critic(state) == "writer"


def test_routes_to_writer_when_revise_but_retry_limit_reached():
    """Critic says revise, but retries already at cap -> must proceed to writer
    to guarantee the graph terminates instead of looping forever."""
    state = {
        "critique": {"verdict": "revise", "reasoning": "still vague"},
        "retry_count": MAX_RETRIES,
    }
    assert route_after_critic(state) == "writer"


def test_routes_to_writer_when_revise_beyond_retry_limit():
    """Defensive case: retry count somehow exceeds cap -> still must terminate."""
    state = {
        "critique": {"verdict": "revise", "reasoning": "still vague"},
        "retry_count": MAX_RETRIES + 5,
    }
    assert route_after_critic(state) == "writer"


def test_missing_retry_count_defaults_safely():
    """If retry_count is somehow missing from state, should default to 0
    and still route correctly (loop, since 0 < MAX_RETRIES)."""
    state = {"critique": {"verdict": "revise", "reasoning": "vague"}}
    assert route_after_critic(state) == "jobfit"