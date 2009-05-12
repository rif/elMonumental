$(document).ready(function(){
    $("li.message").each(function () {
        $(this).fadeOut(16000);
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