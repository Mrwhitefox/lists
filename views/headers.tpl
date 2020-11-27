<title>Tableaux {{" - "+table if table else ""}}</title>

<link rel="icon" type="image/png" href="/static/logo.png" />

<script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>

<script src="https://cdn.datatables.net/1.10.22/js/jquery.dataTables.min.js"></script>

<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.22/css/jquery.dataTables.min.css"></link>

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
            }
            
        });
} );



$( document ).ready(function() {
  $("td").focusout(function(){
        $(this).parent().children().last().children(":button").first().addClass("button-green").removeClass("button-blue");
  });
});

$( document ).ready(function() {
  $(".delete-button").click(function(){
      console.log("triggered!");
      if($(this).hasClass("button-red")){
      console.log("triggered!A");
          idRow = $(this).attr("data-rowid");
          form = document.createElement("form");
          form.method = "post";
          form.action = "/delete/"+idRow;
          document.body.appendChild(form);
          form.submit();
      }
      else{
      console.log("triggered!B");
          $(this).addClass("button-red");
      }
  });
});




function submitRowAsForm(idRow) {
  form = document.createElement("form"); // CREATE A NEW FORM TO DUMP ELEMENTS INTO FOR SUBMISSION
  form.method = "post"; // CHOOSE FORM SUBMISSION METHOD, "GET" OR "POST"
  form.action = "/update/"+idRow; // TELL THE FORM WHAT PAGE TO SUBMIT TO
  $("#"+idRow+" td").each(function() { // GRAB ALL <TD> IN THE ROW IDENTIFIED BY idRow, CLONE THEM, AND DUMP THEM IN OUR FORM
		if(this.getAttribute("data-col")){
	        input = document.createElement("input"); // CREATE AN ELEMENT TO COPY VALUES TO
	        input.type = "hidden";
	        input.name = this.getAttribute("data-col"); // GIVE ELEMENT SAME NAME AS THE <SELECT>
	        input.value = this.textContent; // ASSIGN THE VALUE FROM THE <SELECT>
	        form.appendChild(input);
		}

    });
  document.body.appendChild(form);
  form.submit(); // NOW SUBMIT THE FORM THAT WE'VE JUST CREATED AND POPULATED
}
</script>
