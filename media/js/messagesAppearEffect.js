function showMessages() {
    $.get('/messages/', function(responseData){
        $("#messages").html(responseData);
    });
}

$(document).ready(function(){
   $("li.message").each(function () {
         $(this).fadeOut(16000);
    });
});