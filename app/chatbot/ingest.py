from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
import os

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    doc = loader.load()
    return doc


def split_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300, chunk_overlap=0, add_start_index=True
    )
    all_splits = []
    for doc in docs:
        all_splits.extend(text_splitter.split_documents(doc))
    return all_splits

def index_embeddings(all_splits, model):
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=OllamaEmbeddings(model=model), collection_metadata={"hnsw:space": "cosine"})
    return vectorstore

def ingest_pdfs(dataset_dir, model):
    documents = []
    for file in os.listdir(dataset_dir):
        if file.endswith(".pdf"):
            print("Indexing", file)
            file_path = os.path.join(dataset_dir, file)
            doc = load_pdf(file_path)
            documents.append(doc)
    all_splits = split_documents(documents)
    return index_embeddings(all_splits, model)


if __name__ == "__main__":
    ingest_pdfs("dataset/GraphRAG.pdf", "llama3.2")