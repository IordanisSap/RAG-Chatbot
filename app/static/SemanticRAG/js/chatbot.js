

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

async function sendMessage(message) {
    const res = await fetch('/SemanticRAG/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
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


function getUserMessage() {
    return document.getElementById("input-text").value
}

function clearUserMessage() {
    document.getElementById("input-text").value = ""
}

function setRelevantText(text) {
    if (text) {
        document.getElementById("retreived-text-container").style.display = "block"
        document.getElementById("retreived-text").innerHTML = text
    } else {
        document.getElementById("retreived-text-container").style.display = "none"
    }
}

function setStickyBottom() {
    document.getElementById("sticky-footer").style.bottom = '35px';
    document.getElementById("sticky-footer").style.translate = 'translate(-50%, 0%)';
}

function disableSendButton(state) {
    document.getElementById("send-button").disabled = state
}


async function onMessageSend() {
    userMsg = getUserMessage()
    addUserMessage(userMsg)
    setRelevantText("")
    clearUserMessage()
    disableSendButton(true)
    setStickyBottom()

    getConversation(messages).then(res => {
        document.getElementById("conversation").innerHTML = res
    })

    sendMessage(userMsg).then(res => {
        llm_name = res.name
        baseRes = res.response.base

        ragRes = res.response.rag.response
        ragChunks = res.response.rag.chunks

        addBotMessage(
            [
                {
                    "name": llm_name,
                    "content": baseRes
                },
                {
                    "name": llm_name + " + RAG",
                    "content": ragRes
                }
            ]
        )

        console.log(res)

        getConversation(messages).then(res => {
            document.getElementById("conversation").innerHTML = res
            console.log(ragChunks)
            setRelevantText(ragChunks)
            disableSendButton(false)
        })
    })
}