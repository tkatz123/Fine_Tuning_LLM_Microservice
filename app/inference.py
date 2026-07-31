import json
import os
from llama_cpp import Llama
from src.prompts import EXTRACTION_PROMPT
from src.schema import JobExtraction
from src.evaluation import validate_prediction

LLAMA_MODEL_PATH = os.environ.get("LLAMA_MODEL_PATH", "/Users/tylerkatz/gguf-work/qwen-q4km.gguf")

llm = Llama(model_path = LLAMA_MODEL_PATH, n_ctx = 4096, verbose = False)

def generate_raw(job_description, max_new_tokens = 1024):
    resp = llm.create_chat_completion(
        messages = [
            {'role': 'system', 'content': EXTRACTION_PROMPT},
            {'role': 'user', 'content': job_description}
        ],
        max_tokens = max_new_tokens,
        temperature = 0.0
    )
    return resp['choices'][0]['message']['content'].strip()

def lenient_parse(raw):
    a, b = raw.find("{"), raw.rfind("}")
    try: return json.loads(raw[a:b+1])
    except json.JSONDecodeError: return None

def extract(job_description: str) -> JobExtraction | None:

    raw = generate_raw(job_description)

    parsed = lenient_parse(raw)

    validated = validate_prediction(parsed)

    if validated is None:
        return None
    
    return JobExtraction(**validated)



