$(document).ready(function() {
    $("#matchdays").corner();
    $("#news").corner();
    $("span.async").each(function(){
        var span = $(this);
        $.post('links/', {
            md_id:$(this).attr('md_id')
        }, function(responseData){
            $(span).prepend(responseData);
        });
    });
    $("a.md-detail-link").click(function(e){
        loadPlaceholder("/matchday/" + $(this).parent().attr('md_id') + "/");
        e.preventDefault();
    });
});

function showAddGuest(link) {
    loadPlaceholder(link);
}

function showDelGuest(link) {
    loadPlaceholder(link, function(){
        $("a.dellink").click(function(e){
            $.post("/links/delguest/",
            {
                md_id: $(this).attr('matchdayId'),
                guest_id: $(this).attr('guestId')
            });
            $(this).parent().siblings().css("text-decoration", "line-through");
            $(this).replaceWith('Deleted');
            e.preventDefault();
        });
    });
}
function showEmailForm(md_id) {
    $.get("/getemailform/" + md_id + "/", function(responseData){
        $("#email_form").html(responseData);
        $("#send_email").fadeOut("slow");
        $("#email_form").fadeIn(3000, function () {
            $("form").fadeIn(100);
        });
    });
}
