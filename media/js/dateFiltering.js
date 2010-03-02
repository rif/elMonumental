$(function() {
    $("#since").datepicker({
                dateFormat: 'dd-mm-yy',
                onClose: function(dateText, inst) {
                }
    });
    sortTable();
  });

function sortTable(){
     $("#usersTable").tablesorter(
                    {headers: { 8:  {sorter: false},
                                10: {sorter: false},
                                12: {sorter: false}, 
				14: {sorter: false},
				},
		    widthFixed: true
                    }
     );//.tablesorterPager({container: $("#pager")});
}

