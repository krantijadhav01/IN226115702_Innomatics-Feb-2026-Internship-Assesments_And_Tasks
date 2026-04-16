import os
from dotenv import load_dotenv
from chains.screening_chain import get_screening_chain

load_dotenv()

# Sample Data
job_desc = "Data Scientist: Requires 3+ years experience in Python, SQL, and LangChain. Knowledge of LLMs and RAG is a must."

resumes = {
    "Strong": "John Doe: 5 years experience as Data Scientist. Expert in Python, SQL, and LangChain. Built multiple RAG apps using LLMs.",
    "Average": "Jane Smith: 2 years experience in Data Analysis. Proficient in Python and SQL. Limited exposure to LangChain.",
    "Weak": "Bob White: 10 years experience in Retail Management. Expert in Team Leadership and Inventory. No coding experience."
}

def run_screening():
    chain = get_screening_chain()
    
    print("--- Starting AI Resume Screening ---")
    
    for category, resume in resumes.items():
        print(f"\nProcessing {category} Candidate...")
        
        # Invoke the chain
        result = chain.invoke({
            "job_description": job_desc,
            "resume_text": resume
        })
        
        print(f"Score: {result['fit_score']}/100")
        print(f"Reasoning: {result['explanation']}")

if __name__ == "__main__":
    run_screening()