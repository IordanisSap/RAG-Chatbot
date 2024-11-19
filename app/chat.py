from .chatbot import callLLM_base, callLLM_with_RAG


async def process_message(user_message):
    llmBaseRes = callLLM_base(user_message)
    llmRAGRes, RAGchunks = callLLM_with_RAG(user_message)
    llmKGRAGRes, KGRAGchunks = callLLM_with_RAG(user_message)
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
