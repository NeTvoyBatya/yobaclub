//=================================================== Preloader ====================================================//
window.onload = function(){
    setTimeout( function() {
        var preloader = document.getElementById('loadScreenId');
        if(preloader.classList.contains('done')){
        }
        else{
            preloader.classList.add('done');
        }
    }, 500);
}