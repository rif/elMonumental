
$(function() {
    var myBorder = RUZEE.ShadedBorder.create({ corner:8, shadow:16});
    myBorder.render('teams');
    $('.sortable').sortable({
        revert: false
    });
    $('.draggable').draggable({
        stop: function(event, ui) {
            var target = $(document.elementFromPoint(event.pageX, event.pageY)).parent();
            var parent = target.parent();
            var droppedOnTeam = false;
            $('.team').each(function(){
                if($(this).attr('tm_id') == parent.attr('tm_id')){
                    droppedOnTeam = true;
                }
            });
            if(droppedOnTeam){
                $(this).css("list-style-type", "none");
                $(this).css("text-decoration", "line-through");
                $(this).removeClass("draggable");
                $(this).addClass("pinned");
                $('#drop-message', target).remove();
                $('span.count', parent).text(target.find('li').length);
            }
        },
        connectToSortable: '.sortable',
        addClasses: false,
        helper: 'clone',
        revert: 'invalid',
        zIndex: 2700,
        cursor: 'move',
        cancel: '.pinned'
    });

    $('#save_teams_link').click(function(e){
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
            });
            if(found){
                $.post('/loadTeam/',
                {
                    'teamId': teamId,
                    'pList': pIdList.join(","),
                    'gList': gIdList.join(",")
                }
                );
		showMessages();
            }
        });
        e.preventDefault();
    });
    $('#save_proposal_link').click(function(e){
        var found = false;
        var pList = new Array();
        $('.team').each(function(){
            pList.push($.trim($('#team_title', this).text()));
            $('li', $(this)).each(function(){
                var plName = $.trim($(this).text());
                if(plName != null){
                    pList.push(plName);
                    found = true;
                }
            });
            pList.push("|");
        });
        if(found){
            $.post('/addProposal/', {
                'md_id': $('#teams').attr('md_id'),
                'entries': pList.join(",")
            });
	    showMessages();
        }
        e.preventDefault();
    });
    $('#create_team_link').click(function(e){
        loadPlaceholder($(this).attr("href"));
        e.preventDefault();
    });
    $('#delete_team_link').click(function(e){
        loadPlaceholder($(this).attr("href"), function(){
            $("a.dellink").click(function(e){
                $.post("/links/delteam/",
                {
                    md_id: $(this).attr('matchdayId'),
                    team_id: $(this).attr('teamId')
                }
                );
                $(this).parent().siblings().css("text-decoration", "line-through");
                $(this).replaceWith('Deleted');
                $('div[tm_id="' + $(this).attr('teamId') + '"]').fadeOut("slow");
                showMessages();
                e.preventDefault();
            });
        });
        e.preventDefault();
    });
});
