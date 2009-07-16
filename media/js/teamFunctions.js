$(function() {
    $('.sortable').sortable({
        revert: false
    });
    $('.draggable').draggable({
        stop: function() {
                $(this).css("list-style-type", "none");
                $(this).css("text-decoration", "line-through");
                $(this).removeClass("draggable");
                $(this).addClass("pinned");
        },
        connectToSortable: '.sortable',
        addClasses: false,
        helper: 'clone',
        revert: 'invalid',
        cancel: '.pinned'
    });
    $('.team').droppable({
        drop: function(event, ui) {
            $('span.count', $(this)).text($(this).find('li').length - 1);
            $('#drop-message', $(this)).fadeOut();
        },
        accept: '.draggable'
    });
});
function saveTeams(){
    $('.team').each(function(){
        var pIdList = new Array();
        var gIdList = new Array();
        var teamId = $(this).attr('tm_id');
        var found = false;
        $('li', $(this)).each(function(){
            var plId = $(this).attr('pl_id');
            var guId = $(this).attr('gu_id');
            if(plId != null){
                pIdList.push(plId);
                found = true;
            }
            if(guId != null){
                gIdList.push(guId);
                found = true;
            }
        })
        if(found){
            $.post('/loadTeam/',
                    {'teamId': teamId, 'pList': pIdList.join(","), 'gList': gIdList.join(",")},
                    function(data){
                    }
            );
        }
    });
}
function showAddTeam(link) {
    $("#placeholder").css("display", "none");
    $("#placeholder").load(link).slideDown("slow");
}

function showDelTeam(link) {
    $("#placeholder").css("display", "none");
    $("#placeholder").load(link, function(){
        $("a.dellink").click(function(e){
            $.post("/links/delteam/",
                {md_id: $(this).attr('matchdayId'), team_id: $(this).attr('teamId')}
            );
            $(this).parent().siblings().css("text-decoration", "line-through");
            $(this).replaceWith('Deleted');
            $('div[tm_id="' + $(this).attr('teamId') + '"]').fadeOut("slow");
            e.preventDefault();
        });
    }).slideDown("slow");
}