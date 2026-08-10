from typing import TypedDict, List, Optional


class ParsedResume(TypedDict):
    skills: List[str]
    experience: List[str]      # short bullet summaries of roles/projects
    education: List[str]
    projects: List[str]
    summary: str                # 1-2 line overview of the candidate


class FitAnalysis(TypedDict):
    fit_score: int               # 0-100
    matched_skills: List[str]
    missing_skills: List[str]
    feedback_draft: str          # narrative feedback, may get revised


class Critique(TypedDict):
    verdict: str                 # "pass" or "revise"
    reasoning: str                # why the critic made this call


class CareerCriticState(TypedDict):
    # Inputs
    resume_text: str
    job_description: str

    # Agent outputs (populated as the graph runs)
    parsed_resume: Optional[ParsedResume]
    fit_analysis: Optional[FitAnalysis]
    critique: Optional[Critique]
    final_report: Optional[str]

    # Control flow
    retry_count: int