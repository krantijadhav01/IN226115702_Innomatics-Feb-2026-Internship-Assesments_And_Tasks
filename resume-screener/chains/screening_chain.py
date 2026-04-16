from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from prompts.templates import screening_prompt_template

def get_screening_chain():
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Initialize Parser
    parser = JsonOutputParser()
    
    # LCEL Chain Construction
    chain = screening_prompt_template | llm | parser
    
    return chain