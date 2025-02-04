async function search() {
    message = document.getElementById("input-text-search").value
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
const watchIds = ['input-text-search', 'topk', 'score']

function setWatch() {
    for (id of watchIds) {
        elem = document.getElementById(id)
        elem.addEventListener('input', () => {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(search, doneTypingInterval);
        });
    }
}

setWatch()


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

    doc_container.innerHTML = parsedRes
}


getCollectionDocuments()


const modal = new bootstrap.Modal(document.getElementById('newCollectionModal'))
select_collection = document.getElementById('collections')
select_collection.setAttribute('data-previous-value', select_collection.value);

select_collection.onchange = (event) => {
    const previousValue = select_collection.getAttribute('data-previous-value');
    const currentValue = event.target.value;
    if (currentValue === "new") {
        modal.show();
        document.getElementById('newCollectionForm').reset()
        select_collection.value = previousValue;
    } else {
        select_collection.setAttribute('data-previous-value', currentValue);
        switchToSearch()
        getCollectionDocuments()
        search()
    }
}

search()

document.getElementById('submitButton').addEventListener('click', function () {
    form = document.getElementById('newCollectionForm')
    if (form.checkValidity()) {
        form.submit()
        modal.hide();
    }
    else form.reportValidity();
});


let switchFunc = switchToSearch;

function switchAction(){
    switchFunc()
    if (switchFunc === switchToSearch) switchFunc = switchToChat
    else switchFunc = switchToSearch
}
async function switchToSearch() {
    document.getElementById('search-div').style.display='flex'
    document.getElementById('chat-div').style.display='none'
    document.getElementById('switchLabel').innerHTML = "Switch to chatbot"
    document.getElementById('search-icon-switch').style.display = 'none'
    document.getElementById('chat-icon-switch').style.display = 'block'
}

async function switchToChat() {
    document.getElementById('chat-div').style.display='flex'
    document.getElementById('search-div').style.display='none'
    document.getElementById('switchLabel').innerHTML = "Switch to search"
    document.getElementById('chat-icon-switch').style.display = 'none'
    document.getElementById('search-icon-switch').style.display = 'block'

}


switchToChat()