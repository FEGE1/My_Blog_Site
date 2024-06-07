var path = window.location.pathname;
var nav = document.getElementById("navbar");

if(path=="/"){
    window.addEventListener("scroll",function(){            
        nav.classList.toggle("sticky", window.scrollY > 40 );
    })
}
else{
    nav.classList.add( "sticky");
}
