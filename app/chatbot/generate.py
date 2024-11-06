from langchain_ollama import OllamaLLM
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


def callLLM(prompt, config, system_prompt=""):
    llm = OllamaLLM(model=config["model"])

    llm.temperature = config["temperature"]
    system_prompt = config["prompts"]["system"] + "." + system_prompt

    messages = [
        system_prompt,
        HumanMessage(prompt)
    ]

    response = llm.invoke(messages)
    return response
