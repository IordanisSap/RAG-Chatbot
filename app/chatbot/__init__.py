from KG_RAG import generate, generate_rag, generate_kgrag

__all__ = ["callLLM_base", "callLLM_with_RAG", "callLLM_with_KGRAG"]

def callLLM_with_KGRAG(question):
    return generate_kgrag(question)


def callLLM_with_RAG(question):
    return generate_rag(question)


def callLLM_base(question):
    return generate(question)
