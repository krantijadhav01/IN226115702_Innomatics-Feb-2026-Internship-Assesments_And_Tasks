import os
from dotenv import load_dotenv

from modules.loader import load_pdf
from modules.chunker import split_docs
from modules.embedder import get_embedding
from modules.retriever import create_vectorstore, get_retriever
from modules.llm import get_llm
from graph.workflow import build_graph

load_dotenv()

def setup():
    print("📄 Loading PDF...")
    docs = load_pdf("data/knowledge.pdf")

    print("✂️ Chunking...")
    chunks = split_docs(docs)

    print("🧠 Embedding...")
    embedding = get_embedding()

    print("🗄️ Creating vector DB...")
    vectordb = create_vectorstore(chunks, embedding)

    retriever = get_retriever(vectordb)

    llm = get_llm()

    graph = build_graph(retriever, llm)

    return graph


def main():
    graph = setup()

    print("\n🤖 RAG Customer Support Assistant Ready!")
    print("Type 'exit' to quit\n")

    while True:
        query = input("🧑 You: ")

        if query.lower() == "exit":
            break

        result = graph.invoke({
            "query": query
        })

        print(f"\n🤖 Bot: {result['answer']}\n")


if __name__ == "__main__":
    main()
