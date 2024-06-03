window.addEventListener("scroll",function(){
    var nav = document.getElementById("navbar");
    nav.classList.toggle("sticky", window.scrollY > 20 );
})