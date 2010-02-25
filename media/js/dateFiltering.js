$(function() {
    $("#since").datepicker({
                dateFormat: 'dd-mm-yy',
                onClose: function(dateText, inst) {
                            filtrare();
                }
    });
    $("a#reset").click(function(e){
                $("#since").val('');
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

