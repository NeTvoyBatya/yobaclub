var ButtonThemMenu = document.getElementById('ThemeMenuId');
var ButtonThemMenuIcon = document.getElementById('ThemeMenuIcon');
var tenYearsAhead = 3650*24*60*60
var body = document.getElementById('body')
var checkMarks = {
    "samurai": document.getElementById('SamuraiCheckMark'),
    "forest": document.getElementById('ForestCheckMark'),
    "factory": document.getElementById('FactoryCheckMark'),
    "white_area": document.getElementById('WhiteAreaCheckMark'),
}
var phoneCheckMarks = {
    "samurai": document.getElementById('SamuraiCheckMarkPhone'),
    "forest": document.getElementById('ForestCheckMarkPhone'),
    "factory": document.getElementById('FactoryCheckMarkPhone'),
    "white_area": document.getElementById('WhiteAreaCheckMarkPhone'),
}

function checkThemeCookie(){
    let cookies = document.cookie
    for (let cookie of cookies.split('; ')) {
        if(cookie.startsWith('theme')){
            var cookieValue = cookie.split('=')[1]
        }
    }
    if (cookieValue != null){
        switch (cookieValue){
            case 'samurai':
            case 'forest':
            case 'factory':
            case 'white_area':
                setTheme(cookieValue)
                break;
            case 'secret':
                setTheme('samurai')
                break
        }
    }
}

function setTheme(themeName){
    for(var key in checkMarks){
        themeClass = key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join('');
        if (key == themeName){
            checkMarks[key].classList.add("on")
            phoneCheckMarks[key].classList.add("on")
            body.classList.add(themeClass)
            document.cookie = `theme=${key};max-age=${tenYearsAhead}`
            if (themeName != 'secret'){
                document.getElementById("YobaLogo").setAttribute('src', document.getElementById("YobaLogo").getAttribute('src').replace('YobaSecretLogo.png', 'YobaLogo.png'))
            }
        }else{
            body.classList.remove(themeClass)
            checkMarks[key].classList.remove("on")
            phoneCheckMarks[key].classList.remove("on")
        }
    }
}


//Никит блять, я конкретно не уважаю это порождение больного разума, но мне лень его трогать.
function ThemeMenu (){
    if (!ButtonThemMenuIcon.classList.contains('on') && !ButtonThemMenuIcon.classList.contains('off')){
        ButtonThemMenuIcon.classList.toggle('on')
    }else if (ButtonThemMenuIcon.classList.contains('on')){
        ButtonThemMenuIcon.classList.toggle('on')
        ButtonThemMenuIcon.classList.toggle('off')
    }else if(!ButtonThemMenuIcon.classList.contains('on')){
        ButtonThemMenuIcon.classList.toggle('off')
        ButtonThemMenuIcon.classList.toggle('on')
    }
    if (!ButtonThemMenu.classList.contains('on') && !ButtonThemMenu.classList.contains('off')){
        ButtonThemMenu.classList.toggle('on')
    }else if (ButtonThemMenu.classList.contains ('on')){
        ButtonThemMenu.classList.toggle('on')
        ButtonThemMenu.classList.toggle('off')
    }else if(!ButtonThemMenu.classList.contains('on')){
        ButtonThemMenu.classList.toggle('off')
        ButtonThemMenu.classList.toggle('on')
    }
}

checkThemeCookie()