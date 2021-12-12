//=================================================== Preloader ====================================================//
const themes = {'samurai': SamuraiTheme, 'forest': ForestTheme, 'factory': FactoryTheme, 'white_area': WhiteAreaTheme}

window.onload = function(){
    setTimeout( function() {
        var preloader = document.getElementById('loadScreenId');
        if(preloader.classList.contains('done')){
        }
        else{
            preloader.classList.add('done');
        }
    }, 500);

    
    const storage = window.localStorage
    let theme = storage.getItem('theme')

    if(!(theme == null) && !Object.keys(themes).includes(theme) ){
        storage.removeItem('theme')
    }

    if( !(theme == null) ){
        themes[theme]()
    }
}