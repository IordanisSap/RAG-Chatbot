async function search() {
    message = document.getElementById("input-text").value
    topk = getTopk();
    score_threshold = getScoreThreshold();
    collection = document.getElementById("collections").value
    if (message.replace(/\s/g, "").length < 1) return
    const res = await fetch(`/SemanticRAG/search/${message}?` + new URLSearchParams({
        topk: topk,
        score_threshold: score_threshold,
        collection: collection
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


const doc_container = document.getElementById("documents-container")

async function getCollectionDocuments() {
    const collection = document.getElementById("collections").value

    const res = await fetch(`/SemanticRAG/collection/${collection}`, {
        method: 'GET',
    })

    const parsedRes = await res.text()

    console.log(parsedRes);
    doc_container.innerHTML = parsedRes
}


getCollectionDocuments()
