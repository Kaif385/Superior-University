function sendMessage() {
    const inputField = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const typingIndicator = document.getElementById("typing-indicator");
    const message = inputField.value.trim();

    if (message === "") return;


    addMessage(message, "user-message");
    inputField.value = "";


    typingIndicator.style.display = "block";
    chatBox.scrollTop = chatBox.scrollHeight;


    fetch('/get_response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'msg=' + encodeURIComponent(message)
    })
    .then(response => response.json())
    .then(data => {
        setTimeout(() => {
            typingIndicator.style.display = "none";
            addMessage(data.response, "bot-message");
        }, 700);
    })
    .catch(error => {
        typingIndicator.style.display = "none";
        addMessage("Connection error. Please try again.", "bot-message");
    });
}

function addMessage(text, className) {
    const chatBox = document.getElementById("chat-box");
    const typingIndicator = document.getElementById("typing-indicator");
    
    const div = document.createElement("div");
    div.classList.add("message", className);
    div.innerText = text;
    
    chatBox.insertBefore(div, typingIndicator);
    chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") sendMessage();
});