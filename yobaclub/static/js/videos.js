window.onload = function(){
    fetch("api/get_videos")
    .then(function(respone){
        return respone.json()
    })
    .then(loadVideos)

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
}

function updatePlayer(){
    let video_link = window.videos[window.current_video_index]["link"]
    let thread_link = `${video_link.replace("src", "res").split("/").slice(0, -1).join("/")}.html#${window.videos[window.current_video_index]["post_num"]}`
    let player = document.getElementById("video_player")
    let thread_button = document.getElementById("thread_button")
    player.setAttribute("src", video_link)
    thread_button.setAttribute("href", thread_link)
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