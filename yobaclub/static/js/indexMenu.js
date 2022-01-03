var closeMainMenu = document.getElementById("CloaseMainMenu")
var openMainMenu = document.getElementById("openMainMenu")
var CloseButton = document.getElementById("CloseButton")


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
    for (element of document.getElementsByClassName('openLink')) {
        if (element.className.endsWith(' on')){
            element.classList.toggle('on')
        }
    }
    closeMainMenu.classList.toggle("on")
    openMainMenu.classList.toggle("on")
    CloseButton.classList.toggle("on")
}