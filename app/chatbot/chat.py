from KG_RAG import RAGAgent
import yaml
import os



with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "r") as f:
    config = yaml.safe_load(f)
    
agent = RAGAgent(config)
# agent.index_documents(config["ingestion"]["dataset-dir"])

default_retrieval_config = {
    "topk": config["retrieval"]["topk"],
    "score_threshold": config["retrieval"]["score-threshold"]
}

async def process_message(user_message, retrieval_config = None):
    if retrieval_config is None:
        retrieval_config = default_retrieval_config
    
    llmBaseRes = agent.generate(user_message)
    llmRAGRes, RAGchunks = agent.generate_rag(user_message,retrieval_config)
    # llmKGRAGRes, KGRAGchunks = agent.generate_kgrag(user_message) #TODO

    response = {
        "base": llmBaseRes,
        "rag": {
            "response": llmRAGRes,
            "chunks": [{
                "source": os.path.basename(x.metadata['source']),
                "page": x.metadata['page'],
                "content": x.page_content.split(" ")
            } for x in RAGchunks]
        },
        # "kgrag": {
        #     "response": llmKGRAGRes,
        #     "chunks": "\n\n".join([f"{x.metadata['source']} (page {x.metadata['page']}): {x.page_content}" for x in KGRAGchunks])
        # }
    }
    
    return response

async def search_query(user_message, topk=5, score_threshold=0.6):
    docs = agent.retrieve(user_message, topk, score_threshold)
    docs = [{
        "source": os.path.basename(doc.metadata['source']),
        "page": doc.metadata['page'],
        "content": doc.page_content.split(" ")
    } for doc in docs]
    return docs

def get_llm_name():
    return config["generation"]["model"]