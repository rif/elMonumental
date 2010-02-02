$(function() {
    $("#since").datepicker({dateFormat: 'dd-mm-yy',
                                                             onClose: function(dateText, inst) { filtrare(); }
			                                            });
      $("a#filter").click(function(e){
			      filtrare();
			      e.preventDefault();
			  });
  });

function filtrare(){
    $.post('/filterProfiles/', {'since': $("#since").val()},
                    function(responseData){
            	       $("tbody").html(responseData);
	   });
}

