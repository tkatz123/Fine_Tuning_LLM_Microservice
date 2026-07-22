from pydantic import BaseModel
from enum import Enum

class Seniority(str, Enum):
    junior = "junior"
    mid = "mid"
    senior = "senior"
    lead = "lead"
    unknown = "unknown"

class JobExtraction(BaseModel):
    required_skills: list[str]
    tech_stack: list[str] | None = None
    seniority: Seniority
    avg_comp_range: int | None = None
