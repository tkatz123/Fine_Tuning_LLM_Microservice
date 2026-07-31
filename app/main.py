from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.schema import JobExtraction
from app.inference import extract
import logging
import time

logging.basicConfig(level = logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI(title = "Job Posting Extractor")
class ExtractionRequest(BaseModel):
    job_description: str

@app.middleware("http")
async def log_requests(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info(f"{request.method} {request.url.path} {response.status_code} {elapsed_ms:.0f}ms")
    return response

'''
#Used for testing endpoint
def extract(job_description: str) -> JobExtraction:
    return JobExtraction(
        required_skills = ["stub"],
        tech_stack = None,
        seniority = "mid",
        avg_comp_range = None 
    )
'''

@app.post("/extract", response_model = JobExtraction)
def extract_endpoint(req: ExtractionRequest):
    
    result = extract(req.job_description)

    #Handles error if pydantic check returns none
    if result is None:
        raise HTTPException(status_code = 422, detail = "Could not extract structured data from this posting.")
    
    return result

@app.get("/health")
def health():
    return {"status": "ok"}



