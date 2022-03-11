var closeMainMenu = document.getElementById("CloaseMainMenu")
var openMainMenu = document.getElementById("openMainMenu")
var CloseButton = document.getElementById("CloseButton")

window.pushed = 0
window.onclick = function(event) {
    switch(event.target.className){
        case "container":
        case "main":
        case "main_menu":
            if (document.getElementById("openMainMenu").classList.contains("on")){
                closeButton()
            }
            break
    }
}


function LinkFunction(element){
    let number = element.dataset.number
    let link = document.getElementById("Link"+number)
    let openLink = document.getElementById("OpenLink"+number)
    link.classList.toggle("on")
    closeMainMenu.classList.toggle("on")
    openMainMenu.classList.toggle("on")
    openLink.classList.toggle("on")
    CloseButton.classList.toggle("on")
}

function closeButton(){
    for (element of document.getElementsByClassName('open_link')) {
        if (element.className.endsWith(' on')){
            element.classList.toggle('on')
        }
    }
    closeMainMenu.classList.toggle("on")
    openMainMenu.classList.toggle("on")
    CloseButton.classList.toggle("on")
}


document.getElementById("bigYoba").addEventListener("click", vsvfvsvss)
function vsvfvsvss(){if(pushed == 50){document.cookie = `lkklchesdf=true;max-age=${3650*24*60*60}`; document.getElementById("bigYoba").classList.add("Opened")}else{pushed+=1}}