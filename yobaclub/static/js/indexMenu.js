var closeMainMenu = document.getElementById("CloaseMainMenu")


function LinkFunction(element){
    let number = element.dataset.number
    let link = document.getElementById("Link"+number)
    let openLink = document.getElementById("OpenLink"+number)
    link.classList.toggle("on")
    closeMainMenu.classList.toggle("on")
    openLink.classList.toggle("on")
}
