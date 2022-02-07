window.onload = function(){
    fetch("api/get_commits")
    .then(function(respone){
        return respone.json()
    })
    .then(loadCommits)
}

function simpleStrftime(timestamp) {
    var d = new Date(timestamp * 1000)
    hours = String(d.getHours())
    minutes = String(d.getMinutes())
    day = String(d.getDate())
    month = String(d.getMonth()+1)
    year = String(d.getFullYear())

    hours = hours.length < 2 ? "0"+hours : hours
    minutes = minutes.length < 2 ? "0"+minutes : minutes
    day = day.length < 2 ? "0"+day : day
    month = month.length < 2 ? "0"+month : month

    return `${hours}:${minutes} ${day}.${month}.${year}`
  }

function loadCommits(json){
    var list = document.getElementById("commits_list")
    var preloader = document.getElementById('loadScreenId');
    json.forEach(commit => {
        let avatar = document.createElement("img")
        avatar.className = "history-update__avatar"
        if (commit["author_img"] != null){
            avatar.setAttribute("src", commit["author_img"])
        }else{
            avatar.setAttribute("src", "static/media/noAvatar.png")
        }

        let author = document.createElement("span")
        author.className = "history-update__author"
        author.innerHTML = commit["author"]
        if (commit["author_link"] != null){
            author.classList.add("have_link")
            author.setAttribute("onclick", `window.open("${commit["author_link"]}", '_blank').focus()`)
        }

        let message = document.createElement("span")
        message.className = "history-update__message"
        message.innerHTML = commit["message"]

        let time = document.createElement("span")
        time.className = "history-update__time"
        time.innerHTML = simpleStrftime(commit["time"])

        let list_item = document.createElement("li")
        list_item.className = "history-update__element"
        list_item.setAttribute("type", "none")
        list_item.appendChild(avatar)
        list_item.appendChild(author)
        list_item.appendChild(message)
        list_item.appendChild(time)

        list.appendChild(list_item)
    });
    preloader.classList.add("done")
    document.getElementById('body').classList.add("done")
}
