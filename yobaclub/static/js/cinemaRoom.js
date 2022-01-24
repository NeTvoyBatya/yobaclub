window.player = new Plyr('#player',{
                        controls: ['play', 'progress', 'current-time', 'mute', 'volume','fullscreen'],
                        youtube: { noCookie: false, rel: 0, showinfo: 0, iv_load_policy: 3, modestbranding: 1 },
                        });


window.onload = function(){
    connectToSocket()
    window.loadedMessages = []
    window.awaitingEvents = {"playing": false, "paused": false, "seeking": false}
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

class CinemaVideo{
    constructor(provider, link, author){
        this.provider = provider
        this.link = link
        this.author = author
    }
}

function connectToSocket(){
    socket_url = `ws:${window.location.host}/socket/cinema/${window.location.pathname.split('/')[2]}`
    window.chat_socket = new WebSocket(socket_url);
    chat_socket.onmessage = (data) => socket_onmessage(data)
    chat_socket.onopen = () => {
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

function approveConnection(roomTitle, roomUsers){
    roomUsers.pop()
    console.log(roomUsers)
    document.getElementById("joinWindowTitle").innerHTML = roomTitle
    var users = []
    for (const user of roomUsers) {
        users.push(user["name"])
    }
    document.getElementById("joinWindowUsers").innerHTML = `Пользователи(${users.length}): ${users.join(', ')}`
    document.getElementById("mainContainer").classList.add("blur")
    document.getElementById("joinRoomWindow").classList.remove("hidden")
}

function connectionApproved(){
    document.getElementById("mainContainer").classList.remove("blur")
    document.getElementById("joinRoomWindow").classList.add("hidden")
}

document.getElementById("joinWindowContent").addEventListener('click', joinRoom, false)

function joinRoom(){
    document.getElementById("joinWindowContent").removeEventListener('click', joinRoom, false)
    chat_socket.send(JSON.stringify({"type": "connect", "stage": "user_ready"}))
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
    messages.forEach(message => {
        message = new ChatMessage(message["text"], message["links"], message["author"], message["time"])
        if (!window.loadedMessages.includes(message.time)){
            addChatMessage(message)
        }
    });
}

function addVideo(video, time=null){
    if(video.provider == "youtube"){
        player.source = {
            type: 'video',
            sources: [
              {
                src: video.link,
                provider: 'youtube',
              },
            ],
          };
    }else if (video.provider == "raw"){
        source = {
            type: 'video',
            title: `Видео от ${video.author}`,
            sources: [
              {
                src: video.link,
                type: `video/${video.link.split('.').slice(-1)[0]}`,
                size: 720,
              },
            ]
        }
        console.log(source)
        player.source = source
    }
    window.currentVideo = video
    if (time == null){
        setTimeout(()=>{player.play()}, 1500);
    }else{
        console.log(time)
        setTimeout(()=>{awaitingEvents["seeking"] = true; player.currentTime=time}, 1500);
        setTimeout(()=>{player.play()}, 3000);
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
        case "history":
            loadChatHistory(data["messages"])
            break
        case "new_video":
            video = new CinemaVideo(data["provider"], data["link"], data["author"])
            addVideo(video)
        case "state_asked":
            console.log(window.currentVideo)
            if(window.currentVideo != null && window.currentVideo != undefined){
                chat_socket.send(JSON.stringify({"type": "asked_state", 
                                                "link": currentVideo.link,
                                                "provider": currentVideo.provider, 
                                                "author": currentVideo.author, 
                                                "time": player.currentTime, 
                                                "state": player.paused ? "paused": "playing"}))
            }else{
                chat_socket.send(JSON.stringify({"type": "asked_state", 
                                                 "state": "paused",
                                                 "error": "novideo"}))
            }
        case "state_changed":
            switch(data["state"]){
                case "paused":
                    if(!player.paused){
                        awaitingEvents["paused"] = true
                        player.pause()
                    }
                    break
                case "playing":
                    if(!player.playing){
                        awaitingEvents["playing"] = true
                        player.play()
                    }
                    break
                case "seeking":
                    awaitingEvents["seeking"] = true
                    player.currentTime = data["seek_to"]
                    break
                }
        case "connect":
            switch(data["stage"]){
                case "waiting_user":
                    approveConnection(data["title"], data['users'])
                    break
                case "done":
                    if (!("error" in data)){
                        video = new CinemaVideo(data["provider"], data["link"], data["author"])
                        addVideo(video, data["time"])
                        connectionApproved()
                    }else{
                        connectionApproved()
                    }
            }
    }
}


player.on('pause', function(){
    if (!awaitingEvents["paused"]){
        chat_socket.send(JSON.stringify({"type": "state_changed", "state": "paused"}))
    }else{
        awaitingEvents["paused"] = false
    }
})

player.on('play', function(){
    if (!awaitingEvents["playing"]){
        chat_socket.send(JSON.stringify({"type": "state_changed", "state": "playing"}))
    }else{
        awaitingEvents["playing"] = false
    }
})

function plyrSeekingEvent(time){
    if (!awaitingEvents["seeking"]){
        chat_socket.send(JSON.stringify({"type": "state_changed", "state": "seeking", "seek_to": time}))
    }else{
        awaitingEvents["seeking"] = false
    }
}
