$(function(){
    $.ajaxSetup({ cache: false });
    fadeOutMessages();
});

function fadeOutMessages(){
    $("li.message").each(function () {
        $(this).fadeOut(12000);
    });
}

function showMessages(){
    $("#messages_block").load("/messages/", fadeOutMessages);
}
