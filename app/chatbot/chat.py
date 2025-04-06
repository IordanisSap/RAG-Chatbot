from KG_RAG import RAGAgent
import yaml
import os
from ..utils import validate_path


with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "r") as f:
    config = yaml.safe_load(f)
    
agent = RAGAgent(config)
# agent.index_documents(config["ingestion"]["dataset-dir"])

default_retrieval_config = {
    "topk": config["retrieval"]["topk"],
    "score_threshold": config["retrieval"]["score-threshold"]
}

async def process_message(user_message, collection, retrieval_config = None):
    if retrieval_config is None:
        retrieval_config = default_retrieval_config
    
    persist_dir = validate_path(config["retrieval"]["persist-dir"], collection)
    llmBaseRes = agent.generate(user_message)
    retrieval_config["extensions"] = ['pdf']
    llmRAGRes, RAGchunks = agent.generate_rag_persist(user_message, persist_dir, retrieval_config)
    retrieval_config["extensions"] = ['pdf','csv']
    llmKGRAGRes, KGRAGchunks = agent.generate_rag_persist(user_message, persist_dir, retrieval_config) #TODO

    llm_name = get_llm_name()
    
    response = [
        {
            "name": llm_name,
            "content": llmBaseRes
        },
        {
            "name": llm_name + "+RAG",
            "content": llmRAGRes,
            "chunks": [{
                "source": os.path.basename(x.metadata['source']),
                "page": x.metadata.get('page', 0),
                "row": x.metadata.get('row', 0),
                "content": x.page_content.split(" ")
            } for x in RAGchunks]
        },
        {
            "name": llm_name + "+KG RAG",
            "content": llmKGRAGRes,
            "chunks": [{
                "source": os.path.basename(x.metadata['source']),
                "page": x.metadata.get('page', 0),
                "row": x.metadata.get('row', 0),
                "content": x.page_content.split(" ")
            } for x in KGRAGchunks]
        },
    ]
    
    return response

async def search_query(user_message, collection, topk=5, score_threshold=0.6):
    persist_dir = validate_path(config["retrieval"]["persist-dir"], collection)
    docs = agent.retrieve_persist(user_message, persist_dir, {"topk": topk, "score_threshold": score_threshold})
    docs = [{
        "source": os.path.basename(doc.metadata['source']),
        "page": doc.metadata.get('page', 0),
        "row": doc.metadata.get('row', 0),
        "content": doc.page_content.split(" ")
    } for doc in docs]
    return docs

async def index_documents(source_dir, name):
    persist_dir = config["retrieval"]["persist-dir"]
    vectorstores = get_vectorstores()
    
    if name in vectorstores:
        print("ALREADY EXISTS")
        return
    
    os.makedirs(os.path.join(persist_dir, name), exist_ok=True)
    agent.index_documents(source_dir, os.path.join(persist_dir, name))
    
def get_vectorstores(persist_dir = None):
    if persist_dir is None:
        persist_dir = config["retrieval"]["persist-dir"]
        
    if os.path.exists(persist_dir):
        return os.listdir(persist_dir)
    return []

def get_llm_name():
    return config["generation"]["model"]


def get_tmp_dir():
    return config["tmp-dir"]

def get_doc_dir():
    return config["doc-dir"]