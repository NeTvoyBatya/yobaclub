window.onload = function(){
    fetch("api/get_things")
    .then(function(respone){
        return respone.json()
    })
    .then(loadThings)
}


function loadThings(json){
    let list = document.getElementById("galleryList")

    json.forEach(thing => {
        console.log(thing)
        thing_files = JSON.parse(thing["files"])
        main_image = ""
        thing_files.forEach(file =>{
            if (file["type"] == "image"){
                main_image = file["url"]
            }
        })

        p = document.createElement("p")
        h3 = document.createElement("h3")
        img = document.createElement("img")
        div = document.createElement("div")
        li = document.createElement("li")

        h3.innerHTML = thing["name"]
        p.innerHTML = thing["description"]

        if (main_image.length < 1){
            //Вставить сюда дефолтную картинку
        }else{
            img.setAttribute("src", main_image)
        }

        div.className = "gallery__item-text"
        li.className = "gallery__item"

        div.appendChild(h3)
        div.appendChild(p)

        li.appendChild(img)
        li.appendChild(div)

        list.append(li)
    });
    document.getElementById("loadScreenId").classList.add("done")
}

function showPostItemWindow(){
    document.getElementById("mainContainer").classList.add("blur")
    document.getElementById("postItemWindow").classList.remove("hidden")
}

[document.getElementById("closePostFormButton"), window].forEach(element => {
    element.onclick = function(event){
        switch(event.target.className){
            case "postitem_window":
            case "container":
            case "close_button":
                document.getElementById("postItemWindow").classList.add("hidden")
                document.getElementById("mainContainer").classList.remove("blur")
        }
    }
})
