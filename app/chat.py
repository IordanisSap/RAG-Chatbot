from .chatbot import callLLM_base,callLLM_with_RAG

async def process_message(user_message):
    llmBaseRes = callLLM_base(user_message)
    llmRAGRes = callLLM_with_RAG(user_message)
    response = {
        "base": llmBaseRes,
        "rag": llmRAGRes
    }
    return response