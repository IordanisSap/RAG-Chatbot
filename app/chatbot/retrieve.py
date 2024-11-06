from langchain_core.vectorstores import VectorStore

def retrieve(vectorstore: VectorStore, prompt: str):
    retriever = vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 6, "score_threshold": 0.6})
    retrieved_docs = retriever.invoke(prompt)
    return retrieved_docs