from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


def get_llm():
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def generate_answer(llm, query, context):
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a customer support assistant.

Use ONLY the context below to answer.

Context:
{context}

Question:
{question}

If answer is not found, say "I don't know".
"""
    )

    chain = prompt | llm
    response = chain.invoke({
        "context": context,
        "question": query
    })

    return response.content
