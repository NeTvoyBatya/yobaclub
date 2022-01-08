window.player = new Plyr('#player',{
                        autoplay: true, 
                        controls: ['play', 'progress', 'current-time', 'mute', 'volume','fullscreen'],
                        youtube: { noCookie: false, rel: 0, showinfo: 0, iv_load_policy: 3, modestbranding: 1 },
                        });


window.onload = function(){
    connectToSocket()
    window.isConnectionLost = false
    window.syncGotEventList = {"pause": false, "play": true, "seek": false}
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

function addVideo(video_payload){
    switch(video_payload["provider"]){
        case "youtube":
            player.source = {type: "video", sources: [{src:video_payload["videos"][0], provider: "youtube"}]}
            break
        case "raw":
            if (video_payload["videos"][0].includes(".mp4")){
                ext = "mp4"
            }else{
                ext = "webm"
            }
            player.source = {type: "video", title: video_payload["videos"][0], sources: [{src:video_payload["videos"][0], type: `video/${ext}`}]}
    }
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
            addVideo(data)
            break
        case "history":
            loadChatHistory(data["messages"])
            break
        case "video_state_changed":
            state = data["state_content"]
            switch(state["state_type"]){
                case "paused":
                    syncGotEventList["pause"] = true
                    player.pause()
                    break
                case "playing":
                    syncGotEventList["play"] = true
                    player.play()
                    break
                case "seeking":
                    syncGotEventList["seek"] = true
                    player.currentTime = state["seek_to"]
            }
            break
    }
}

player.on('pause', (event) => {
    if(!syncGotEventList["pause"]){
        chat_socket.send(JSON.stringify({"type": "video_state_changed", "state": "paused"}))
        return
    }
    syncGotEventList["pause"] = false
})

player.on('play', (event) => {
    if(!syncGotEventList["play"]){
        chat_socket.send(JSON.stringify({"type": "video_state_changed", "state": "playing"}))
        return
    }
    syncGotEventList["play"] = false 
})

function plyrSeekingEvent(seekingTime){
    if(!syncGotEventList["seek"]){
        chat_socket.send(JSON.stringify({"type": "video_state_changed", "state": "seeking", "seek_to": seekingTime}))
        return
    }
    syncGotEventList["seek"] = false
}

