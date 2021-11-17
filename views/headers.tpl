<title>Tableaux {{" - "+table if table else ""}}</title>

<link rel="icon" type="image/png" href="/static/logo.png" />

<script src="/static/jquery-3.5.1.min.js" integrity="sha384-ZvpUoO/+PpLXR1lu4jmpXWu80pZlYUAfxl5NsBMWOEPSjUn/6Z/hRTt8+pR6L4N2"></script>

<script src="/static/jquery.dataTables.min.js" integrity="sha384-XnTxmviuqUy3cHBf+lkYWuTSDlhxCDxd9RgSo5zvzsCq93P9xNa6eENuAITCwxNh"></script>


<script src="/static/dataTables.buttons.min.js" integrity="sha384-MGimb05YiSGNcXiLlj03UNahXBECHmFTe5iVBqh6sf2G7ccabI3/EOqzBnNw97/T"></script>
<script src="/static/buttons.html5.min.js" integrity="sha384-pp2ArcKo71umWphZ7QCCjQbnICkbOkLF88ZeoeZDPbqdAVvxZlcrla3lyT7pY/ue"></script>
<script src="/static/buttons.print.min.js" integrity="sha384-mOGjUrCoMJ8/pGqc8SQHuJdYPrdB9cjSkiuLQbw6D7orbJyMkk6xYDlYtkEH051d"></script>
<script src="/static/theme.js" integrity="sha384-bjcyLhD3HIrP9mAbeiSLqbyPugYFcs+BRD4OOhIWzCgoFwZ46GTetSvOUZfe98PD"></script>

<link rel="stylesheet" type="text/css" href="/static/jquery.dataTables.min.css" integrity="sha384-fMhhhMktDQZbvmPfBnKagbr1oS3tDYtFDoOCrnSjq1tZ3kmY/2Tm3Ei7uAL2hAS1"></link>

<link rel="stylesheet" href="/static/pure.min.css" integrity="sha384-UU8kk90p/K2Nap2Aw4M19cGNy16njCCgQLQ455EmZqROSNzpHaVc4jN+g4GoxZLC">
<link rel="stylesheet" href="/static/index.css" integrity="sha384-BzYXkMkVMBVdvnIydG8Y/uBOiiCYbrK6dBafWoPw9WbDPP1zU+4NBdCVy1GpAMBc">


% if table:

<script>
$(document).ready( function () {
        $('#myTable').DataTable({
            "paging": false,
            "info": false,
            "stateSave": true,
            "language" : {
                "search": "",
                "searchPlaceholder": "search"
            },
            "dom":"Bftr",
            initComplete: function(){
                $('#myTable_filter label input').focus();
            },
             buttons: [
                { extend: 'copy', className: 'pure-button' },
                { extend: 'csv', className: 'pure-button' },
                { extend: 'print', className: 'pure-button' },
				{
		            text: 'Reset sorting',
		            action: function ( e, dt, node, config ) {
                        $('#myTable').DataTable().order([]).draw();location.reload();
                    },
                    className: 'pure-button'
                 }
            ]
        });
} );

%if writeable:

$( document ).ready(function() {
  $("td").focusout(function(){
        $(this).addClass("edited");
        $(this).parent().children().last().children(":button").first().addClass("button-green");
  });
});


$( document ).ready(function() {
  $('td').keydown(function (e) {
    if ((e.ctrlKey || e.metaKey) && (e.keyCode == 13 || e.keyCode == 10)) {
        // Ctrl-Enter pressed
        submitRowAsForm($(this).parent().attr('id'));

    }
  });
});

$( document ).ready(function() {
  $(".delete-button").click(function(){
      if($(this).hasClass("button-red")){
          idRow = $(this).attr("data-rowid");
          form = document.createElement("form");
          form.method = "post";
          form.action = "/{{table}}/{{view}}/delete/"+idRow;
          document.body.appendChild(form);
          form.submit();
      }
      else{
          $(this).addClass("button-red");
      }
  });
});

function submitRowAsForm(idRow) {
  form = document.createElement("form"); // CREATE A NEW FORM TO DUMP ELEMENTS INTO FOR SUBMISSION
  form.method = "post"; // CHOOSE FORM SUBMISSION METHOD, "GET" OR "POST"
  form.action = "/{{table}}/{{view}}/update/"+idRow; // TELL THE FORM WHAT PAGE TO SUBMIT TO
  $("#"+idRow+" td").each(function() { // GRAB ALL <TD> IN THE ROW IDENTIFIED BY idRow, CLONE THEM, AND DUMP THEM IN OUR FORM
		if(this.getAttribute("data-col")){
	        textarea = document.createElement("textarea"); // CREATE AN ELEMENT TO COPY VALUES TO
	        textarea.style = "visibility:hidden;position:absolute;";
	        textarea.name = this.getAttribute("data-col"); // GIVE ELEMENT SAME NAME AS THE <SELECT>
	        textarea.value = this.innerText; // ASSIGN THE VALUE FROM THE <SELECT>
            console.log(this.textContent);
	        form.appendChild(textarea);
		}

    }
    );
  document.body.appendChild(form);
  form.submit(); // NOW SUBMIT THE FORM THAT WE'VE JUST CREATED AND POPULATED
}
%end
</script>
%end
