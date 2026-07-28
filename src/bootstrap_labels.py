import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv
import json
from pydantic import ValidationError
from pathlib import Path
from tqdm import tqdm
import argparse
from src.schema import JobExtraction
from src.prompts import EXTRACTION_PROMPT

load_dotenv()

client = Anthropic(max_retries = 5)

def extract_one(job_description: str) -> JobExtraction:
    resp = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        system = EXTRACTION_PROMPT,
        messages = [{"role": "user", "content": job_description}]
    )

    raw = resp.content[0].text.strip()

    #Strips out JSON before validating incase any code fences are added
    a, b = raw.find("{"), raw.rfind("}")

    output = raw[a:b + 1]

    job_extraction = JobExtraction.model_validate_json(output)

    return job_extraction

def main(limit = None):
    df = pd.read_csv("data/raw/AI_Engineer_Job_Data.csv")
    df.columns = [c.lstrip("\ufeff") for c in df.columns] #Strips the BOM off 'company"
    if limit:
        df = df.head(limit)

    #Quick data cleaning
    df = df.drop_duplicates(subset = 'job_description')
    df['company'] = df['company'].str.strip()
    df['job_title'] = df['job_title'].str.strip()

    valid_records = []
    failed_records = []

    for idx, row in tqdm(df.iterrows(), total = len(df)):
        try:
            extracted_job = extract_one(str(row['job_description']))
            record = {"id": int(idx), "company": row["company"], "job_title": row["job_title"], **extracted_job.model_dump()} #Converts pydantic object into dictionary
            valid_records.append(record)
        except Exception as e:
            record = {"id": int(idx), "company": row["company"], "job_title": row["job_title"], "error": str(e)[:300]}
            failed_records.append(record)

    #Make sure the folder exists
    Path("data/interim").mkdir(parents = True, exist_ok = True)

    with open("data/interim/labels_draft.jsonl", "w") as f:
        for record in valid_records:
            f.write(json.dumps(record) + "\n")
    
    with open("data/interim/labels_failed.jsonl", "w") as f:
        for record in failed_records:
            f.write(json.dumps(record) + "\n")

    print(f"{len(valid_records)} job postings were sucessfully parsed")
    print(f"{len(failed_records)} job postings were unsucessfully parsed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type = int, default = None, help = "only label the first N postigns")
    args = parser.parse_args()
    main(args.limit)
        
