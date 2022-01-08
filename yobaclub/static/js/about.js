window.onload = function(){
    fetch("api/get_commits")
    .then(function(respone){
        return respone.json()
    })
    .then(loadCommits)
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
        time.innerHTML = commit["time"]

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
