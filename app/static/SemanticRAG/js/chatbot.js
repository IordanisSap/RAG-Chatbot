let messages = []

function addUserMessage(text) {
    messages = []
    messages.push({
        "role": "user",
        "content": text
    })
}

function addBotMessage(responses) {
    messages.push({
        "role": "ai",
        "responses": responses
    })
}

async function getConversation(messages) {
    const res = await fetch('/SemanticRAG/conversation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: messages })
    })
    const parsedRes = await res.text()
    return parsedRes
}

async function getRelevantWork(passages, userMsg) {
    const res = await fetch('/SemanticRAG/passages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ collection: collection, passages: passages, query: userMsg })
    })
    const parsedRes = await res.text()
    return parsedRes
}

async function sendMessage(message, topk, score_threshold) {
    const res = await fetch('/SemanticRAG/chat?' + new URLSearchParams({
        topk: topk,
        score_threshold: score_threshold
    }), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ collection: collection, message: message })
    })

    const parsedRes = await res.json()
    return parsedRes
}


document.getElementById("input-text").addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        if (!event.shiftKey) {
            event.preventDefault();
            document.getElementById("send-button").click()
        }
    }
})

function getTopkChat() {
    elem = document.getElementById("topk-chat");
    return elem.value !== "" ? elem.value : elem.getAttribute("placeholder");
}

function getScoreThresholdChat() {
    elem = document.getElementById("score-chat");
    return elem.value !== "" ? elem.value : elem.getAttribute("placeholder");
}


function clearUserMessage() {
    document.getElementById("input-text").value = ""
}

function setRelevantText(text) {
    if (text) {
        document.getElementById("retrieved-text-container").style.display = "block"
        document.getElementById("retrieved-text").innerHTML = text
    } else document.getElementById("retrieved-text-container").style.display = "none"
}

function setStickyBottom() {
    document.getElementById("sticky-footer").style.bottom = '35px';
    document.getElementById("sticky-footer").style.translate = 'translate(-50%, 0%)';
}

function disableSendButton(state) {
    document.getElementById("send-button").disabled = state
}


async function onMessageSend() {
    userMsg = document.getElementById("input-text").value
    addUserMessage(userMsg)
    setRelevantText("")
    document.getElementById("input-text").value = ""
    disableSendButton(true)
    setStickyBottom()

    getConversation(messages).then(res => {
        document.getElementById("conversation").innerHTML = res
    })

    topk = getTopkChat()
    score_threshold = getScoreThresholdChat()

    sendMessage(userMsg, topk, score_threshold).then(res => {
        console.log(res)
        addBotMessage(res)

        rag_passages = res[1].chunks


        getConversation(messages).then(res => {
            document.getElementById("conversation").innerHTML = res
            disableSendButton(false)
        })

        if (rag_passages)
            getRelevantWork(rag_passages, userMsg).then(res => {
                const parsedRes = res
                const keywords = userMsg.toLowerCase().split(/\s+/)
                const modifiedRes = parsedRes
                    .split(/\s+/)
                    .map(word => isKeyword(word, keywords) ? '<strong>' + word + '</strong>' : word)
                    .join(" ");
                setRelevantText(modifiedRes)
            })
    })
}



input_textarea = document.getElementById("input-text")
function adjustTextarea(textarea) {
    const lineHeight = parseFloat(getComputedStyle(textarea).lineHeight);
    const maxLines = 8;
    const maxHeight = lineHeight * maxLines;

    textarea.style.height = textarea.lineHeight + "px";
    textarea.style.overflowY = "hidden";

    function adjustHeight() {
        textarea.style.height = 0;
        if (textarea.scrollHeight > maxHeight) {
            textarea.style.height = maxHeight + "px";
            textarea.style.overflowY = "scroll";
        } else {
            textarea.style.height = textarea.scrollHeight + "px";
            textarea.style.overflowY = "hidden";
        }
    }

    adjustHeight()

    const originalDescriptor = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(textarea), 'value');

    Object.defineProperty(textarea, 'value', {
        get: function () {
            return originalDescriptor.get.call(this);
        },
        set: function (val) {
            originalDescriptor.set.call(this, val);
            setTimeout(() => adjustHeight.call(this), 0);
        }
    });
    textarea.addEventListener("input", adjustHeight);
}
adjustTextarea(input_textarea)