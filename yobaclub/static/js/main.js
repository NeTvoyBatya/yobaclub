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

function ThemeMenu (){
    ButtonThemMenuIcon.classList.toggle('on')
    ButtonThemMenu.classList.toggle('on')
}
function SamuraiTheme(){
    SamuraiCheckBox.toggleAttribute('checked')
    if (SamuraiCheckBox.checked);
        SamuraiCheckMark.classList.add('on')
        ForestCheckMark.classList.remove('on')
        FactoryCheckMark.classList.remove('on')
        WhiteAreaCheckMark.classList.remove('on')
}
function ForestTheme(){

    ForestCheckBox.toggleAttribute('checked')
    if (ForestCheckMark.checked);
        ForestCheckMark.classList.add('on')
        SamuraiCheckMark.classList.remove('on')
        FactoryCheckMark.classList.remove('on')
        WhiteAreaCheckMark.classList.remove('on')
}
function FactoryTheme(){
   
    FactoryCheckBox.toggleAttribute('checked')
    if (FactoryCheckMark.checked);
        FactoryCheckMark.classList.add('on')
        SamuraiCheckMark.classList.remove('on')
        ForestCheckMark.classList.remove('on')
        WhiteAreaCheckMark.classList.remove('on')
}
function WhiteAreaTheme(){

    WhiteAreaCheckBox.toggleAttribute('checked')
    if (WhiteAreaCheckMark.checked);
        WhiteAreaCheckMark.classList.add('on')
        SamuraiCheckMark.classList.remove('on')
        FactoryCheckMark.classList.remove('on')
        ForestCheckMark.classList.remove('on')
}