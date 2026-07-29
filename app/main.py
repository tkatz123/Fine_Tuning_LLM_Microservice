from fastapi import FastAPI
from pydantic import BaseModel
from src.schema import JobExtraction

app = FastAPI(title = "Job Posting Extractor")
1
class ExtractionRequest(BaseModel):
    job_description: str

def extract(job_description: str) -> JobExtraction:
    return JobExtraction(
        required_skills = ["stub"],
        tech_stack = None,
        seniority = "mid",
        avg_comp_range = None 
    )

@app.post("/extract", response_model = JobExtraction)
def extract_endpoint(req: ExtractionRequest):
    return extract(req.job_description)

@app.get("/health")
def health():
    return {"status": "ok"}

