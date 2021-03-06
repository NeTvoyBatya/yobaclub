window.onload = function(){
    getVideos()
    window.autoplay_on = false
    window.addEventListener("keydown", function(event) {
        if (event.key == 'ArrowRight'){
            let button = this.document.getElementById("buttonNext")
            button.classList.add('pseudo_active')
            button.click()
        }else if(event.key == 'ArrowLeft'){
            let button =  this.document.getElementById("buttonPrevious")
            button.classList.add('pseudo_active')
            button.click()
        }
    }, true);
    window.addEventListener("keyup", function(event) {
        if (event.key == 'ArrowRight'){
            let button = this.document.getElementById("buttonNext")
            button.classList.remove('pseudo_active')
        }else if(event.key == 'ArrowLeft'){
            let button =  this.document.getElementById("buttonPrevious")
            button.classList.remove('pseudo_active')
        }
    }, true);
}

function getVideos(){
    fetch("api/get_videos")
    .then(function(response){
        if (response.status != 200){
            setTimeout(getVideos, 2000)
        }else{
            response.json().then(loadVideos)
        }})
}

function updateTitles(){
    let number = document.getElementById("video_number")
    let title = document.getElementById("video_title")
    let title_text = window.videos[window.current_video_index]["name"]
    number.innerHTML = `${window.current_video_index+1}/${window.videos.length}`
    if (title_text.length > 25){
        title.innerHTML =   title_text.slice(0, 25)+"..."
        title.setAttribute('data-tooltip', window.videos[window.current_video_index]["name"])
    }else{
        title.removeAttribute('data-tooltip')
        title.innerHTML =  title_text
    }

}

function updatePlayer(){
    let video_link = window.videos[window.current_video_index]["link"]
    let player = document.getElementById("video_player")
    player.setAttribute("src", video_link)
}

function updateVideo(){
    updateTitles()
    updatePlayer()
}

function loadVideos(json){
    console.log(json)
    var preloader = document.getElementById("loadScreenId")
    let player = document.getElementById("video_player")
    window.videos = json["videos"]
    window.threads = json["threads"]
    window.current_video_index = 0
    player.volume = 0.15
    updateVideo()
    player.pause()
    preloader.classList.add("done")
    player.play()
}

function nextVideo(){
    if (window.current_video_index+1 < window.videos.length){
        window.current_video_index+=1
        updateVideo()
    }
}

function previousVideo(){
    if (window.current_video_index-1 >= 0){
        window.current_video_index-=1
        updateVideo()
    }
}

function loop(){
    loopButton = document.getElementById("loopButton")
    autoplayButton = document.getElementById("autoplayButton")
    player = document.getElementById("video_player")
    player.removeEventListener("ended", nextVideo, false)
    player.toggleAttribute("loop")
    window.autoplay_on = false
    autoplayButton.classList.remove("active")
    loopButton.classList.toggle("active")
}

function autoplay(){
    loopButton = document.getElementById("loopButton")
    autoplayButton = document.getElementById("autoplayButton")
    player = document.getElementById("video_player")
    if (window.autoplay_on == true){
        player.removeEventListener("ended", nextVideo, false)
        window.autoplay_on = false
        autoplayButton.classList.remove("active")
    }else{
        player.removeAttribute("loop")
        player.addEventListener("ended", nextVideo, false)
        window.autoplay_on = true
        loopButton.classList.remove("active")
        autoplayButton.classList.add("active")
    }
}

function inThread(){
    video = window.videos[window.current_video_index]
    let thread_link = `${video["link"].replace("src", "res").split("/").slice(0, -1).join("/")}.html#${video["post_num"]}`
    window.open(thread_link, "_blank").focus()
}

function yobaAlert(text, showTime){
    let notificationForm = document.getElementById("notificationForm")
    notificationForm.firstElementChild.innerHTML = text
    notificationForm.classList.remove("hidden")
    return new Promise(resolve => {
        setTimeout(() => {notificationForm.classList.add("hidden"); resolve(true)}, showTime)
    })
}

function yobaPrompt(timeout){
    let promptForm = document.getElementById("promptForm")
    promptForm.classList.remove("hidden")
    return new Promise(resolve => {
        setTimeout(() => {promptForm.classList.add("hidden"); resolve(false)}, timeout)
    })
}

function postVideo(){
    post_src = document.getElementById("video_player").src
    post_title = document.getElementById("promptInput").value
    document.getElementById("promptForm").classList.add("hidden")
    document.getElementById("promptInput").value = ""
    fetch("api/post_video",{
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"src": post_src, "title": post_title})
    })
    .then(function(response){
        return response.json()
    })
    .then(function(json){
        yobaAlert(json["text"], 5000)
    })
}

function getTrack(button){
    player = document.getElementById("video_player")
    button.classList.add("active")
    fetch("api/get_track", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"url": document.getElementById("video_player").src, "time": player.currentTime, "duration": player.duration})
    })
    .then(function(response){
        return response.json()
    })
    .then(function(json){
        yobaAlert(json["text"], 5000)
        button.classList.remove("active")
    })

}

function removeVideosOfThread(){
    let to_delete = []
    thread_num = window.videos[window.current_video_index]["thread_num"]
    for (let i = window.videos.length-1; i >= 0; i--) {
        if (window.videos[i]["thread_num"] == thread_num){
            to_delete.push(i)
        }
    }
    while (to_delete.includes(window.current_video_index)) {
        window.current_video_index++
    }
    let offset = 0
    for (const index of to_delete) {
        window.videos.splice(index, 1)
        if (index < window.current_video_index){
            offset++
        }
    }
    window.current_video_index-=offset
    if (window.current_video_index >= window.videos.length) window.current_video_index = window.videos.length-1
    updateVideo()
    document.getElementById("deleteThreadWindow").classList.add("hidden")
    document.getElementById("mainContainer").classList.remove("blur")
}

function showDeleteThreadWindow(){
    deleted_thread_num = window.videos[window.current_video_index]["thread_num"]
    deleted_count = 0
    for (const video of window.videos) {
        if (video["thread_num"] == deleted_thread_num){
            deleted_count++
        }
    }
    window_title = window.threads[deleted_thread_num]['subject']
    window_text = `?????????? ????????????????, ?? ???????????? ?????????????????? ${window.videos.length-deleted_count} ??????????`
    button_text = `?????????????? ${deleted_count} ??????????`
    document.getElementById("deleteThreadTitle").innerHTML = window_title
    document.getElementById("deleteThreadText").innerHTML = window_text
    document.getElementById("deleteButton").innerHTML = button_text
    document.getElementById("video_player").pause()
    document.getElementById("mainContainer").classList.add("blur")
    document.getElementById("deleteThreadWindow").classList.remove("hidden")
}

[document.getElementById("closeDeleteWindowButton"), window].forEach(element => {
    element.onclick = function(event){
        switch(event.target.className){
            case "delete_thread_window":
            case "container":
            case "close_button":
            case "close_button_img":
                document.getElementById("deleteThreadWindow").classList.add("hidden")
                document.getElementById("mainContainer").classList.remove("blur")
        }
    }
})