//=================================================== Preloader ====================================================//
window.onload = function(){
    setTimeout( function() {
        var preloader = document.getElementById('loadScreenId');
        preloader.classList.add("done")
    }, 500);
}