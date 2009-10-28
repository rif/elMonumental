$(function(){
    /*$.ajaxSetup({ 
        cache: false
    });*/
    fadeOutMessages();
});

function fadeOutMessages(){
    $("li.message").fadeOut(12000);
}

function showMessages(){
    setTimeout(function (){$("#messages_block").load("/messages/", fadeOutMessages);}, 1000);
}

function loadPlaceholder(link){
    $("#placeholder").hide().load(link).slideDown("slow");
}

function loadPlaceholder(link, callback){
    $("#placeholder").hide().load(link, callback).slideDown("slow");
}
