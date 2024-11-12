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
        splits = text_splitter.split_documents(doc)

        # Add metadata to each chunk
        for split in splits:
            split.metadata['title'] = 'Paper Title'
        all_splits.extend(splits)
    return all_splits


def index_embeddings(model, all_splits, dest_dir):
    vectorstore = Chroma.from_documents(documents=all_splits,
                                        embedding=OllamaEmbeddings(
                                            model=model),
                                        collection_metadata={
                                            "hnsw:space": "cosine"},
                                        persist_directory=dest_dir)
    return vectorstore


def ingest_pdfs(model, dataset_dir, dest_dir):
    documents = []
    for file in os.listdir(dataset_dir):
        if file.endswith(".pdf"):
            print("Indexing", file)
            file_path = os.path.join(dataset_dir, file)
            doc = load_pdf(file_path)
            documents.append(doc)
    all_splits = split_documents(documents)
    return index_embeddings(model, all_splits, dest_dir)


def load_embeddings(model, embeddings_dir):
    vectorstore = Chroma(persist_directory=embeddings_dir, embedding_function=OllamaEmbeddings(model=model))
    return vectorstore


if __name__ == "__main__":
    ingest_pdfs("dataset/GraphRAG.pdf", "llama3.2")
