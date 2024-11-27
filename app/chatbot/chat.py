from KG_RAG import RAGAgent
import yaml
import os



with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "r") as f:
    config = yaml.safe_load(f)
    
agent = RAGAgent(config)
agent.index_documents(config["ingestion"]["dataset-dir"])

async def process_message(user_message):
    llmBaseRes = agent.generate(user_message)
    llmRAGRes, RAGchunks = agent.generate_rag(user_message)
    llmKGRAGRes, KGRAGchunks = agent.generate_kgrag(user_message)

    response = {
        "base": llmBaseRes,
        "rag": {
            "response": llmRAGRes,
            "chunks": "\n\n".join([f"{x.metadata['source']} (page {x.metadata['page']}): {x.page_content}" for x in RAGchunks])
        },
        "kgrag": {
            "response": llmKGRAGRes,
            "chunks": "\n\n".join([f"{x.metadata['source']} (page {x.metadata['page']}): {x.page_content}" for x in KGRAGchunks])
        }
    }
    return response
