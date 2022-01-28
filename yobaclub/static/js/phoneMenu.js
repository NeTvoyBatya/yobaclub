var PhoneMenuId = document.getElementById('PhoneMenuId');
var PhoneNavId = document.getElementById('phone__navId')
var BGBlur = document.getElementById('mainContainer')
var Body = document.getElementById('body')
var PhoneMenuButton = document.getElementById('PhoneMenuButton')

function PhoneMenu (){
    PhoneMenuId.classList.toggle("on")
    PhoneNavId.classList.toggle("on")
    BGBlur.classList.toggle("blur")
    Body.classList.toggle("nonScroll")
    PhoneMenuButton.classList.toggle("on")
}
