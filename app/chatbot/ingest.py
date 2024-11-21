from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
import os

from .utils import call_in_batches

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    doc = loader.load()
    return doc

def load_pdfs(dataset_dir):
    documents = []
    pdf_files = [file for file in os.listdir(dataset_dir) if file.endswith(".pdf")]
    for i,file in enumerate(pdf_files):
            print("({0}/{1}) Loading {2}".format(i + 1,len(pdf_files),file))
            file_path = os.path.join(dataset_dir, file)
            doc = load_pdf(file_path)
            documents.append(doc)
    return documents


def split_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600, chunk_overlap=0, add_start_index=True
    )

    def split_to_chunks(docs):
        all_splits = []
        for doc in docs:
            splits = text_splitter.split_documents(doc)

            # Add metadata to each chunk
            for split in splits:
                split.metadata['title'] = 'Paper Title'
            all_splits.extend(splits)
        return all_splits
    data = call_in_batches(split_to_chunks,docs,1)
    return data


def index_embeddings(text_chunks, model, dest_dir):
    embedding_model = OllamaEmbeddings(model=model)
    vector_store = Chroma(
        collection_metadata={"hnsw:space": "cosine"},
        persist_directory=dest_dir,
        embedding_function=embedding_model
    )
    index_func = lambda documents: vector_store.add_documents(documents=documents)
    call_in_batches(index_func,text_chunks, 500)
    return vector_store


def ingest_pdfs(dataset_dir, model, dest_dir):
    print("Loading documents")
    documents = load_pdfs(dataset_dir)
    print("Splitting documents")
    chunks = split_documents(documents)
    print("Indexing chunks")
    return index_embeddings(chunks, model, dest_dir)

def load_embeddings(model, embeddings_dir):
    vectorstore = Chroma(persist_directory=embeddings_dir, embedding_function=OllamaEmbeddings(model=model))
    return vectorstore


if __name__ == "__main__":
    ingest_pdfs("dataset/GraphRAG.pdf", "llama3.2")
