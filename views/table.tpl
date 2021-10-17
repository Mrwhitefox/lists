<table id="myTable" class="pure-table compact row-border hover stripe">
<thead>
<tr>
% for col in view_columns[table][view]:
<th>{{col}}</th>
% end
<th></th>
</tr>
</thead>
<tbody>
%for t in tasks:
<tr id="{{t.id}}">
% for c in view_columns[table][view]:
<td contenteditable="true" data-col={{c}}>{{! t.getHtml(c)}}</td>
% end
<td>
    <button class="pure-button" onclick="submitRowAsForm('{{t.id}}')">✔</button>
    <button class="pure-button delete-button" data-rowid={{t.id}}>X</button>
    
    </td>
</tr>
%end
</tbody>
</table>
