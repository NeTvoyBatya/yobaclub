window.onload = function(){
    connectToSocket()
    window.isConnectionLost = false
    document.getElementById("chatInputField").addEventListener("keydown", function(event){
        if( event.key == "Enter"){
            sendMessage()
        }
    })
    document.getElementById("loadScreenId").classList.add("done")
}

class ChatMessage {
    constructor(text, links, author, time){
        this.text = text
        this.links = links
        this.author = author
        this.time = time
    }
}

function connectToSocket(){
    window.chat_socket = new WebSocket("ws://127.0.0.1:8000/socket/cinema-chat");
    chat_socket.onmessage = (data) => socket_onmessage(data)
    chat_socket.onopen = () => {
        window.loadedMessages = []
        if (isConnectionLost){
            addChatMessage(new ChatMessage(`Соединение восстановлено: ${reconnectTime}`, [], "SYSTEM:", 500))
            isConnectionLost = false
        }
    }
    chat_socket.onclose  = (event) => {
        if (!isConnectionLost){
            addChatMessage(new ChatMessage("Соединение потеряно, мы попробуем всё исправить!", [], "SYSTEM:", 500))
            isConnectionLost = true
        }
        setTimeout(function(){
            reconnectTime = new Date().toTimeString()
            addChatMessage(new ChatMessage(`Попытка подключения: ${reconnectTime}`, [], "SYSTEM:", 500))
            connectToSocket()
        }, 5000)
    }

}

function sendMessage(){
    input_field = document.getElementById("chatInputField")
    chat_socket.send(JSON.stringify({"type": "msg", "text": input_field.value}));
    input_field.value = ""
}

function addChatMessage(message){
    let chat = document.getElementById("chatList")
    let message_element = document.createElement("li")
    let message_author = document.createElement("h4")
    let message_text = document.createElement("p")
    links = message.links
    text = message.text
    author = message.author
    time = message.time

    links.reverse()
    links.forEach(link => {
        url = text.slice(link[0], link[1])
        text = text.slice(0, link[0])+`<a class="link" href="${url}">${url}</a>`+text.slice(link[1], text.length)
    });

    message_author.innerHTML = author
    message_text.innerHTML = text
    message_element.className = "message"

    message_element.appendChild(message_author)
    message_element.appendChild(message_text)
    message_element.dataset.time = time

    chat.appendChild(message_element)
    window.loadedMessages.push(message.time)
}

function loadChatHistory(messages){
    window.loadedMessages = []
    messages.forEach(message => {
        message = new ChatMessage(message["text"], message["links"], message["author"], message["time"])
        if (!window.loadedMessages.includes(message.time)){
            addChatMessage(message)
        }
    });
}

function socket_onmessage(payload){
    let data = JSON.parse(payload.data)
    console.log(data)
    switch(data["type"]){
        case "msg":
            message = new ChatMessage(data["text"], data["links"], data["author"], data["time"])
            addChatMessage(message)
            break
        case "new_video":
            console.log(`New videos from ${data["author"]}`)
            console.log(data["videos"])
        case "history":
            loadChatHistory(data["messages"])
    }
}
