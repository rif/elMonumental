$(document).ready(function(){
    $.ajaxSetup({ cache: false });
    $("li.message").each(function () {
        $(this).fadeOut(13000);
    });
});

function showAddGuest(link) {
    $("#placeholder").css("display", "none");
    $("#placeholder").load(link).slideDown("slow");
}

function showDelGuest(link) {
    $("#placeholder").css("display", "none");
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
