from pydantic import BaseModel, Field
from typing import List


class ParsedResumeSchema(BaseModel):
    skills: List[str] = Field(description="List of technical and soft skills found in the resume")
    experience: List[str] = Field(description="Short bullet summaries of work experience or roles")
    education: List[str] = Field(description="Degree, institution, and year entries")
    projects: List[str] = Field(description="Short bullet summaries of notable projects")
    summary: str = Field(description="A 1-2 sentence overview of the candidate's profile")


class FitAnalysisSchema(BaseModel):
    fit_score: int = Field(ge=0, le=100, description="Overall fit score between 0 and 100")
    matched_skills: List[str] = Field(description="Skills present in both resume and job description")
    missing_skills: List[str] = Field(description="Skills required by the job but absent from the resume")
    feedback_draft: str = Field(description="Specific, actionable feedback on the candidate's fit")


class CritiqueSchema(BaseModel):
    verdict: str = Field(description="Either 'pass' or 'revise'")
    reasoning: str = Field(description="One sentence explaining the verdict")