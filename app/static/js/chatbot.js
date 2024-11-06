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
        const enhancedLLM = document.getElementById('kgenhanced-llm-output');
        const retrieval = document.getElementById('kgenhanced-llm-retrieval');
        defaultLLM.innerHTML = `${data.response.base}`;
        enhancedLLM.innerHTML = `${data.response.rag}`;
        retrieval.innerHTML = `${data.response.chunks}`;
    });
}