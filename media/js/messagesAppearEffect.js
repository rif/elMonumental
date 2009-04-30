$(document).ready(function(){
   $("li.message").ready(function (liElement) {
        alert("As you can see, the link no longer took you to jquery.com");
         $(liElement).fadeOut("slow");
    });
});
