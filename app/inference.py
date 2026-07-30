import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.prompts import EXTRACTION_PROMPT
from src.schema import JobExtraction
from src.evaluation import validate_prediction

MODEL_ID = "tkatz123/qwen2.5-3b-job-extraction-merged"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype = torch.bfloat16)
model.eval()

def generate_raw(job_description, max_new_tokens = 1024):
    msgs = [{"role":"system","content":EXTRACTION_PROMPT},{"role":"user","content":job_description}]

    text = tokenizer.apply_chat_template(
        msgs, 
        add_generation_prompt=True, 
        tokenize=False
        )

    inp = tokenizer(text, return_tensors="pt")

    out = model.generate(
        **inp, max_new_tokens=max_new_tokens, 
        do_sample=False, 
        pad_token_id=tokenizer.eos_token_id
        )

    return tokenizer.decode(out[0][inp["input_ids"].shape[-1]:], skip_special_tokens=True).strip()

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



