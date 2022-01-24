var ButtonThemMenu = document.getElementById('ThemeMenuId');
var ButtonThemMenuIcon = document.getElementById('ThemeMenuIcon');
var SamuraiCheckBox = document.getElementById('SamuraiCheckBoxId')
var SamuraiCheckMark = document.getElementById('SamuraiCheckMark')
var ForestCheckBox = document.getElementById('ForestCheckBoxId')
var ForestCheckMark = document.getElementById('ForestCheckMark')
var FactoryCheckBox = document.getElementById('FactoryCheckBoxId')
var FactoryCheckMark = document.getElementById('FactoryCheckMark')
var WhiteAreaCheckBox = document.getElementById('WhiteAreaCheckBoxId')
var WhiteAreaCheckMark = document.getElementById('WhiteAreaCheckMark')
var BodyBacgroundTheme = document.getElementById('body')
var tenYearsAhead = 3650*24*60*60

let cookies = document.cookie
for (let cookie of cookies.split('; ')) {
    if(cookie.startsWith('theme')){
        var cookieValue = cookie.split('=')[1]
    }
}
if (cookieValue != null){
    switch (cookieValue){
        case 'samurai':
            SamuraiCheckBox.toggleAttribute('checked')
            SamuraiCheckMark.classList.add('on')
            break;
        case 'forest':
            ForestCheckBox.toggleAttribute('checked')
            ForestCheckMark.classList.add('on')
            break;
        case 'factory':
            FactoryCheckBox.toggleAttribute('checked')
            FactoryCheckMark.classList.add('on')
            break;
        case 'white_area':
            WhiteAreaCheckBox.toggleAttribute('checked')
            WhiteAreaCheckMark.classList.add('on')
            break;
    }
}

function ThemeMenu (){
    if (ButtonThemMenuIcon.classList.contains ('on') != true && ButtonThemMenuIcon.classList.contains ('off') != true){
        ButtonThemMenuIcon.classList.toggle('on')
    }else if (ButtonThemMenuIcon.classList.contains ('on')){
        ButtonThemMenuIcon.classList.toggle('on')
        ButtonThemMenuIcon.classList.toggle('off')
    }else if(ButtonThemMenuIcon.classList.contains ('on') != true){
        ButtonThemMenuIcon.classList.toggle('off')
        ButtonThemMenuIcon.classList.toggle('on')
    }
    if (ButtonThemMenu.classList.contains ('on') != true && ButtonThemMenu.classList.contains ('off') != true){
        ButtonThemMenu.classList.toggle('on')
    }else if (ButtonThemMenu.classList.contains ('on')){
        ButtonThemMenu.classList.toggle('on')
        ButtonThemMenu.classList.toggle('off')
    }else if(ButtonThemMenu.classList.contains ('on') != true){
        ButtonThemMenu.classList.toggle('off')
        ButtonThemMenu.classList.toggle('on')
    }
}
function SamuraiTheme(){
    SamuraiCheckBox.toggleAttribute('checked')
    if (SamuraiCheckBox.checked);
        SamuraiCheckMark.classList.add('on')
        ForestCheckMark.classList.remove('on')
        FactoryCheckMark.classList.remove('on')
        WhiteAreaCheckMark.classList.remove('on')

        BodyBacgroundTheme.classList.add('Samurai')
        BodyBacgroundTheme.classList.remove('Forest')
        BodyBacgroundTheme.classList.remove('Factory')
        BodyBacgroundTheme.classList.remove('WhiteArea')
        document.cookie = `theme=samurai;max-age=${tenYearsAhead};`

}
function ForestTheme(){

    ForestCheckBox.toggleAttribute('checked')
    if (ForestCheckMark.checked);
        ForestCheckMark.classList.add('on')
        SamuraiCheckMark.classList.remove('on')
        FactoryCheckMark.classList.remove('on')
        WhiteAreaCheckMark.classList.remove('on')

        BodyBacgroundTheme.classList.remove('Samurai')
        BodyBacgroundTheme.classList.add('Forest')
        BodyBacgroundTheme.classList.remove('Factory')
        BodyBacgroundTheme.classList.remove('WhiteArea')
        document.cookie = `theme=forest;max-age=${tenYearsAhead};`
}
function FactoryTheme(){
   
    FactoryCheckBox.toggleAttribute('checked')
    if (FactoryCheckMark.checked);
        FactoryCheckMark.classList.add('on')
        SamuraiCheckMark.classList.remove('on')
        ForestCheckMark.classList.remove('on')
        WhiteAreaCheckMark.classList.remove('on')

        BodyBacgroundTheme.classList.remove('Samurai')
        BodyBacgroundTheme.classList.remove('Forest')
        BodyBacgroundTheme.classList.add('Factory')
        BodyBacgroundTheme.classList.remove('WhiteArea')
        document.cookie = `theme=factory;max-age=${tenYearsAhead};`
}
function WhiteAreaTheme(){

    WhiteAreaCheckBox.toggleAttribute('checked')
    if (WhiteAreaCheckMark.checked);
        WhiteAreaCheckMark.classList.add('on')
        SamuraiCheckMark.classList.remove('on')
        FactoryCheckMark.classList.remove('on')
        ForestCheckMark.classList.remove('on')
        
        BodyBacgroundTheme.classList.remove('Samurai')
        BodyBacgroundTheme.classList.remove('Forest')
        BodyBacgroundTheme.classList.remove('Factory')
        BodyBacgroundTheme.classList.add('WhiteArea')
        document.cookie = `theme=white_area;max-age=${tenYearsAhead};`
}