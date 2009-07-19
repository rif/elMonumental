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
        $("#placeholder").hide();
        $("#placeholder").load("/matchday/" + $(this).parent().attr('md_id') + "/").slideDown("slow");
        e.preventDefault();
    });
});

function showAddGuest(link) {
    $("#placeholder").hide();
    $("#placeholder").load(link).slideDown("slow");
}

function showDelGuest(link) {
    $("#placeholder").hide();
    $("#placeholder").load(link, function(){
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
    }).slideDown("slow");
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