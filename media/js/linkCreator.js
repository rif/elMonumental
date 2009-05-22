$(document).ready(function() {
    $("span.async").each(function(){
        var span = $(this);
        $.post('links/', {
            md_id:$(this).attr('md_id')
            }, function(responseData){
            $(span).prepend(responseData);
        });
    });
    $("a.md-detail-link").click(function(e){
        $.get("/matchday/" + $(this).parent().attr('md_id') + "/",
            function(responseData){
                $("div#placeholder").html(responseData);
            });
        e.preventDefault();
    });
});