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

for (id of watchIds) {
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









const divider = document.querySelector('.divider');
const leftFlexbox = document.getElementById('search-div');
const rightFlexbox = document.getElementById('documents-div');

let isDragging = false;

divider.addEventListener('mousedown', (e) => {
  isDragging = true;
  document.body.style.cursor = 'ew-resize'; // Change cursor during drag
});

document.addEventListener('mousemove', (e) => {
  if (!isDragging) return;

  const containerRect = divider.parentElement.getBoundingClientRect();
  const newLeftWidth = e.clientX - containerRect.left;
  const newRightWidth = containerRect.width - newLeftWidth - divider.offsetWidth;

  // Update flexbox widths
  leftFlexbox.style.flex = `0 0 ${newLeftWidth}px`;
  rightFlexbox.style.flex = `0 0 ${newRightWidth}px`;
});

document.addEventListener('mouseup', () => {
  isDragging = false;
  document.body.style.cursor = ''; // Reset cursor
});