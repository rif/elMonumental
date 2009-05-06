$(document).ready(function(){
    $("a.dellink").click(function(e){
        $.post("/links/delguest/",
            { md_id: $(this).attr('matchdayId'),
              guest_id: $(this).attr('guestId')
            });
        $(this).replaceWith('Deleted');
        e.preventDefault();
    });
});
