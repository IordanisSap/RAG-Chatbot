async function search() {
    message = document.getElementById("input-text-search").value
    topk = getTopk();
    score_threshold = getScoreThreshold();
    collection = document.getElementById("collections").value
    if (message.replace(/\s/g, "").length < 1) return
    const res = await fetch(`/SemanticRAG/search/${encodeURIComponent(message)}?` + new URLSearchParams({
        topk: topk,
        score_threshold: score_threshold,
        collection: collection
    }), {
        method: 'GET',
    })

    const parsedRes = await res.text()
    const keywords = message.toLowerCase().split(/\s+/)
    const modifiedRes = parsedRes
        .split(/\s+/)
        .map(word => isKeyword(word, keywords) ? '<strong>' + word + '</strong>' : word)
        .join(" ");
    document.getElementById("results").innerHTML = modifiedRes
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

    if (collection === 'new') {
        return;
    }

    const res = await fetch(`/SemanticRAG/collection/${collection}`, {
        method: 'GET',
    })

    const parsedRes = await res.text()

    // document.getElementById("documentsLabel").value =

    doc_container.innerHTML = parsedRes
}


getCollectionDocuments()



const modal = new bootstrap.Modal(document.getElementById('newCollectionModal'))
select_collection = document.getElementById('collections')
select_collection.setAttribute('data-previous-value', select_collection.value);


if (select_collection.value === "new") modal.show();

select_collection.onchange = (event) => {
    const previousValue = select_collection.getAttribute('data-previous-value');
    const currentValue = event.target.value;
    if (currentValue === "new") {
        openModal()
        select_collection.value = previousValue;
    } else {
        select_collection.setAttribute('data-previous-value', currentValue);
        getCollectionDocuments()
        search()
    }
}

function openModal() {
    modal.show();
    document.getElementById('newCollectionForm').reset()
}

search()


function showLoader() {
    document.getElementById('loader').classList.remove('d-none');
    document.getElementById('loader').classList.add('d-flex');
}


// function hideLoader() {
//     document.getElementById('loader').classList.remove('d-flex');
//     document.getElementById('loader').classList.add('d-none');
// }

document.getElementById('submitButton').addEventListener('click', function () {
    form = document.getElementById('newCollectionForm')
    if (form.checkValidity()) {
        showLoader()
        form.submit()
        modal.hide();
    }
    else form.reportValidity();
});


let switchFunc = switchToSearch;

function switchAction() {
    switchFunc()
    if (switchFunc === switchToSearch) switchFunc = switchToChat
    else switchFunc = switchToSearch
}
async function switchToSearch() {
    document.getElementById('search-div').style.display = 'flex'
    document.getElementById('chat-div').style.display = 'none'
    document.getElementById('switchLabel').innerHTML = "Switch to chatbot"
    document.getElementById('search-icon-switch').style.display = 'none'
    document.getElementById('chat-icon-switch').style.display = 'block'
}

async function switchToChat() {
    document.getElementById('chat-div').style.display = 'flex'
    document.getElementById('search-div').style.display = 'none'
    document.getElementById('switchLabel').innerHTML = "Switch to search"
    document.getElementById('chat-icon-switch').style.display = 'none'
    document.getElementById('search-icon-switch').style.display = 'block'

}


switchToChat()

const swiper = new Swiper(".mySwiper", {
    slidesPerView: 'auto',          // Number of slides to show at once
    spaceBetween: 20,          // Gap between slides in px
    loop: true,                // Whether to loop through slides
    pagination: {
        el: ".swiper-pagination",
        clickable: true
    },
    navigation: {
        nextEl: ".swiper-button-n",
        prevEl: ".swiper-button-p"
    },
    on: {
        // 'progress' fires for each movement; param 'progress' is in [0..1]
        progress(swiperInstance, progressValue) {
            const prevBtn = document.querySelector(".swiper-button-p");
            const nextBtn = document.querySelector(".swiper-button-n");

            // At the extreme left (progressValue = 0)
            if (progressValue === 0) {
                prevBtn.style.display = "none";
            } else {
                prevBtn.style.display = "block";
            }

            // At the extreme right (progressValue = 1)
            if (progressValue === 1) {
                nextBtn.style.display = "none";
            } else {
                nextBtn.style.display = "block";
            }
        }
    }
});


function onRecommendationClick(text) {
    document.getElementById("input-text").value = text.trim()
}