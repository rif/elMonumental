$(function(){
    $.ajaxSetup({ cache: false });
    $("li.message").each(function () {
        $(this).fadeOut(13000);
    });
});
