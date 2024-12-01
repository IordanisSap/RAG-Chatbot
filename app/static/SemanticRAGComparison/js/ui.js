document.querySelectorAll("textarea").forEach(function(textarea) {
    const lineHeight = parseFloat(getComputedStyle(textarea).lineHeight); // Get the line height of the textarea
    const maxLines = 6;
    const maxHeight = lineHeight * maxLines;

    textarea.style.height = textarea.lineHeight + "px";
    console.log(textarea.style.height)
    textarea.style.overflowY = "hidden";

    textarea.addEventListener("input", function() {
        this.style.height = "auto"; // Reset the height to auto
        if (this.scrollHeight > maxHeight) {
            this.style.height = maxHeight + "px"; // Set height to maxHeight
            this.style.overflowY = "scroll"; // Enable scrolling
        } else {
            this.style.height = this.scrollHeight + "px"; // Adjust to content
            this.style.overflowY = "hidden"; // Hide scrollbar
        }
    });
});


function getUserMessage(){
    return document.getElementById("input-text").value
}

function showUserMessage(text) {
    document.getElementById("user-message").style.display = "flex"
    document.getElementById("user-message-text").value = text
} 

function showChatbotMessage(text) {
    document.querySelector("#chatbot-message").style.display = "flex"
} 


function onMessageSend() {
    showUserMessage(getUserMessage())
    showChatbotMessage("")
}