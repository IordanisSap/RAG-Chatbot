async function sendMessage(message) {
    const res = await fetch('/SemanticRAG/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })

    const parsedRes = await res.json()
    return parsedRes
}


document.querySelectorAll("textarea").forEach(function (textarea) {
    const lineHeight = parseFloat(getComputedStyle(textarea).lineHeight);
    console.log(lineHeight)

    const maxLines = textarea.id === "input-text" ? 8 : 50;
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
});


function getUserMessage() {
    return document.getElementById("input-text").value
}

function clearUserMessage() {
    document.getElementById("input-text").value = ""
}

function showUserMessage(text) {
    document.getElementById("user-message").style.display = "flex"
    document.getElementById("user-message-text").value = text
}

function hideChatbotResponses() {
    document.querySelector("#chatbot-message").style.display = "none"
}

function showChatbotLoading(show) {
    document.querySelector("#chatbot-message-placeholder").style.display = show ? "flex" : "none"
    document.querySelector("#chat-message-text-placeholder").value = ""
    hideChatbotResponses()
}

function setChatbotResponses(res1, res2) {
    document.querySelector("#chatbot-message").style.display = "flex"
    document.getElementById("chatbot-message-text1").value = res1
    document.getElementById("chatbot-message-text2").value = res2
}

function setRelevantText(text) {
    if (text) {
        document.getElementById("retreived-text-container").style.display = "block"
        document.getElementById("retreived-text").innerHTML = text
    } else {
        document.getElementById("retreived-text-container").style.display = "none"
    }
}

function setStickyBottom(){
    document.getElementById("sticky-footer").style.bottom = '35px';
    document.getElementById("sticky-footer").style.translate = 'translate(-50%, 0%)';
}

function disableSendButton(state) {
    document.getElementById("send-button").disabled = state
}


function onMessageSend() {
    userMsg = getUserMessage()
    showUserMessage(userMsg)
    showChatbotLoading(true)
    setRelevantText("")
    clearUserMessage()
    disableSendButton(true)
    setStickyBottom()

    sendMessage(userMsg).then(res => {
        baseRes = res.response.base

        ragRes = res.response.rag.response
        ragChunks = res.response.rag.chunks

        showChatbotLoading(false)
        setChatbotResponses(baseRes, ragRes)
        setRelevantText(ragChunks)
        disableSendButton(false)
    })
}

function setResponseSelection(id) {
    res = document.getElementById(id).value;
    hideChatbotResponses()

    document.querySelector("#chatbot-message-placeholder").style.display = "flex"
    document.querySelector("#chat-message-text-placeholder").value = res;
}