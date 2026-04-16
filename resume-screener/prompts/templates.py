from langchain_core.prompts import ChatPromptTemplate

# Skill Extraction & Matching Template
SCREENER_PROMPT = """
You are an expert HR Data Scientist. Your task is to evaluate a candidate's Resume against a Job Description.

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Evaluation Rules:
1. Extract key skills, tools, and years of experience.
2. Compare them against the requirements.
3. Do NOT assume skills not explicitly mentioned.
4. Provide a Fit Score (0-100) based on alignment.

Output the result strictly in this JSON format:
{{
    "extracted_skills": ["skill1", "skill2"],
    "experience_summary": "Summary of years and roles",
    "fit_score": 85,
    "explanation": "Detailed reasoning for the score"
}}
"""

screening_prompt_template = ChatPromptTemplate.from_template(SCREENER_PROMPT)