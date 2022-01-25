window.onload = function(){
    fetch("api/get_videos")
    .then(function(respone){
        return respone.json()
    })
    .then(loadVideos)

    window.autoplay_on = false
    window.addEventListener("keydown", function(event) {
        if (event.key == 'ArrowRight'){
          nextVideo()
        }else if(event.key == 'ArrowLeft'){
          previousVideo()
        }
        }, true);
}

function updateTitles(){
    let number = document.getElementById("video_number")
    let title = document.getElementById("video_title")
    number.innerHTML = `${window.current_video_index+1}/${window.videos.length}`
    title.innerHTML = window.videos[window.current_video_index]["name"]
    title.setAttribute('data-tooltip', window.videos[window.current_video_index]["name"])
    
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
    var preloader = document.getElementById("loadScreenId")
    let player = document.getElementById("video_player")
    window.videos = json["videos"]
    window.threads = json["threads"]
    window.current_video_index = 0
    player.volume = 0.15
    updateVideo()
    player.pause()
    console.log(json)
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