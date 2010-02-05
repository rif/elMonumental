$(function() {
    $("#since").datepicker({
                dateFormat: 'dd-mm-yy',
                onClose: function(dateText, inst) {
                            filtrare();
                }
    });
    $("a#filter").click(function(e){
                filtrare();
                e.preventDefault();
    });
    sortTable();
  });

function filtrare(){
    $.post('/filterProfiles/', {'since': $("#since").val()},
                    function(responseData){
            	       $("tbody").html(responseData);
	   });
    sortTable();
}

function sortTable(){
     $("#usersTable").tablesorter(
                    {headers: { 8: { sorter: false},
                                10: {sorter: false},
                                12: {sorter: false} }
                    }
     );
}