async function search() {
    message = document.getElementById("input-text").value
    topk = getTopk();
    score_threshold = getScoreThreshold();
    if (message.replace(/\s/g, "").length < 1) return
    const res = await fetch(`/SemanticRAG/search/${message}?` + new URLSearchParams({
        topk: topk,
        score_threshold: score_threshold
    }), {
        method: 'GET',
    })

    const parsedRes = await res.text()
    document.getElementById("results").innerHTML = parsedRes
}

let typingTimer;
const doneTypingInterval = 500;
const watchIds = ['input-text', 'topk', 'score']

const textarea = document.getElementById('input-text');

for (id of watchIds){
    elem = document.getElementById(id)
    elem.addEventListener('input', () => {
        clearTimeout(typingTimer); 
        typingTimer = setTimeout(search, doneTypingInterval);
    });
}

function getTopk() {
    elem = document.getElementById("topk");
    return elem.value !== "" ? elem.value : elem.getAttribute("placeholder");
}

function getScoreThreshold() {
    elem = document.getElementById("score");
    return elem.value !== "" ? elem.value : elem.getAttribute("placeholder");
}
