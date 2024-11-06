from .chatbot import callLLM_base, callLLM_with_RAG


async def process_message(user_message):
    llmBaseRes = callLLM_base(user_message)
    llmRAGRes, chunks = callLLM_with_RAG(user_message)
    response = {
        "base": llmBaseRes,
        "rag": llmRAGRes,
        "chunks": "\n\n".join([f"{x.metadata['source']} (page {x.metadata['page']}): {x.page_content}" for x in chunks])
    }
    return response
