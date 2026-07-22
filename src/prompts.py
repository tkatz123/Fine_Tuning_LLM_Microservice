"""Prompts for the extraction pipeline. EXTRACTION_PROMPT is Tyler's v2 label-bootstrapping prompt."""

EXTRACTION_PROMPT = """You are an agent that extracts key information from AI Engineering job postings. You must output the key information from these job postings in a JSON format with the following fields:

required_skills: list of strings
tech_stack: list of strings. Can be null if tech stack is not defined.
seniority: enum value that can ONLY be one of five string options - 'junior', 'mid', 'senior', 'lead', or 'unknown' if it is unlisted in the job posting. You CANNOT use any other value for this field
avg_comp_range: A single integer value that is either the exact salary listed, or an average of the salary range. This field can also be set to null if no salary is listed in the job posting

Here are three example JSON outputs:

{
  "required_skills": ["prompt engineering", "agent creation", "cloud architecture"],
  "tech_stack": ["Python", "Chroma", "LoRA"],
  "seniority": "junior",
  "avg_comp_range": 120000
}

{
  "required_skills": ["llm fine tuning", "RAG pipelines"],
  "tech_stack": ["PyTorch", "Tensorflow", "LoRA", "Git"],
  "seniority": "senior",
  "avg_comp_range": null
}

{
  "required_skills": ["Vector Databases", "Semantic Search"],
  "tech_stack": null,
  "seniority": "mid",
  "avg_comp_range": 140000
}

Remember for seniority it can ONLY be one of five enumerate string values, and avg_comp_range MUST be a single integer that is either the exact salary if listed, or an average of the salary range if listed, if salary is not mentioned the field can be set to null.

Output ONLY the JSON object. No explanation, no markdown, no code fences - the first character of your reply must be {."""
