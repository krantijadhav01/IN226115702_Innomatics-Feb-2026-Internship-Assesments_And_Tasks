from langchain_community.vectorstores import Chroma

def create_vectorstore(docs, embedding):
    vectordb = Chroma.from_documents(
        docs,
        embedding,
        persist_directory="./chroma_db"
    )
    return vectordb

def get_retriever(vectordb):
    return vectordb.as_retriever(search_kwargs={"k": 3})
