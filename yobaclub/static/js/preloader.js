//=================================================== Preloader ====================================================//
window.onload = function(){
    setTimeout( function() {
        var preloader = document.getElementById('loadScreenId');
        var mainBody = document.getElementById('body')
        if(preloader.classList.contains('done')){
        }
        else{
            preloader.classList.add('done');
        }
        if(mainBody.classList.contains('done')){
        }
        else{
            mainBody.classList.add('done');
        }
    }, 500);
}