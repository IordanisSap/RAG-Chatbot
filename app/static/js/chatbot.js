function sendMessage() {
    const message = document.getElementById('input-text').value;
    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: message})
    })
    .then(response => response.json())
    .then(data => {
        console.log("data:",data);
        const defaultLLM = document.getElementById('default-llm-output');
        const RAGLLM = document.getElementById('rag-llm-output');
        const enhancedLLM = document.getElementById('kgenhanced-llm-output');
        const retrieval = document.getElementById('kgenhanced-llm-retrieval');
        defaultLLM.innerHTML = `${data.response.base}`;
        RAGLLM.innerHTML = `${data.response.rag.response}`;
        enhancedLLM.innerHTML = `${data.response.kgrag.response}`;
        retrieval.innerHTML = `${data.response.kgrag.chunks}`;
    });
}