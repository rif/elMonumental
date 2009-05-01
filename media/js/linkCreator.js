$(document).ready(function() {
    $("span.async").each(function(){
        var span = $(this);
        $.post('links/', {md_id:$(this).attr('id')}, function(responseData){
            $(span).html(responseData);
        });
    });
});