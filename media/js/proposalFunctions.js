$(function(){
    $("a.proposals_link").click(function(e){
        loadPlaceholder($(this).attr("href"));
        e.preventDefault();
    });
    $("a.delete_proposal_link").click(function(e){
        var delLink = $(this);
        $.get(delLink.attr("href"), function(){
            delLink.siblings().css("text-decoration", "line-through");
            delLink.replaceWith('Deleted');
        });
        e.preventDefault();
    });
});
