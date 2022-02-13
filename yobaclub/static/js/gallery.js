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
        author = document.createElement("h3")
        img = document.createElement("img")
        item_div = document.createElement("div")
        title_div = document.createElement("div")
        li = document.createElement("li")

        h3.innerHTML = thing["name"]
        p.innerHTML = thing["description"]
        author.innerHTML = thing["author"]
        
        if (thing_files.length > 1){
            files_length = String(thing_files.length)
            if(files_length.endsWith('1') && files_length[files_length.length-2] !='1'){
                h3.innerHTML += ` (${files_length} файл)`
            }else if((files_length.endsWith('2') || files_length.endsWith('3') || files_length.endsWith('4')) && files_length[files_length.length-2] !='1'){
                h3.innerHTML += ` (${files_length} файла)`
            }else{
                h3.innerHTML += ` (${files_length} файлов)`
            }
        }

        
        if (main_image.length < 1){
            img.setAttribute("src", "static/media/image_placeholder.jpg")
        }else{
            img.setAttribute("src", main_image)
        }

        item_div.className = "gallery__item-div"
        title_div.className = "gallery__item-title"
        li.className = "gallery__item"

        title_div.appendChild(h3)
        title_div.appendChild(author)

        item_div.appendChild(title_div)
        item_div.appendChild(p)

        li.appendChild(img)
        li.appendChild(item_div)

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
            case "close_button_img":
                document.getElementById("postItemWindow").classList.add("hidden")
                document.getElementById("mainContainer").classList.remove("blur")
        }
    }
})
