from .ingest import ingest_pdfs
from .retrieve import retrieve
from .generate import callLLM
import yaml
import os


__all__ = ["callLLM_base", "callLLM_with_RAG"]


with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "r") as f:
    config = yaml.safe_load(f)

vectorstore = ingest_pdfs(
    "datasets/MarineRestorationAnalysis/pdf", config["embedding-model"])


def callLLM_with_RAG(question):
    retrieved_docs = retrieve(vectorstore, question)
    if (len(retrieved_docs) == 0):
        return callLLM_base(question), retrieved_docs

    system_prompt = "Answer according to your knowledge and, if needed, the given facts. You are given the following data: " + \
        " ".join(list(map(lambda x: x.page_content, retrieved_docs)))
    system_prompt += "\nIf the data is irrelevant, ignore it and answer according to your knowledge.Do NOT mention that you were given any data or information in your response."

    response = callLLM(question, config, system_prompt)
    return response, retrieved_docs


def callLLM_base(question):
    return callLLM(question, config)
