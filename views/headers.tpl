<title>Tableaux {{" - "+table if table else ""}}</title>

<link rel="icon" type="image/png" href="/static/logo.png" />

<script src="/static/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>

<script src="/static/jquery.dataTables.min.js"></script>


<script src="/static/dataTables.buttons.min.js"></script>
<script src="/static/jszip.min.js"></script>
<script src="/static/pdfmake.min.js"></script>
<script src="/static/vfs_fonts.js"></script>
<script src="/static/buttons.html5.min.js"></script>
<script src="/static/buttons.print.min.js"></script>

<link rel="stylesheet" type="text/css" href="/static/jquery.dataTables.min.css"></link>

<link rel="stylesheet" href="/static/pure.min.css" crossorigin="anonymous">
<link rel="stylesheet" href="/static/index.css">

<style>
.dataTables_filter input { width: 100% }
.dataTables_filter { width: 100% }

td[contenteditable="true"]:focus {
    background-color: #FF4040;
}

.edited{
    background-color: #FF4040;
}
</style>


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
             buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print',
				{
		            text: 'Reset filters',
		            action: function ( e, dt, node, config ) {
                        $('#myTable').DataTable().order([]).draw();location.reload();
                    }
                 }
            ]
        });
} );




$( document ).ready(function() {
  $("td").focusout(function(){
        $(this).parent().children().last().children(":button").first().addClass("button-green").removeClass("button-blue");
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
</script>
