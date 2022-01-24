window.onload = function(){
    fetch("api/get_cinema_rooms")
    .then(function(respone){
        return respone.json()
    })
    .then(loadRooms)
}

function loadRooms(json){
    console.log(json)
    var preloader = document.getElementById('loadScreenId');
    var list = document.getElementById('roomsList')
    preloader.classList.add("done")
    json.forEach(room => {
        login_only = document.createElement('h1')
        users_count = document.createElement('h1')
        room_name = document.createElement('h1')
        div = document.createElement('div')
        ul = document.createElement('ul')

        div.className = "cinema_room"
        div.onclick = function(event){
            window.location.href = `cinema/${room["room_id"]}`
        }
        if (room["login_only"]){
            login_only.innerHTML = "Только для членов йоба-клуба"
        }else{
            login_only.innerHTML = "Открытый вход"
        }
    
        users_count.innerHTML = room["users_in"].length
        room_name.innerHTML = room["room_name"]

        div.appendChild(room_name)
        div.appendChild(users_count)
        div.appendChild(login_only)
    
        ul.appendChild(div)
        list.appendChild(ul)

    });
}