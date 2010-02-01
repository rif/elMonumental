$(function() {
      $("#de_la").datepicker({dateFormat: 'dd-mm-yy',
			      onClose: function(dateText, inst) { filtrare(); }
			     });
      $("#pana_la").datepicker({dateFormat: 'dd-mm-yy',
				onClose: function(dateText, inst) { filtrare(); }
			       });
      $("a#filtru").click(function(e){
			      filtrare();
			      e.preventDefault();
			  });
  });

function filtrare(){
    $.post('/filtreaza/', {
	       'de_la': $("#de_la").val(),
	       'pana_la': $("#pana_la").val()
	   }, function(responseData){
	       $("tbody").html(responseData);
	   });
}