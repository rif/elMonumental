$(document).ready(function(){
    $("li.message").each(function () {
        $(this).fadeOut(13000);
    });
});

function showAddGuest(link) {
    $("#placeholder").load(link);
}

function showDelGuest(link) {
    $("#placeholder").load(link, function(){
        $("a.dellink").click(function(e){
            $.post("/links/delguest/",
            {
                md_id: $(this).attr('matchdayId'),
                guest_id: $(this).attr('guestId')
            });
            $(this).replaceWith('Deleted');
            e.preventDefault();
        });
    });
}
function showEmailForm(md_id) {
    $.get("/getemailform/" + md_id + "/", function(responseData){
        $("div#email_form").html(responseData);
        $("a#send_email").fadeOut("slow");
        $("div#email_form").fadeIn(3000, function () {
            $("form").fadeIn(100);
        });
    });
}